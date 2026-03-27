from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_space_harness.normalizers.conflict_preservation import (  # noqa: E402
    ConflictPreservationNormalizer,
)
from decision_space_harness.schemas.core import AgentResult  # noqa: E402
from decision_space_harness.tasks.loader import load_task  # noqa: E402


@pytest.fixture()
def task():
    return load_task(ROOT / "data" / "tasks" / "synthetic" / "conflict_policy_01.yaml")


@pytest.fixture()
def normalizer():
    return ConflictPreservationNormalizer()


def test_normalize_valid_output(task, normalizer) -> None:
    agent_result = AgentResult(
        raw_output_text="\n".join(
            [
                "FINAL_ANSWER: Recommend policy_x while preserving key disagreement.",
                "SELECTED_OPTION: policy_x",
                "REPRESENTED_FRAMES: economic,legal",
                "PRESERVED_CONFLICTS: cost_burden",
                "CITED_EVIDENCE: doc1,doc2",
            ]
        ),
        artifact_schema="baseline_direct_artifacts/v1",
        artifact_payload={"raw_output": "placeholder"},
        parse_status="valid",
        cited_evidence_ids=["doc1", "doc2"],
        model_provenance={"model": "local_model"},
    )
    normalized = normalizer.normalize(task, agent_result, {})
    assert normalized.payload["parse_status"] == "valid"
    assert normalized.payload["selected_option_id"] == "policy_x"
    assert normalized.payload["preserved_conflict_ids"] == ["cost_burden"]
    assert normalized.unknown_mappings == []


def test_unknown_mapping_is_preserved(task, normalizer) -> None:
    agent_result = AgentResult(
        raw_output_text="\n".join(
            [
                "FINAL_ANSWER: Recommend policy_x while preserving key disagreement.",
                "SELECTED_OPTION: policy_z",
                "REPRESENTED_FRAMES: economic",
                "PRESERVED_CONFLICTS: cost_burden",
                "CITED_EVIDENCE: doc1",
            ]
        ),
        artifact_schema="baseline_direct_artifacts/v1",
        artifact_payload={"raw_output": "placeholder"},
        parse_status="valid",
        cited_evidence_ids=["doc1"],
        model_provenance={"model": "local_model"},
    )
    normalized = normalizer.normalize(task, agent_result, {})
    assert "policy_z" in normalized.unknown_mappings
