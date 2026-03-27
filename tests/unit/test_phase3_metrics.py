from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_space_harness.metrics.frame_preservation import FramePreservationMetric  # noqa: E402
from decision_space_harness.metrics.option_breadth import OptionBreadthMetric  # noqa: E402
from decision_space_harness.metrics.path_dependence import PathDependenceMetric  # noqa: E402
from decision_space_harness.schemas.core import MetricSubject, Task  # noqa: E402


def _load_task() -> Task:
    payload = yaml.safe_load(
        (ROOT / "data" / "tasks" / "synthetic" / "conflict_policy_01.yaml").read_text()
    )
    return Task.from_dict(payload)


def test_frame_and_option_metrics_score_expected_ratios() -> None:
    task = _load_task()
    subject = MetricSubject(
        subject_type="selected_run",
        subject_id="cell_1",
        record={
            "task_id": task.task_id,
            "normalized_artifacts": {
                "payload": {
                    "parse_status": "valid",
                    "represented_frames": ["economic"],
                    "generated_option_ids": ["policy_x"],
                }
            },
        },
    )

    frame_result = FramePreservationMetric().score_subject(subject, {"task": task})
    option_result = OptionBreadthMetric().score_subject(subject, {"task": task})

    assert frame_result.score == pytest.approx(0.5)
    assert option_result.score == pytest.approx(0.5)


def test_path_dependence_scores_group_divergence() -> None:
    metric = PathDependenceMetric()
    subject = MetricSubject(
        subject_type="comparison_group",
        subject_id="group_1",
        record={
            "comparison_group_id": "group_1",
            "members": [
                {
                    "eligible_for_metric_scoring": True,
                    "normalized_artifacts": {
                        "payload": {
                            "parse_status": "valid",
                            "represented_frames": ["economic", "legal"],
                            "preserved_conflict_ids": ["cost_burden"],
                            "generated_option_ids": ["policy_x"],
                            "selected_option_id": "policy_x",
                        }
                    },
                },
                {
                    "eligible_for_metric_scoring": True,
                    "normalized_artifacts": {
                        "payload": {
                            "parse_status": "valid",
                            "represented_frames": ["economic"],
                            "preserved_conflict_ids": ["enforcement_risk"],
                            "generated_option_ids": ["policy_y"],
                            "selected_option_id": "policy_y",
                        }
                    },
                },
            ],
        },
    )

    result = metric.score_subject(subject, {"task": None})

    assert result.status == "scored"
    assert result.score == pytest.approx(0.875)
