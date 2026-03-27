from __future__ import annotations

from dataclasses import dataclass

from decision_space_harness.metrics.common import (
    invalid_parse_result,
    jaccard_similarity,
    tokenize_text,
)
from decision_space_harness.schemas.core import MetricResult, MetricSubject, ProjectionContract


@dataclass
class LexicalJaccardExtensionMetric:
    metric_id: str = "lexical_jaccard_extension"
    metric_version: str = "v1"

    def required_projection_contract(self) -> ProjectionContract:
        return ProjectionContract(source_view="selected_runs", group_by="cell")

    def score_subject(self, subject: MetricSubject, context: dict) -> MetricResult:
        normalized = subject.record["normalized_artifacts"]["payload"]
        if normalized["parse_status"] != "valid":
            return invalid_parse_result(subject, self.metric_id, self.metric_version)

        final_answer_text = normalized["final_answer_text"]
        answer_tokens = tokenize_text(final_answer_text)
        evidence_tokens: list[str] = []
        for item in context["task"].evidence_items:
            evidence_tokens.extend(tokenize_text(item["content"]["text"]))

        return MetricResult(
            subject_type=subject.subject_type,
            subject_id=subject.subject_id,
            metric_id=self.metric_id,
            metric_version=self.metric_version,
            score=jaccard_similarity(answer_tokens, evidence_tokens),
            status="scored",
            diagnostics=[],
            obligation_references=[],
        )
