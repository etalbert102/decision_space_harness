from __future__ import annotations

from pathlib import Path

import yaml
from decision_space_harness.schemas.core import Task, ValidationResult


def load_task(task_path: str | Path) -> Task:
    path = Path(task_path)
    payload = yaml.safe_load(path.read_text())
    return Task.from_dict(payload)


def validate_task(task: Task) -> ValidationResult:
    errors: list[str] = []
    if task.task_family != "conflict_preservation":
        errors.append(f"Unsupported task family for phase 1B: {task.task_family}")
    if task.source_type not in {"synthetic", "real"}:
        errors.append(f"Unsupported source type: {task.source_type}")
    if not task.evidence_items:
        errors.append("Task must include at least one evidence item")
    if not task.annotations.get("candidate_option_ids"):
        errors.append("Task must include candidate_option_ids")
    return ValidationResult(ok=not errors, errors=errors)


def load_task_set(task_set_path: str | Path) -> list[Task]:
    path = Path(task_set_path)
    payload = yaml.safe_load(path.read_text())
    task_paths = payload.get("task_paths", [])
    tasks: list[Task] = []
    seen_task_ids: set[str] = set()
    for task_path in task_paths:
        resolved = (path.parent / task_path).resolve()
        task = load_task(resolved)
        if task.task_id in seen_task_ids:
            raise ValueError(f"Duplicate task_id in task set: {task.task_id}")
        seen_task_ids.add(task.task_id)
        tasks.append(task)
    return tasks
