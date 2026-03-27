from __future__ import annotations

from dataclasses import dataclass

from decision_space_harness.metrics.common import invalid_parse_result
from decision_space_harness.schemas.core import MetricResult, MetricSubject, ProjectionContract


@dataclass
class ConflictRetentionMetric:
    metric_id: str = "conflict_retention"
    metric_version: str = "v1"

    def required_projection_contract(self) -> ProjectionContract:
        return ProjectionContract(source_view="selected_runs", group_by="cell")

    def score_subject(self, subject: MetricSubject, context: dict) -> MetricResult:
        task = context["task"]
        expected = task.annotations["expected_conflict_ids"]
        normalized = subject.record["normalized_artifacts"]["payload"]
        if normalized["parse_status"] != "valid":
            return invalid_parse_result(subject, self.metric_id, self.metric_version)
        preserved = normalized["preserved_conflict_ids"]
        denominator = len(expected)
        score = 0.0 if denominator == 0 else len(preserved) / denominator
        return MetricResult(
            subject_type=subject.subject_type,
            subject_id=subject.subject_id,
            metric_id=self.metric_id,
            metric_version=self.metric_version,
            score=score,
            status="scored",
            diagnostics=[],
            obligation_references=[],
        )
