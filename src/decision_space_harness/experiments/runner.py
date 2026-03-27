from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from decision_space_harness.agents.baseline_direct import BaselineDirectAgent
from decision_space_harness.agents.option_generation import OptionGenerationAgent
from decision_space_harness.agents.retrieve_then_synthesize import RetrieveThenSynthesizeAgent
from decision_space_harness.agents.structured_conflict_preserving import (
    StructuredConflictPreservingAgent,
)
from decision_space_harness.artifacts.parse import parse_prefixed_value
from decision_space_harness.evidence.providers import TopKEvidenceProvider
from decision_space_harness.metrics.aggregation import (
    summarize_metric_results,
    write_metric_figure,
    write_summary_table_csv,
)
from decision_space_harness.metrics.conflict_retention import ConflictRetentionMetric
from decision_space_harness.metrics.frame_preservation import FramePreservationMetric
from decision_space_harness.metrics.lexical_jaccard_extension import (
    LexicalJaccardExtensionMetric,
)
from decision_space_harness.metrics.option_breadth import OptionBreadthMetric
from decision_space_harness.metrics.path_dependence import PathDependenceMetric
from decision_space_harness.model_provider.heuristic import HeuristicModelProvider
from decision_space_harness.normalizers.conflict_preservation import (
    ConflictPreservationNormalizer,
)
from decision_space_harness.perturbation_operators.shuffle import ShuffleEvidenceOperator
from decision_space_harness.perturbation_operators.reverse import ReverseEvidenceOperator
from decision_space_harness.protocols.perturbation_group import PerturbationGroupProtocol
from decision_space_harness.protocols.single_run import SingleRunProtocol
from decision_space_harness.registries.simple import RegistrySet
from decision_space_harness.schemas.core import ExperimentConfig, MessageRecord, RunSpec, Task
from decision_space_harness.tasks.loader import load_task_set, validate_task
from decision_space_harness.telemetry.jsonl import (
    load_attempt_records,
    write_attempt_record,
    write_json,
    write_message_record,
    write_selected_run_view,
    write_step_record,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def build_default_registries() -> RegistrySet:
    registries = RegistrySet()
    registries.task_families.register("conflict_preservation", {"version": "v1"})
    registries.evidence_providers.register("top2", TopKEvidenceProvider(name="top2"))
    registries.evidence_providers.register("top1", TopKEvidenceProvider(name="top1"))
    registries.evidence_providers.register("top5", TopKEvidenceProvider(name="top5"))
    registries.study_protocols.register("benchmark_single_run/v1", SingleRunProtocol())
    registries.study_protocols.register("perturbation_group/v1", PerturbationGroupProtocol())
    registries.agents.register("baseline_direct", BaselineDirectAgent())
    registries.agents.register("retrieve_then_synthesize", RetrieveThenSynthesizeAgent())
    registries.agents.register("option_generation", OptionGenerationAgent())
    registries.agents.register(
        "structured_conflict_preserving", StructuredConflictPreservingAgent()
    )
    registries.metrics.register("conflict_retention", ConflictRetentionMetric())
    registries.metrics.register("frame_preservation", FramePreservationMetric())
    registries.metrics.register("option_breadth", OptionBreadthMetric())
    registries.metrics.register("path_dependence", PathDependenceMetric())
    registries.metrics.register(
        "lexical_jaccard_extension", LexicalJaccardExtensionMetric()
    )
    registries.normalizers.register(
        "conflict_preservation_to_benchmark_v1",
        ConflictPreservationNormalizer(),
    )
    registries.perturbation_operators.register("shuffle_evidence/v1", ShuffleEvidenceOperator())
    registries.perturbation_operators.register("reverse_evidence/v1", ReverseEvidenceOperator())
    return registries


def load_experiment(config_path: str | Path) -> ExperimentConfig:
    payload = yaml.safe_load(Path(config_path).read_text())
    return ExperimentConfig.from_dict(payload)


def _build_cell_id(config: ExperimentConfig, task: Task, agent: str, prompt_variant: str, evidence_provider: str, model: str, seed: int) -> str:
    return (
        f"{config.experiment_id}_{task.task_id}_{agent}_{prompt_variant}_"
        f"{evidence_provider}_{model}_seed{seed}"
    )


def expand_grid(config: ExperimentConfig, tasks: list[Task]) -> list[RunSpec]:
    run_specs: list[RunSpec] = []
    operators = config.perturbation_operators or [None]
    for task in tasks:
        for agent_name in config.agents:
            for prompt_variant in config.prompt_variants:
                for evidence_provider in config.evidence_providers:
                    for perturbation_operator in operators:
                        for model_name in config.models:
                            for seed in config.seeds:
                                run_specs.append(
                                    RunSpec(
                                        experiment_id=config.experiment_id,
                                        task_id=task.task_id,
                                        agent_name=agent_name,
                                        prompt_variant=prompt_variant,
                                        evidence_provider=evidence_provider,
                                        perturbation_operator=perturbation_operator,
                                        model_name=model_name,
                                        seed=seed,
                                    )
                                )
    return run_specs


def _build_attempt_record(
    *,
    config: ExperimentConfig,
    task: Task,
    cell_id: str,
    attempt_index: int,
    agent_name: str,
    prompt_variant: str,
    evidence_provider_name: str,
    model_name: str,
    seed: int,
    evidence_bundle: dict,
    agent_result,
    normalized,
    perturbation_operator_name: str | None = None,
) -> dict:
    attempt_id = f"{cell_id}_attempt{attempt_index}"
    normalization_state = (
        "valid" if normalized.payload["parse_status"] == "valid" else "invalid"
    )
    assessable = normalization_state == "valid"
    return {
        "event_id": f"evt_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{attempt_id}",
        "cell_id": cell_id,
        "attempt_id": attempt_id,
        "comparison_group_id": (
            f"{task.task_id}_{agent_name}_{prompt_variant}_{evidence_provider_name}_{model_name}_seed{seed}"
            if perturbation_operator_name
            else task.task_id
        ),
        "case_id": task.task_id,
        "experiment_id": config.experiment_id,
        "task_id": task.task_id,
        "task_family": task.task_family,
        "agent_config": agent_name,
        "prompt_variant": prompt_variant,
        "evidence_provider_config": evidence_provider_name,
        "model": model_name,
        "seed": seed,
        "attempt_index": attempt_index,
        "latency_ms": 0,
        "execution_state": "completed",
        "normalization_state": normalization_state,
        "supersedes_attempt_id": None,
        "error": None,
        "assessability": {
            "status": "assessable" if assessable else "unassessable",
            "reasons": [] if assessable else ["Normalization parse status invalid"],
        },
        "review": {
            "state": "no_new_obligations_created"
            if not normalized.unknown_mappings
            else "obligations_present",
            "obligations": normalized.unknown_mappings,
        },
        "evidence_bundle": {
            "bundle_id": evidence_bundle["bundle_id"],
            "items": [item["evidence_id"] for item in evidence_bundle["items"]],
            "order_sensitive": evidence_bundle["order_sensitive"],
            "permutation_id": evidence_bundle["permutation_id"],
            "base_bundle_id": evidence_bundle["base_bundle_id"],
            "operator_id": evidence_bundle.get("operator_id"),
        },
        "artifacts": {
            "schema": agent_result.artifact_schema,
            "payload": agent_result.artifact_payload,
        },
        "normalized_artifacts": {
            "schema": normalized.schema_id,
            "diagnostics": normalized.diagnostics,
            "unknown_mappings": normalized.unknown_mappings,
            "payload": normalized.payload,
        },
        "provenance": {
            "prompt_template_id": prompt_variant,
            "model": agent_result.model_provenance["model"],
            "generation_params": agent_result.model_provenance["generation_params"],
            "tokens_used": agent_result.model_provenance["tokens_used"],
        },
    }


def _derive_selected_runs(attempts: list[dict]) -> list[dict]:
    by_cell: dict[str, list[dict]] = {}
    for attempt in attempts:
        by_cell.setdefault(attempt["cell_id"], []).append(attempt)
    selected_runs: list[dict] = []
    for cell_attempts in by_cell.values():
        successful = [
            attempt for attempt in cell_attempts if attempt["execution_state"] == "completed"
        ]
        selected = successful[-1] if successful else cell_attempts[-1]
        selected_run = dict(selected)
        selected_run["selected_attempt_id"] = selected["attempt_id"]
        if successful:
            selected_run["selection_role"] = "metric_scoring"
            selected_run["eligible_for_metric_scoring"] = True
        else:
            selected_run["selection_role"] = "failure_accounting"
            selected_run["eligible_for_metric_scoring"] = False
        selected_runs.append(selected_run)
    return sorted(selected_runs, key=lambda record: record["cell_id"])


def _build_message_records(
    *,
    config: ExperimentConfig,
    task: Task,
    cell_id: str,
    attempt_id: str,
    agent_result,
) -> list[dict]:
    message_records: list[dict] = []
    for index, message in enumerate(agent_result.message_trace, start=1):
        message_id = f"{attempt_id}_msg{index}"
        record = MessageRecord(
            message_id=message_id,
            attempt_id=attempt_id,
            cell_id=cell_id,
            experiment_id=config.experiment_id,
            task_id=task.task_id,
            sender_agent=message["sender_agent"],
            receiver_agent=message["receiver_agent"],
            message_type=message["message_type"],
            content=message["content"],
            parent_message_id=message.get("parent_message_id"),
            referenced_evidence_ids=message.get("referenced_evidence_ids", []),
            referenced_option_ids=message.get("referenced_option_ids", []),
            referenced_conflict_ids=message.get("referenced_conflict_ids", []),
            correlation_id=attempt_id,
            sequence_index=index,
        )
        message_records.append(record.model_dump())
    return message_records


def _subject_context(subject, protocol_name: str) -> dict:
    if subject.subject_type == "comparison_group":
        members = subject.record["members"]
        anchor = members[0]
        return {
            "task_id": anchor["task_id"],
            "agent_config": anchor["agent_config"],
            "prompt_variant": anchor["prompt_variant"],
            "evidence_provider_config": anchor["evidence_provider_config"],
            "comparison_group_id": subject.subject_id,
            "study_protocol": protocol_name,
        }
    return {
        "task_id": subject.record["task_id"],
        "agent_config": subject.record["agent_config"],
        "prompt_variant": subject.record["prompt_variant"],
        "evidence_provider_config": subject.record["evidence_provider_config"],
        "comparison_group_id": subject.record["comparison_group_id"],
        "study_protocol": protocol_name,
    }


def execute_experiment(config_path: str | Path) -> dict:
    repo_root = _repo_root()
    config = load_experiment(config_path)
    registries = build_default_registries()
    protocol = registries.study_protocols.get(config.study_protocol)
    validation = protocol.validate_experiment(config)
    if not validation.ok:
        raise ValueError("; ".join(validation.errors))

    task_set_path = repo_root / "data" / "task_sets" / f"{config.task_set}.yaml"
    tasks = load_task_set(task_set_path)
    task_lookup = {task.task_id: task for task in tasks}
    run_specs = expand_grid(config, tasks)
    output_dir = (repo_root / config.output_dir).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    attempts_path = output_dir / "attempts.jsonl"
    runs_path = output_dir / "runs.jsonl"
    metrics_path = output_dir / "metrics.jsonl"
    steps_path = output_dir / "steps.jsonl"
    messages_path = output_dir / "message_records.jsonl"
    summary_table_path = output_dir / "summary_table.json"
    summary_table_csv_path = output_dir / "summary_table.csv"
    figure_path = output_dir / "figures" / "metric_means.txt"

    model_provider = HeuristicModelProvider()
    normalizer = registries.normalizers.get("conflict_preservation_to_benchmark_v1")

    for task in tasks:
        task_validation = validate_task(task)
        if not task_validation.ok:
            raise ValueError("; ".join(task_validation.errors))
    for run_spec in run_specs:
        task = task_lookup[run_spec.task_id]
        cell_id = _build_cell_id(
            config,
            task,
            run_spec.agent_name,
            run_spec.prompt_variant,
            run_spec.evidence_provider,
            run_spec.model_name,
            run_spec.seed,
        )
        if run_spec.perturbation_operator:
            cell_id = f"{cell_id}_{run_spec.perturbation_operator.replace('/', '_')}"
        evidence_provider = registries.evidence_providers.get(run_spec.evidence_provider)
        evidence_bundle = evidence_provider.get_base_evidence(
            task, run_spec.evidence_provider, run_spec.seed
        )
        if run_spec.perturbation_operator:
            operator = registries.perturbation_operators.get(run_spec.perturbation_operator)
            evidence_bundle = operator.apply(
                task, evidence_bundle, run_spec.perturbation_operator, run_spec.seed
            )
        write_step_record(
            {
                "cell_id": cell_id,
                "task_id": task.task_id,
                "boundary": "input",
                "status": "ok",
            },
            steps_path,
        )
        write_step_record(
            {
                "cell_id": cell_id,
                "task_id": task.task_id,
                "boundary": "divergence",
                "bundle_id": evidence_bundle["bundle_id"],
                "evidence_ids": [item["evidence_id"] for item in evidence_bundle["items"]],
                "perturbation_operator": run_spec.perturbation_operator,
            },
            steps_path,
        )
        agent = registries.agents.get(run_spec.agent_name)
        agent_result = agent.run_agent(
            task=task,
            evidence_bundle=evidence_bundle,
            prompt_variant=run_spec.prompt_variant,
            model_name=run_spec.model_name,
            seed=run_spec.seed,
            model_provider=model_provider,
        )
        write_step_record(
            {
                "cell_id": cell_id,
                "task_id": task.task_id,
                "boundary": "commit",
                "selected_option_id": parse_prefixed_value(
                    agent_result.raw_output_text, "SELECTED_OPTION"
                ),
            },
            steps_path,
        )
        normalized = normalizer.normalize(task, agent_result, {})
        attempt_record = _build_attempt_record(
            config=config,
            task=task,
            cell_id=cell_id,
            attempt_index=1,
            agent_name=run_spec.agent_name,
            prompt_variant=run_spec.prompt_variant,
            evidence_provider_name=run_spec.evidence_provider,
            model_name=run_spec.model_name,
            seed=run_spec.seed,
            evidence_bundle=evidence_bundle,
            agent_result=agent_result,
            normalized=normalized,
            perturbation_operator_name=run_spec.perturbation_operator,
        )
        write_attempt_record(attempt_record, attempts_path)
        for message_record in _build_message_records(
            config=config,
            task=task,
            cell_id=cell_id,
            attempt_id=attempt_record["attempt_id"],
            agent_result=agent_result,
        ):
            write_message_record(message_record, messages_path)
        write_step_record(
            {
                "cell_id": cell_id,
                "task_id": task.task_id,
                "boundary": "attempt_summary",
                "execution_state": attempt_record["execution_state"],
                "normalization_state": attempt_record["normalization_state"],
                "assessability_status": attempt_record["assessability"]["status"],
            },
            steps_path,
        )

    attempts = load_attempt_records(attempts_path)
    selected_runs = _derive_selected_runs(attempts)
    for selected_run in selected_runs:
        write_selected_run_view(selected_run, runs_path)

    metric_results: list[dict] = []
    for metric_name in config.metrics:
        metric = registries.metrics.get(metric_name)
        projection = metric.required_projection_contract()
        subjects = protocol.materialize_subjects(selected_runs, projection)
        for subject in subjects:
            task_id = (
                subject.record["task_id"]
                if subject.subject_type != "comparison_group"
                else subject.record["members"][0]["task_id"]
            )
            task = task_lookup[task_id]
            result = metric.score_subject(subject, {"task": task})
            result_row = result.model_dump()
            result_row.update(_subject_context(subject, config.study_protocol))
            metric_results.append(result_row)
            write_selected_run_view(result_row, metrics_path)

    summary_table = summarize_metric_results(metric_results)
    write_json(summary_table_path, summary_table)
    write_summary_table_csv(summary_table_csv_path, summary_table)
    write_metric_figure(figure_path, summary_table)

    summary = {
        "experiment_id": config.experiment_id,
        "attempt_count": len(attempts),
        "selected_run_count": len(selected_runs),
        "metric_result_count": len(metric_results),
        "summary_table_path": str(summary_table_path.relative_to(repo_root)),
        "figure_path": str(figure_path.relative_to(repo_root)),
        "message_record_count": len(
            [
                line
                for line in messages_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        )
        if messages_path.exists()
        else 0,
        "readiness": {
            "executable": True,
            "reproducible": True,
            "scientifically_interpretable": "not_evaluated",
        },
    }
    write_json(output_dir / "summary.json", summary)
    write_step_record(
        {
            "experiment_id": config.experiment_id,
            "boundary": "summary",
            "attempt_count": len(attempts),
            "metric_result_count": len(metric_results),
        },
        steps_path,
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Usage: python -m decision_space_harness.experiments.runner <config_path>")
        return 1
    execute_experiment(args[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
