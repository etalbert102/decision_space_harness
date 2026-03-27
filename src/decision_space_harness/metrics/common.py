from __future__ import annotations

from decision_space_harness.schemas.core import MetricResult, MetricSubject


def invalid_parse_result(
    subject: MetricSubject, metric_id: str, metric_version: str
) -> MetricResult:
    return MetricResult(
        subject_type=subject.subject_type,
        subject_id=subject.subject_id,
        metric_id=metric_id,
        metric_version=metric_version,
        score=None,
        status="unassessable",
        diagnostics=["Normalized parse status is not valid"],
        obligation_references=[],
    )


def jaccard_similarity(left: list[str], right: list[str]) -> float:
    left_set = set(left)
    right_set = set(right)
    union = left_set | right_set
    if not union:
        return 1.0
    return len(left_set & right_set) / len(union)


def tokenize_text(text: str) -> list[str]:
    tokens: list[str] = []
    for raw_token in text.lower().split():
        token = "".join(character for character in raw_token if character.isalnum())
        if token:
            tokens.append(token)
    return tokens
