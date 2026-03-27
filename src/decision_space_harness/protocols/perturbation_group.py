from __future__ import annotations

from dataclasses import dataclass

from decision_space_harness.schemas.core import MetricSubject, ProjectionContract, ValidationResult


@dataclass
class PerturbationGroupProtocol:
    name: str = "perturbation_group/v1"

    def validate_experiment(self, config) -> ValidationResult:
        errors: list[str] = []
        if not config.perturbation_operators:
            errors.append("Perturbation group protocol requires perturbation_operators")
        return ValidationResult(ok=not errors, errors=errors)

    def materialize_subjects(
        self, records: list[dict], projection_spec: ProjectionContract
    ) -> list[MetricSubject]:
        if projection_spec.group_by == "comparison_group":
            grouped_records: dict[str, list[dict]] = {}
            for record in records:
                if projection_spec.source_view == "selected_runs" and not record.get(
                    "eligible_for_metric_scoring", False
                ):
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
            if projection_spec.source_view == "selected_runs" and not record.get(
                "eligible_for_metric_scoring", False
            ):
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
        return ["prompt_template_id", "model", "seed", "comparison_group_id"]

    def declared_semantics(self) -> dict:
        return {
            "study_type": "perturbation_group",
            "unit_of_aggregation": "comparison_group",
        }
