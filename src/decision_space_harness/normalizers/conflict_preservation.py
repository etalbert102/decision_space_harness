from __future__ import annotations

from dataclasses import dataclass

from decision_space_harness.schemas.core import AgentResult, NormalizedArtifacts, Task


def _parse_csv_field(raw_output: str, prefix: str) -> list[str]:
    for line in raw_output.splitlines():
        if line.startswith(prefix):
            value = line.split(":", 1)[1].strip()
            if not value:
                return []
            return [item.strip() for item in value.split(",") if item.strip()]
    return []


def _parse_scalar_field(raw_output: str, prefix: str) -> str | None:
    for line in raw_output.splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip() or None
    return None


@dataclass
class ConflictPreservationNormalizer:
    name: str = "conflict_preservation_to_benchmark_v1"

    def normalize(self, task: Task, agent_result: AgentResult, run_context: dict) -> NormalizedArtifacts:
        valid_frames = set(task.annotations["relevant_frame_ids"])
        valid_conflicts = set(task.annotations["expected_conflict_ids"])
        valid_options = set(task.annotations["candidate_option_ids"])
        valid_evidence = {item["evidence_id"] for item in task.evidence_items}

        represented_frames = _parse_csv_field(agent_result.raw_output_text, "REPRESENTED_FRAMES")
        preserved_conflicts = _parse_csv_field(agent_result.raw_output_text, "PRESERVED_CONFLICTS")
        cited_evidence_ids = _parse_csv_field(agent_result.raw_output_text, "CITED_EVIDENCE")
        generated_option_ids = _parse_csv_field(agent_result.raw_output_text, "GENERATED_OPTIONS")
        selected_option_id = _parse_scalar_field(agent_result.raw_output_text, "SELECTED_OPTION")
        final_answer_text = _parse_scalar_field(agent_result.raw_output_text, "FINAL_ANSWER")

        unknown_mappings: list[str] = []
        if any(value not in valid_frames for value in represented_frames):
            unknown_mappings.extend(
                [value for value in represented_frames if value not in valid_frames]
            )
        if any(value not in valid_conflicts for value in preserved_conflicts):
            unknown_mappings.extend(
                [value for value in preserved_conflicts if value not in valid_conflicts]
            )
        if selected_option_id and selected_option_id not in valid_options:
            unknown_mappings.append(selected_option_id)
        if any(value not in valid_options for value in generated_option_ids):
            unknown_mappings.extend(
                [value for value in generated_option_ids if value not in valid_options]
            )
        if any(value not in valid_evidence for value in cited_evidence_ids):
            unknown_mappings.extend(
                [value for value in cited_evidence_ids if value not in valid_evidence]
            )

        parse_status = "valid"
        diagnostics: list[str] = []
        if final_answer_text is None or selected_option_id is None:
            parse_status = "invalid"
            diagnostics.append("Missing required final answer or selected option")

        return NormalizedArtifacts(
            schema="decision_space_benchmark_normalized/v1",
            diagnostics=diagnostics,
            unknown_mappings=unknown_mappings,
            payload={
                "represented_frames": [value for value in represented_frames if value in valid_frames],
                "preserved_conflict_ids": [
                    value for value in preserved_conflicts if value in valid_conflicts
                ],
                "generated_option_ids": [
                    value for value in generated_option_ids if value in valid_options
                ]
                or ([selected_option_id] if selected_option_id in valid_options else []),
                "selected_option_id": selected_option_id,
                "final_answer_text": final_answer_text or "",
                "cited_evidence_ids": [
                    value for value in cited_evidence_ids if value in valid_evidence
                ],
                "parse_status": parse_status,
            },
        )
