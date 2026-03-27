from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_space_harness.experiments.runner import execute_experiment  # noqa: E402


def test_synthetic_suite_runs_all_expanded_tasks() -> None:
    config_path = ROOT / "experiments" / "configs" / "conflict_synthetic_suite_v1.yaml"
    summary = execute_experiment(config_path)
    output_dir = ROOT / "outputs" / "experiments" / "conflict_synthetic_suite_v1"

    assert summary["attempt_count"] == 12
    assert summary["selected_run_count"] == 12
    assert summary["metric_result_count"] == 12

    attempts = [
        json.loads(line)
        for line in (output_dir / "attempts.jsonl").read_text().splitlines()
        if line
    ]
    message_rows = [
        json.loads(line)
        for line in (output_dir / "message_records.jsonl").read_text().splitlines()
        if line
    ]
    assert len(attempts) == 12
    assert len(message_rows) == 12


def test_real_suite_runs_provisional_real_tasks() -> None:
    config_path = ROOT / "experiments" / "configs" / "conflict_real_docs_v1.yaml"
    summary = execute_experiment(config_path)
    output_dir = ROOT / "outputs" / "experiments" / "conflict_real_docs_v1"

    assert summary["attempt_count"] == 8
    assert summary["selected_run_count"] == 8
    assert summary["metric_result_count"] == 8

    metrics = [
        json.loads(line)
        for line in (output_dir / "metrics.jsonl").read_text().splitlines()
        if line
    ]
    message_rows = [
        json.loads(line)
        for line in (output_dir / "message_records.jsonl").read_text().splitlines()
        if line
    ]
    assert len(metrics) == 8
    assert len(message_rows) == 8
