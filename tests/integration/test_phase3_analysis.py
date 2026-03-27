from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_space_harness.experiments.runner import execute_experiment  # noqa: E402


def test_phase3_analysis_emits_group_metrics_and_reports() -> None:
    config_path = ROOT / "experiments" / "configs" / "conflict_phase3_analysis_v1.yaml"
    summary = execute_experiment(config_path)
    output_dir = ROOT / "outputs" / "experiments" / "conflict_phase3_analysis_v1"

    assert summary["attempt_count"] == 8
    assert summary["selected_run_count"] == 8
    assert summary["metric_result_count"] == 36

    metrics = [
        json.loads(line)
        for line in (output_dir / "metrics.jsonl").read_text().splitlines()
        if line
    ]
    path_rows = [row for row in metrics if row["metric_id"] == "path_dependence"]
    assert len(path_rows) == 4
    assert {row["subject_type"] for row in path_rows} == {"comparison_group"}

    summary_table = json.loads((output_dir / "summary_table.json").read_text())
    assert {row["metric_id"] for row in summary_table["overall"]} == {
        "conflict_retention",
        "frame_preservation",
        "lexical_jaccard_extension",
        "option_breadth",
        "path_dependence",
    }
    figure_text = (output_dir / "figures" / "metric_means.txt").read_text()
    assert "Metric Means" in figure_text
    assert "path_dependence" in figure_text
