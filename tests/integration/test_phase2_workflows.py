from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_space_harness.experiments.runner import execute_experiment  # noqa: E402


def test_multi_agent_sweep_runs_all_phase2_agents_and_variants() -> None:
    config_path = ROOT / "experiments" / "configs" / "conflict_multi_agent_v1.yaml"
    summary = execute_experiment(config_path)
    output_dir = ROOT / "outputs" / "experiments" / "conflict_multi_agent_v1"

    assert summary["attempt_count"] == 16
    assert summary["selected_run_count"] == 16
    assert summary["metric_result_count"] == 16

    attempts = [
        json.loads(line)
        for line in (output_dir / "attempts.jsonl").read_text().splitlines()
        if line
    ]
    agent_names = {row["agent_config"] for row in attempts}
    prompt_variants = {row["prompt_variant"] for row in attempts}
    assert agent_names == {
        "baseline_direct",
        "retrieve_then_synthesize",
        "option_generation",
        "structured_conflict_preserving",
    }
    assert prompt_variants == {"default", "disagreement_preserving"}


def test_perturbation_group_workflow_emits_group_metadata() -> None:
    config_path = ROOT / "experiments" / "configs" / "conflict_perturbation_v1.yaml"
    summary = execute_experiment(config_path)
    output_dir = ROOT / "outputs" / "experiments" / "conflict_perturbation_v1"

    assert summary["attempt_count"] == 8
    attempts = [
        json.loads(line)
        for line in (output_dir / "attempts.jsonl").read_text().splitlines()
        if line
    ]
    assert all(row["comparison_group_id"].startswith("policy_01_") for row in attempts)
    assert {row["evidence_bundle"]["operator_id"] for row in attempts} == {
        "shuffle_evidence/v1",
        "reverse_evidence/v1",
    }
    assert len({row["comparison_group_id"] for row in attempts}) == 4
    counts_by_group = {}
    for row in attempts:
        counts_by_group[row["comparison_group_id"]] = (
            counts_by_group.get(row["comparison_group_id"], 0) + 1
        )
    assert all(count == 2 for count in counts_by_group.values())
