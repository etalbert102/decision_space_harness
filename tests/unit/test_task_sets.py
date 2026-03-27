from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_space_harness.tasks.loader import load_task_set, validate_task  # noqa: E402


def test_synthetic_task_set_loads_all_phase1b_tasks() -> None:
    tasks = load_task_set(ROOT / "data" / "task_sets" / "conflict_tasks_v1.yaml")
    assert len(tasks) == 12
    assert all(task.source_type == "synthetic" for task in tasks)
    assert all(validate_task(task).ok for task in tasks)


def test_real_task_set_loads_provisional_real_tasks() -> None:
    tasks = load_task_set(ROOT / "data" / "task_sets" / "real_conflict_tasks_v1.yaml")
    assert len(tasks) == 8
    assert all(task.source_type == "real" for task in tasks)
    assert all(validate_task(task).ok for task in tasks)
