from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class ValidationResult(BaseModel):
    ok: bool
    errors: list[str] = Field(default_factory=list)
    flags: list[str] = Field(default_factory=list)


class Task(BaseModel):
    task_id: str
    title: str
    task_family: str
    source_type: str
    query: str
    evidence_items: list[dict[str, Any]]
    annotations_schema: str
    annotations: dict[str, Any]
    tags: list[str] = Field(default_factory=list)

    @field_validator("annotations")
    @classmethod
    def _validate_annotations(cls, value: dict[str, Any]) -> dict[str, Any]:
        required = [
            "frames",
            "conflicts",
            "options",
            "relevant_frame_ids",
            "expected_conflict_ids",
            "candidate_option_ids",
        ]
        missing = [field for field in required if field not in value]
        if missing:
            raise ValueError(
                f"Task annotations missing required field(s): {', '.join(missing)}"
            )
        return value

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Task":
        return cls.model_validate(payload)


class ExperimentConfig(BaseModel):
    experiment_id: str
    description: str
    task_set: str
    analysis_label: str = "exploratory"
    target_use: str = "benchmark"
    readiness_target: str = "executable"
    agents: list[str]
    prompt_variants: list[str]
    evidence_providers: list[str]
    perturbation_operators: list[str] = Field(default_factory=list)
    models: list[str]
    metrics: list[str]
    study_protocol: str
    protocol_artifact: str | None = None
    seeds: list[int]
    output_dir: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExperimentConfig":
        return cls.model_validate(payload)


class GenerationConfig(BaseModel):
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int | None = None
    seed: int | None = None
    max_tokens: int = 512
    stop: list[str] | None = None
    format: str | None = None


class ModelResponse(BaseModel):
    text: str
    model: str
    tokens_used: int
    generation_params: dict[str, Any]


class AgentResult(BaseModel):
    raw_output_text: str
    artifact_schema: str
    artifact_payload: dict[str, Any]
    parse_status: str
    cited_evidence_ids: list[str]
    model_provenance: dict[str, Any]
    message_trace: list[dict[str, Any]] = Field(default_factory=list)


class MessageRecord(BaseModel):
    message_id: str
    attempt_id: str
    cell_id: str
    experiment_id: str
    task_id: str
    sender_agent: str
    receiver_agent: str
    message_type: str
    content: str
    parent_message_id: str | None = None
    referenced_evidence_ids: list[str] = Field(default_factory=list)
    referenced_option_ids: list[str] = Field(default_factory=list)
    referenced_conflict_ids: list[str] = Field(default_factory=list)
    correlation_id: str | None = None
    sequence_index: int


class NormalizedArtifacts(BaseModel):
    schema_id: str = Field(alias="schema")
    diagnostics: list[str]
    unknown_mappings: list[str]
    payload: dict[str, Any]


class MetricSubject(BaseModel):
    subject_type: str
    subject_id: str
    record: dict[str, Any]


class ProjectionContract(BaseModel):
    source_view: str
    group_by: str | None = None


class RunSpec(BaseModel):
    experiment_id: str
    task_id: str
    agent_name: str
    prompt_variant: str
    evidence_provider: str
    perturbation_operator: str | None = None
    model_name: str
    seed: int


class MetricResult(BaseModel):
    subject_type: str
    subject_id: str
    metric_id: str
    metric_version: str
    score: float | None
    status: str
    diagnostics: list[str]
    obligation_references: list[str]
