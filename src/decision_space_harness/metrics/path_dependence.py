from __future__ import annotations

from dataclasses import dataclass

from decision_space_harness.metrics.common import jaccard_similarity
from decision_space_harness.schemas.core import MetricResult, MetricSubject, ProjectionContract


def _pairwise_average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


@dataclass
class PathDependenceMetric:
    metric_id: str = "path_dependence"
    metric_version: str = "v1"

    def required_projection_contract(self) -> ProjectionContract:
        return ProjectionContract(source_view="selected_runs", group_by="comparison_group")

    def score_subject(self, subject: MetricSubject, context: dict) -> MetricResult:
        members = subject.record["members"]
        valid_members = [
            member
            for member in members
            if member["normalized_artifacts"]["payload"]["parse_status"] == "valid"
            and member.get("eligible_for_metric_scoring", False)
        ]
        if len(valid_members) < 2:
            return MetricResult(
                subject_type=subject.subject_type,
                subject_id=subject.subject_id,
                metric_id=self.metric_id,
                metric_version=self.metric_version,
                score=None,
                status="unassessable",
                diagnostics=["Comparison group has fewer than two valid members"],
                obligation_references=[],
            )

        pair_scores: list[float] = []
        for index, left in enumerate(valid_members):
            left_payload = left["normalized_artifacts"]["payload"]
            for right in valid_members[index + 1 :]:
                right_payload = right["normalized_artifacts"]["payload"]
                frame_score = jaccard_similarity(
                    left_payload["represented_frames"],
                    right_payload["represented_frames"],
                )
                conflict_score = jaccard_similarity(
                    left_payload["preserved_conflict_ids"],
                    right_payload["preserved_conflict_ids"],
                )
                option_score = jaccard_similarity(
                    left_payload["generated_option_ids"],
                    right_payload["generated_option_ids"],
                )
                selection_score = (
                    1.0
                    if left_payload["selected_option_id"] == right_payload["selected_option_id"]
                    else 0.0
                )
                consistency = _pairwise_average(
                    [frame_score, conflict_score, option_score, selection_score]
                )
                pair_scores.append(1.0 - consistency)

        return MetricResult(
            subject_type=subject.subject_type,
            subject_id=subject.subject_id,
            metric_id=self.metric_id,
            metric_version=self.metric_version,
            score=_pairwise_average(pair_scores),
            status="scored",
            diagnostics=[f"group_member_count={len(valid_members)}"],
            obligation_references=[],
        )
