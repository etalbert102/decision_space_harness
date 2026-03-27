from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_space_harness.experiments.runner import execute_experiment  # noqa: E402


def test_sample_experiment_runs_end_to_end() -> None:
    config_path = ROOT / "experiments" / "configs" / "conflict_smoothing_v1.yaml"
    summary = execute_experiment(config_path)
    output_dir = ROOT / "outputs" / "experiments" / "conflict_smoothing_v1"

    assert summary["attempt_count"] == 1
    assert summary["selected_run_count"] == 1
    assert summary["metric_result_count"] == 1

    attempts_path = output_dir / "attempts.jsonl"
    runs_path = output_dir / "runs.jsonl"
    metrics_path = output_dir / "metrics.jsonl"
    messages_path = output_dir / "message_records.jsonl"
    summary_path = output_dir / "summary.json"

    assert attempts_path.exists()
    assert runs_path.exists()
    assert metrics_path.exists()
    assert messages_path.exists()
    assert summary_path.exists()

    metric_rows = [json.loads(line) for line in metrics_path.read_text().splitlines() if line]
    message_rows = [json.loads(line) for line in messages_path.read_text().splitlines() if line]
    assert metric_rows[0]["metric_id"] == "conflict_retention"
    assert metric_rows[0]["status"] == "scored"
    assert metric_rows[0]["score"] == pytest.approx(0.5)
    assert len(message_rows) == 1
    assert message_rows[0]["sender_agent"] == "baseline_direct"
    assert message_rows[0]["receiver_agent"] == "baseline_direct"
