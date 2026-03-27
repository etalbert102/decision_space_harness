from __future__ import annotations

from dataclasses import dataclass

from decision_space_harness.schemas.core import MetricSubject, ProjectionContract, ValidationResult


@dataclass
class SingleRunProtocol:
    name: str = "benchmark_single_run/v1"

    def validate_experiment(self, config) -> ValidationResult:
        errors: list[str] = []
        if len(config.agents) == 0:
            errors.append("Experiment must declare at least one agent")
        return ValidationResult(ok=not errors, errors=errors)

    def materialize_subjects(
        self, records: list[dict], projection_spec: ProjectionContract
    ) -> list[MetricSubject]:
        if projection_spec.group_by == "comparison_group":
            grouped_records: dict[str, list[dict]] = {}
            for record in records:
                if projection_spec.source_view == "selected_runs":
                    if not record.get("eligible_for_metric_scoring", False):
                        continue
                grouped_records.setdefault(record["comparison_group_id"], []).append(record)
            return [
                MetricSubject(
                    subject_type="comparison_group",
                    subject_id=group_id,
                    record={"comparison_group_id": group_id, "members": members},
                )
                for group_id, members in sorted(grouped_records.items())
            ]

        subjects: list[MetricSubject] = []
        for record in records:
            if projection_spec.source_view == "selected_runs":
                if not record.get("eligible_for_metric_scoring", False):
                    continue
            subjects.append(
                MetricSubject(
                    subject_type="selected_run",
                    subject_id=record["cell_id"],
                    record=record,
                )
            )
        return subjects

    def required_provenance(self) -> list[str]:
        return ["prompt_template_id", "model", "seed"]

    def declared_semantics(self) -> dict:
        return {"study_type": "single_run", "unit_of_aggregation": "cell"}
