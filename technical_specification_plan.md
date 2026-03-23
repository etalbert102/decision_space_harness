# DecisionSpace Harness Technical Specification Plan

## 1. Purpose

DecisionSpace Harness is a reusable evaluation and experimentation platform for measuring how LLM-agent pipelines compress, preserve, or reshape the space of interpretations and actions available during evidence synthesis. The system is designed to support benchmark-style comparisons, prompt and evidence sweeps, and repeatable empirical studies across the broader decision-space research area.

The primary claim supported by the initial benchmark slice is narrower:

The harness can measure whether structured, conflict-preserving agent workflows retain more disagreement, frame diversity, and candidate actions than answer-first synthesis pipelines under declared benchmark conditions.

The broader platform goal is stronger:

The harness should function as modular research infrastructure for decision-space experiments, so new task families, evidence providers, metrics, and agent modules can be added without rewriting core orchestration code.

This document converts the concept brief in `specification.md` into an implementation-ready technical plan for the v1 harness core, while also identifying post-v1 scientific extension points.

The plan also draws on the visibility-first principles in `/home/etalbert102/fidelity_framework`, especially:

1. make important judgment structure visible rather than implicit
2. place explicit anchors at meaningful boundaries
3. treat assessment outputs as review inputs, not approvals
4. preserve trace integrity so results remain assessable
5. use transcripts and fixtures to guard known critical paths without overstating coverage

## 2. Goals

### 2.1 Primary Goals

1. Build a reproducible harness for running multiple agent pipelines over a shared task suite.
2. Log intermediate reasoning artifacts and evidence choices in a machine-readable telemetry format.
3. Compute interpretable structural metrics that capture decision-space compression.
4. Support experiment definition through configuration rather than code changes.
5. Produce outputs suitable for benchmarking, reporting, and future research reuse.
6. Ensure new decision-space task families, metrics, evidence providers, and agent modules can be added with minimal or no changes to existing modules.
7. Define a strict normalization boundary so heterogeneous agent outputs can be scored consistently.

### 2.2 Non-Goals

1. Building a production UI or web service.
2. Supporting a large model matrix or large-scale distributed execution in v1.
3. Optimizing for maximum benchmark throughput in the first version.
4. Creating open-ended autonomous agents with arbitrary tool chains outside the experiment contract.
5. Measuring generic model accuracy as the primary system outcome.
6. Claiming that successful execution, metric computation, or assessment implies approval, safety, authority verification, or completeness.

## 3. Success Criteria

The initial version is successful if it satisfies all of the following:

1. A user can run one command to execute a named experiment configuration end to end.
2. The harness supports four initial agent configurations:
   direct synthesis, retrieve-then-synthesize, option-generation, structured conflict-preserving.
3. The task suite contains at least:
   12 synthetic tasks and 5 real-document tasks in phase 1,
   expanding to 40 to 50 total tasks by phase 2.
4. Each run emits structured JSONL telemetry with stable run metadata and extensible artifact payloads.
5. The system computes:
   conflict retention, frame preservation, option breadth, and path dependence.
6. The harness can detect and report structural differences when they exist on fixture tasks with known expected relationships.
7. Another researcher can clone the repository, install dependencies, and reproduce a documented demo run.
8. A new decision-space task family or metric module can be added through registration and configuration without modifying the experiment runner.
9. The v1 specification defines stable run identity, retry semantics, and comparison-group semantics for perturbation studies.

## 4. Research Questions

The platform must support the following research questions:

1. Do answer-first pipelines smooth over legitimate disagreement in evidence?
2. Do synthesis pipelines collapse multi-frame evidence into a narrower interpretive schema?
3. How sensitive are outputs to evidence ordering, evidence depth, and prompt framing?
4. Do structured agent workflows preserve a broader candidate action space than standard RAG baselines?
5. Which pipeline choices materially improve structural robustness without requiring model changes?
6. What other structural decision-space properties can be studied once the harness supports new task families and metrics?

## 5. System Scope

### 5.1 In Scope

1. Task definition and storage.
2. Evidence bundle generation and perturbation.
3. Agent pipeline execution over controlled inputs.
4. Telemetry collection for intermediate and final outputs.
5. Metric computation from task metadata and run artifacts.
6. Experiment configuration, expansion, execution, and aggregation.
7. Export of results for analysis and report generation.
8. Pluggable extension points for broader decision-space experiments.

### 5.2 Out of Scope

1. Human-in-the-loop annotation tooling in v1.
2. Online retrieval from live web sources during evaluation by default.
3. Fine-tuning or model training.
4. Real-time serving infrastructure.
5. Full interactive dashboards in v1.

## 6. Conceptual Architecture

The runtime flow is:

Task Set
-> Experiment Configuration
-> Run Grid Expansion
-> Evidence Provider / Bundle Selection
-> Agent Pipeline Execution
-> Telemetry Logging
-> Metric Scoring
-> Aggregation and Reporting

Following the fidelity-framework doctrine, the runtime should make judgment structure visible at explicit boundaries rather than burying it inside opaque orchestration. For this harness, the default execution boundaries are:

1. input boundary: task, config, and evidence validation
2. divergence boundary: evidence permutation, branching, option generation, or other expansion of the decision space
3. commit boundary: final answer selection, artifact finalization, and persisted run record emission
4. summary boundary: experiment-level aggregation, diagnostics, and obligation reporting

This architecture separates six concerns:

1. task semantics
2. experimental design
3. evidence provisioning
4. pipeline behavior
5. measurement logic
6. result presentation

The architecture must treat the following as replaceable modules rather than fixed benchmark components:

1. task families
2. annotation schemas
3. evidence providers
4. agent pipelines
5. artifact schemas
6. metric modules
7. aggregators
8. reporters
9. perturbation operators
10. study protocols

## 7. Functional Requirements

### 7.1 Task Layer

The system must:

1. Load task definitions from version-controlled files.
2. Support synthetic tasks and real-document tasks under a unified base schema.
3. Store evidence documents and family-specific annotations with each task.
4. Support task filtering by task family, source type, and experiment tags.
5. Validate task files before execution.
6. Support family-specific annotation payloads without requiring changes to the base task schema.
7. Allow new decision-space task families to be registered independently of existing task families.

### 7.2 Evidence Layer

The system must:

1. Support no-evidence and evidence-enabled pipelines.
2. Support multiple evidence provider types, including local document bundles, precomputed retrieval outputs, and future provider modules.
3. Select evidence bundles according to named provider configurations such as `top5` and `top10`.
4. Support deterministic evidence ordering and seeded permutations for path-dependence experiments.
5. Record exactly which evidence items were selected and in what order.
6. Allow new evidence providers to be added without modifying the experiment runner.
7. Emit stable bundle identifiers and permutation metadata so perturbation studies can be grouped deterministically.

### 7.3 Agent Layer

The system must:

1. Support four initial agent configurations.
2. Accept standardized run inputs regardless of underlying prompting strategy.
3. Emit artifacts through a common envelope with task-family-specific payloads when applicable.
4. Allow prompt variants to be swapped without code changes.
5. Fail gracefully when an agent output is malformed.
6. Allow new agent modules to declare capabilities and artifact contracts without changing existing agent modules.
7. Emit either required normalized scoring fields directly or the raw fields required by a registered normalizer.

### 7.4 Experiment Layer

The system must:

1. Treat experiments as named, versioned configuration objects.
2. Expand configuration grids across tasks, agents, prompts, evidence providers, models, metrics, and seeds.
3. Allow experiment-specific metric selection.
4. Support rerunning failed cells without rerunning the full experiment.
5. Produce an experiment summary artifact after completion.
6. Resolve named modules through registries rather than hard-coded conditionals in the runner.
7. Treat run cell identity, attempt identity, and perturbation comparison groups as first-class execution concepts.
8. Emit explicit boundary events or equivalent step records for input, divergence, commit, and summary stages.

### 7.5 Telemetry Layer

The system must:

1. Log one JSON object per run step or one normalized object per completed run, depending on the selected mode.
2. Include enough information to recompute metrics offline.
3. Preserve raw model outputs when permitted by configuration.
4. Track timing, seeds, errors, and retries.
5. Store outputs in a stable directory structure for later aggregation.
6. Separate stable run envelope fields from extensible artifact payloads so new modules do not require schema churn.
7. Preserve superseded attempts rather than overwriting them, while making the aggregate-selected attempt unambiguous for aggregation.
8. Mark runs or experiments unassessable when trace integrity required for comparison or scoring is missing.

### 7.6 Metrics Layer

The system must:

1. Compute metrics deterministically from task metadata and telemetry.
2. Distinguish between missing data, zero scores, and invalid runs.
3. Support per-run, per-task-family, and per-experiment aggregation.
4. Expose both scalar scores and supporting diagnostic counts.
5. Allow new metric modules to be registered independently and bound to specific task families or artifact types.
6. Validate that required normalized fields and comparison-group structure are present before scoring.
7. Produce obligations and diagnostics for human review when assessability or compatibility conditions fail.

## 8. Non-Functional Requirements

1. Reproducibility: runs must be seedable and configuration-driven.
2. Inspectability: all important intermediate artifacts must be observable in logs.
3. Modularity: new experiments and most new decision-space modules should require configuration changes and registration, not edits to core orchestration code.
4. Simplicity: the v1 implementation should remain understandable by a single researcher.
5. Portability: the harness should run on a standard local development machine.
6. Extensibility: new metrics, tasks, evidence providers, and agent types must fit existing interfaces.
7. Backward compatibility: adding a new task family or metric should not break existing experiment configs or historical artifacts.
8. Honesty of claims: the harness must distinguish visibility, reproducibility, and scientific interpretability rather than collapsing them into a single pass state.

## 9. Repository Structure

Recommended repository layout:

```text
decision-space-harness/
  README.md
  pyproject.toml
  configs/
    registries/
    models/
    prompts/
    evidence_providers/
    artifact_schemas/
    perturbation_operators/
    study_protocols/
  data/
    tasks/
      synthetic/
      real/
    task_sets/
  experiments/
    configs/
    runner.py
  outputs/
    runs/
    experiments/
    reports/
  src/
    decision_space_harness/
      agents/
      artifacts/
      evidence/
      experiments/
      metrics/
      registries/
      runners/
      schemas/
      tasks/
      telemetry/
      utils/
  tests/
    unit/
    integration/
    fixtures/
  reports/
  notebooks/
```

## 10. Data Model

### 10.1 Task Schema

The task layer should use a two-part schema:

1. a stable `BaseTask` envelope shared by all task families
2. a family-specific annotation payload defined by the registered task family

This prevents the base schema from being rewritten every time a new decision-space task type is added.

Each task should be represented as a JSON or YAML document with the following required base fields:

```json
{
  "task_id": "policy_04",
  "title": "Industrial emissions regulation tradeoff",
  "task_family": "conflict_preservation",
  "source_type": "synthetic",
  "query": "What policy approach should a regulator take?",
  "evidence_items": [
    {
      "evidence_id": "doc1",
      "kind": "document",
      "title": "Economic analysis in favor of policy X",
      "content": {
        "text": "..."
      },
      "provenance": {
        "source_title": "Synthetic economic brief",
        "publication_date": null,
        "citation": "Synthetic source"
      }
    }
  ],
  "annotations_schema": "conflict_preservation/v1",
  "annotations": {
    "frames": [
      {"frame_id": "legal", "label": "Legal"},
      {"frame_id": "economic", "label": "Economic"},
      {"frame_id": "operational", "label": "Operational"}
    ],
    "conflicts": [
      {
        "conflict_id": "cost_burden",
        "label": "Cost burden disagreement",
        "evidence_ids": ["doc1", "doc3"]
      },
      {
        "conflict_id": "implementation_timeline",
        "label": "Implementation timeline disagreement",
        "evidence_ids": ["doc2", "doc4"]
      }
    ],
    "options": [
      {"option_id": "policy_x", "label": "Policy X"},
      {"option_id": "policy_y", "label": "Policy Y"},
      {"option_id": "hybrid_option", "label": "Hybrid option"}
    ],
    "relevant_frame_ids": ["legal", "economic", "operational"],
    "minority_frame_ids": ["legal"],
    "expected_conflict_ids": [
      "cost_burden",
      "implementation_timeline"
    ],
    "candidate_option_ids": ["policy_x", "policy_y", "hybrid_option"]
  },
  "tags": ["benchmark_v1", "high_conflict"]
}
```

### 10.2 Task Schema Requirements

1. `task_id` must be unique.
2. `task_family` must resolve through the task-family registry.
3. `evidence_items` must contain stable `evidence_id` values.
4. The base task schema must only require fields shared across all task families.
5. Family-specific annotations must be validated by the annotation schema associated with `task_family` and `annotations_schema`.
6. Task families may define additional required fields inside `annotations` without affecting other task families.
7. Real-document tasks must include provenance metadata such as source title, publication date, and citation string.
8. Task families that use frames, conflicts, options, or other scored entities must declare them as identifier-bearing objects in annotations rather than raw strings.
9. The base task envelope must permit non-document evidence kinds so future task families can attach structured state, constraints, graphs, or counterfactual metadata without schema breaks.

### 10.3 Minimal Shared Ontology for v1

To make normalized artifacts comparable across agents and task families, v1 must define a minimal shared ontology at the task level rather than leaving identifier semantics entirely to post-v1 protocol layers.

The minimum shared identifiers are:

1. `evidence_id`: stable identifier for an evidence item in `evidence_items`
2. `frame_id`: stable identifier for an analytical frame named in task annotations
3. `conflict_id`: stable identifier for a conflict point or disagreement relation named in task annotations
4. `option_id`: stable identifier for a candidate action or decision option named in task annotations

The v1 normalization contract must require:

1. normalized artifact identifiers map to task-defined identifiers when such identifiers exist
2. unmappable values use explicit null or unknown states rather than free-text pseudo-identifiers
3. metric modules score only over declared identifiers or declared null or unknown states according to their compatibility rules
4. task families define how `frame_id`, `conflict_id`, and `option_id` are instantiated in their annotations when those constructs are used
5. any scored entity introduced by a future task family must have the same identifier-bearing shape: stable id, human-readable label, and optional family-specific metadata

### 10.4 Task Family Examples

The initial harness should support at least the following registered task families:

1. `conflict_preservation`
2. `frame_diversity`
3. `option_space`

Path dependence should be treated in v1 as a perturbation-based study pattern and metric applicable to compatible task families, not as a standalone task family.

Future decision-space families should be addable through new annotation schemas, metrics, and configs, for example:

1. uncertainty preservation
2. source attribution fidelity
3. causal alternative generation
4. policy tradeoff articulation
5. deliberative ranking stability

### 10.5 Experiment Schema

Each experiment config should define the evaluation slice and execution grid:

```yaml
experiment_id: conflict_smoothing_v1
description: Compare baseline and structured agents on disagreement retention.
task_set: conflict_tasks_v1
agents:
  - baseline_direct
  - structured_conflict_preserving
prompt_variants:
  - default
  - disagreement_preserving
evidence_providers:
  - top5
  - top10
models:
  - local_model
metrics:
  - conflict_retention
  - option_breadth
study_protocol: benchmark_single_run/v1
seeds:
  - 11
  - 22
output_dir: outputs/experiments/conflict_smoothing_v1
```

Experiment configs should also support optional module overrides:

1. task-family-specific validators
2. artifact schema selection
3. aggregation strategy
4. reporter selection
5. normalizer selection
6. perturbation operator selection
7. study protocol selection

Override resolution must be deterministic. For v1, module selection precedence should be:

`explicit cell override < experiment override < task-family default < registry default`

Where more than one compatible module remains after precedence is applied, the configuration should be rejected rather than resolved by import order or registry iteration order.

For v1, the expanded run grid should produce a stable logical execution unit called a `cell`.

Each `cell` is the unique combination of:

1. task or case identifier
2. agent configuration
3. prompt variant
4. evidence provider configuration
5. model
6. seed
7. perturbation operator and perturbation instance, when applicable

Each execution attempt of a cell should receive a separate `attempt_id`.

For v1, retry and aggregation semantics should be deterministic:

1. every retry appends a new attempt rather than resuming an incomplete attempt in place
2. attempt status values should include a fixed terminal set such as `completed`, `failed`, and `invalid`
3. aggregation should use the latest successful attempt for a cell when any successful attempt exists
4. if no successful attempt exists, aggregation should use the latest terminal non-success attempt only for failure accounting, not as a substitute successful score
5. superseded attempts must remain preserved in telemetry
6. the aggregate-selected attempt for each cell must be explicit in persisted outputs

### 10.6 Telemetry Schema

Telemetry should use a stable envelope plus an extensible artifact payload. The stable envelope supports aggregation and reproducibility; the artifact payload supports modular expansion.

Telemetry should also distinguish among:

1. `cell_id`: stable identifier for the logical run cell
2. `attempt_id`: identifier for one execution attempt of that cell
3. `comparison_group_id`: identifier tying together runs that must be compared to compute a perturbation-based metric
4. `case_id`: optional identifier for paired, blocked, or repeated observations that share a unit of analysis

Where step-level logging is enabled, telemetry should treat step records as judgment anchors at the harness boundaries:

1. `input`
2. `divergence`
3. `commit`
4. `summary`

These records are visibility artifacts. They do not certify correctness, authority, or completeness.

Each completed run should emit a normalized record similar to:

```json
{
  "run_id": "20260323_conflict_smoothing_v1_policy_04_baseline_direct_top5_seed11",
  "cell_id": "conflict_smoothing_v1_policy_04_baseline_direct_default_top5_local_model_seed11",
  "attempt_id": "conflict_smoothing_v1_policy_04_baseline_direct_default_top5_local_model_seed11_attempt1",
  "comparison_group_id": "policy_04_top5_seed11_shuffle_group_a",
  "case_id": "policy_04",
  "experiment_id": "conflict_smoothing_v1",
  "task_id": "policy_04",
  "task_family": "conflict_preservation",
  "agent_config": "baseline_direct",
  "prompt_variant": "default",
  "evidence_provider_config": "top5",
  "model": "local_model",
  "seed": 11,
  "attempt_index": 1,
  "latency_ms": 4812,
  "status": "completed",
  "supersedes_attempt_id": null,
  "error": null,
  "assessability": {
    "status": "assessable",
    "reasons": []
  },
  "evidence_bundle": {
    "bundle_id": "policy_04_top5_seed11",
    "items": ["doc3", "doc1", "doc2", "doc4"],
    "order_sensitive": true,
    "permutation_id": "shuffle_00",
    "base_bundle_id": "policy_04_top5_seed11_base"
  },
  "artifacts": {
    "schema": "conflict_preservation_artifacts/v1",
    "payload": {
      "retrieved_frames": ["economic", "legal"],
      "source_conflict_count": 2,
      "generated_frames": ["economic"],
      "generated_options": ["policy_x"],
      "selected_option": "policy_x",
      "final_answer": "...",
      "conflicts_preserved": 1,
      "minority_frame_survived": false
    }
  },
  "normalized_artifacts": {
    "schema": "decision_space_core_normalized/v1",
    "payload": {
      "represented_frames": ["economic"],
      "preserved_conflict_ids": ["cost_burden"],
      "generated_option_ids": ["policy_x"],
      "selected_option_id": "policy_x",
      "final_answer_text": "...",
      "cited_evidence_ids": ["doc1", "doc3"],
      "parse_status": "valid"
    }
  }
}
```

The telemetry schema must permit other artifact payloads without changing the top-level envelope.

For v1, metrics should score against `normalized_artifacts`, not agent-specific raw payloads. Agents may emit richer task-family-specific artifacts, but every benchmarked run must end with a normalized scoring payload produced either:

1. directly by the agent, or
2. by a registered postprocessor or normalizer applied after agent execution

If normalization fails, the run should be marked invalid for metrics that depend on the missing fields, while still preserving the raw artifacts for inspection.

The v1 normalization layer must also preserve explicit unknown states. A normalizer must not invent task-independent identifiers merely to satisfy the scoring schema.

To preserve future extensibility, the normalization boundary should distinguish between:

1. a stable core normalized envelope used by the runner, telemetry, and generic aggregation
2. one or more normalized views or subject projections consumed by metrics

The stable core normalized envelope should contain:

1. `schema`
2. `parse_status`
3. `entities`: typed identifier-bearing observations such as frames, conflicts, options, sources, rankings, uncertainties, or other declared task-family entities
4. `relations`: typed links among entities when the task family requires them
5. `final_text_fields`: named human-readable synthesis outputs
6. `provenance_links`: evidence and lineage references recoverable from the run
7. `unknown_mappings`: explicit records of unmappable values
8. `extensions`: family-specific normalized payloads that remain outside the core shared fields

The benchmark-specific fields such as `represented_frames`, `preserved_conflict_ids`, `generated_option_ids`, and `selected_option_id` should be treated as the v1 benchmark normalized view derived from the core envelope, not as the only future-proof normalization contract.

### 10.7 Provenance and Compatibility Metadata

To keep extension behavior machine-checkable rather than implicit, every persisted run and every registry entry should expose enough metadata for compatibility validation.

Minimum compatibility-relevant persisted metadata should include:

1. task family id and version
2. annotation schema id and version
3. artifact schema id and version
4. normalized schema id and version
5. evidence provider id and version
6. perturbation operator id and version when applicable
7. study protocol id and version when applicable
8. metric ids and versions used for scoring

The runner should validate these metadata against declared module capabilities before execution and again before scoring grouped metrics.

If trace integrity fails, such as missing correlation across grouped runs or missing bundle lineage for perturbation comparisons, the relevant metric computation should become `unassessable` rather than silently degrading to a numeric score.

### 10.8 Assessment Status and Obligations

Following the fidelity-framework model, harness assessment outputs should create review obligations rather than approval states.

Recommended assessment statuses:

1. `unassessable`: trace integrity, compatibility, or required artifacts are missing
2. `obligations_present`: the run or experiment completed, but review-worthy issues were detected
3. `no_new_obligations_created`: no new issues were detected relative to the configured checks

These statuses do not imply:

1. approval
2. safety
3. correctness
4. authority verification
5. complete coverage

Typical obligation sources include:

1. missing normalization fields
2. parse failures
3. missing comparison-group peers
4. missing provenance metadata
5. unsupported metric-task-family combinations
6. absent evidence lineage for perturbation studies

These states should be modeled as separate axes rather than overloaded flags:

1. execution state: `completed`, `failed`, `invalid`
2. assessability state: `assessable`, `unassessable`
3. review state: `no_new_obligations_created`, `obligations_present`

The runner, metrics layer, and reporters should consume these axes independently so future modules do not need to reinterpret the meaning of `invalid`, `failed`, or `unassessable`.

## 11. Registry and Plugin Model

The harness should use explicit registries so new modules can be added without modifying the runner.

### 11.1 Required Registries

1. task family registry
2. annotation schema registry
3. evidence provider registry
4. agent registry
5. normalizer registry
6. artifact schema registry
7. metric registry
8. aggregation registry
9. reporter registry
10. perturbation operator registry
11. study protocol registry

Each registry entry should define:

1. module identifier
2. version
3. implementation path
4. accepted input schema
5. emitted artifact schema
6. compatibility constraints
7. version compatibility policy
8. required provenance fields
9. grouping requirements when the module consumes grouped observations

Registry compatibility should be machine-checkable. A module should be selectable only when its declared requirements are satisfied by the task family, normalized schema, study protocol, and run grouping available in the experiment definition.

Plugin loading should also be a documented contract, not an implicit import convention. For v1, each registry entry should declare:

1. loader kind such as `python_import`, `entry_point`, or `config_builtin`
2. implementation reference in the format required by that loader kind
3. constructor or factory symbol when applicable
4. whether the module is pure configuration, stateless code, or stateful runtime code

Module loading failures should surface as configuration or startup errors before run execution begins.

### 11.2 Extension Principle

A new decision-space module should be addable by:

1. implementing the module against a declared interface
2. registering it in configuration
3. referencing it in an experiment config

Core orchestration code should not need to change unless the extension introduces an entirely new execution primitive.

## 12. Module Design

### 12.1 `tasks`

Responsibilities:

1. Load and validate task files.
2. Resolve task sets into concrete task lists.
3. Provide typed task objects to downstream components.
4. Dispatch family-specific annotation validation through the registry.

Interfaces:

1. `load_task(task_path) -> Task`
2. `load_task_set(task_set_id) -> list[Task]`
3. `validate_task(task) -> ValidationResult`

### 12.2 `evidence`

Responsibilities:

1. Build evidence bundles from task evidence items or other registered evidence sources.
2. Build a base bundle before any registered perturbation is applied.
3. Apply provider-specific selection logic only.
4. Return ordered evidence bundles with metadata.

Interfaces:

1. `get_base_evidence(task, provider_config, seed) -> EvidenceBundle`

The evidence layer should not own experimental perturbation semantics beyond producing a base bundle and stable lineage metadata.

### 12.3 `perturbation_operators`

Responsibilities:

1. Transform a base evidence bundle or other task-linked inputs under a declared experimental operator.
2. Preserve lineage metadata linking the derived bundle back to its base bundle and operator instance.
3. Declare what properties the operator is intended to preserve and what dimensions it changes.

Interfaces:

1. `apply(task, base_bundle, operator_config, seed) -> PerturbedInput`
2. `describe_constraints() -> PerturbationConstraints`

### 12.4 `agents`

Responsibilities:

1. Transform task plus evidence inputs into agent-specific prompts.
2. Execute model calls or local inference.
3. Parse outputs into a common artifact envelope with schema-specific payloads.
4. Hand off raw artifacts to a registered normalizer when the agent does not emit the benchmark scoring schema directly.

Interfaces:

1. `run_agent(run_context) -> AgentResult`
2. `parse_output(raw_output) -> AgentArtifacts`
3. `describe_capabilities() -> AgentCapabilities`

Minimum `AgentResult` contract for v1:

1. raw model output
2. task-family-specific artifact payload
3. parse status
4. cited evidence identifiers when available
5. enough structured fields to support registered normalization

Planned agent implementations:

1. `baseline_direct`
2. `retrieve_then_synthesize`
3. `option_generation`
4. `structured_conflict_preserving`

### 12.5 `metrics`

Responsibilities:

1. Score completed runs using task annotations and telemetry.
2. Return scalar metrics and diagnostic details.
3. Declare which task families and artifact schemas each metric supports.
4. Declare the comparison unit required for scoring, such as single run, repeated-run case, or perturbation group.

Interfaces:

1. `score_subject(subject, context) -> MetricResult`
2. `score_projection() -> ProjectionSpec`
3. `aggregate_results(metric_results) -> AggregateResult`
4. `supports(task_family, artifact_schema, study_protocol) -> bool`
5. `required_projection_contract() -> ProjectionContract`

`MetricSubject` is the unit consumed by a metric after protocol-defined materialization. For some metrics it is one run; for others it is a perturbation group, repeated-run case, paired counterfactual block, or other protocol-defined comparison unit.

Metrics should not own raw record grouping logic. A metric may declare the projection contract it requires, but study protocols should be the single owner of how persisted records are grouped and materialized into admissible `MetricSubject` instances.

### 12.6 `normalizers`

Responsibilities:

1. Convert agent-specific artifacts into a stable normalized scoring schema.
2. Apply task-family-aware normalization rules without pushing benchmark logic into the core runner.
3. Mark normalization failures explicitly and preserve diagnostics.

Interfaces:

1. `normalize(task, agent_result, run_context) -> NormalizedArtifacts`
2. `supports(task_family, agent_config, artifact_schema) -> bool`

### 12.7 `study_protocols`

Responsibilities:

1. Define the unit of analysis, grouping rules, rerun policy, and required controls for an experiment class.
2. Validate that an execution config satisfies protocol-specific requirements before runs are expanded.
3. Supply grouping and aggregation hints to metrics and reporting modules.

Interfaces:

1. `validate_experiment(config) -> ValidationResult`
2. `materialize_subjects(records, projection_spec) -> list[MetricSubject]`
3. `required_provenance() -> list[str]`

Study protocols should be the sole authority for:

1. grouping persisted records into comparison units
2. validating grouped-subject completeness
3. deriving `comparison_group_id`, `case_id`, and related correlation metadata semantics
4. rejecting inadmissible partial groups before metric scoring begins

This keeps grouped metrics extensible without pushing protocol-specific branching back into the experiment runner or metric implementations.

### 12.8 `telemetry`

Responsibilities:

1. Normalize runtime artifacts into stable JSONL records.
2. Persist logs, raw outputs, and derived summaries.
3. Preserve compatibility between envelope fields and extensible payloads.
4. Preserve boundary-level step records needed to reconstruct judgment structure.

Interfaces:

1. `write_run_record(record, path)`
2. `write_step_record(record, path)`
3. `load_records(path) -> list[RunRecord]`

### 12.9 `experiments`

Responsibilities:

1. Load experiment configs.
2. Expand configuration grids into executable runs.
3. Materialize stable `cell_id` values and track multiple `attempt_id` values per cell.
4. Orchestrate run execution, retries, normalization, scoring, and aggregation.
5. Resolve modules exclusively through registries and declared interfaces.
6. Surface obligation summaries without presenting them as approvals.
7. Compose evidence providers, perturbation operators, study protocols, metrics, and reporters without embedding metric-specific or protocol-specific branching in the runner.

Interfaces:

1. `load_experiment(config_path) -> ExperimentConfig`
2. `expand_grid(config) -> list[RunSpec]`
3. `execute_experiment(config) -> ExperimentSummary`

## 13. Agent Pipeline Specifications

### 13.1 Baseline Direct Synthesis

Input:
task query and available evidence bundle.

Behavior:
produce a direct answer with no explicit option or conflict stage.

Expected artifacts:

1. final answer
2. optional cited evidence references
3. raw output or structured fields sufficient for normalization into frames, preserved conflicts, and selected action when those metrics are enabled

### 13.2 Retrieve-Then-Synthesize

Input:
task query plus retrieved top-k evidence.

Behavior:
synthesize an answer from retrieved evidence only.

Expected artifacts:

1. retrieved doc list
2. final answer
3. raw output or structured fields sufficient for normalization into the common scoring schema

### 13.3 Option-Generation Agent

Input:
task query plus evidence bundle.

Behavior:
generate multiple candidate actions before selecting one.

Expected artifacts:

1. candidate options
2. selected option
3. final answer
4. optional cited evidence references

### 13.4 Structured Conflict-Preserving Agent

Input:
task query plus evidence bundle.

Behavior:
identify frames, identify disagreements, generate options, select option, answer.

Expected artifacts:

1. identified frames
2. identified disagreements
3. candidate options
4. selected option
5. final answer
6. optional cited evidence references

### 13.5 Normalized Benchmark Scoring Schema

For v1 benchmarking, all four agent configurations must be transformed into a common normalized scoring payload before metric computation.

The minimum normalized payload should include:

1. `represented_frames`: normalized frame identifiers present in the final synthesis
2. `preserved_conflict_ids`: normalized conflict identifiers preserved in the synthesis
3. `generated_option_ids`: normalized candidate action identifiers
4. `selected_option_id`: selected action identifier when applicable
5. `final_answer_text`: final synthesized answer text
6. `cited_evidence_ids`: evidence items referenced by the answer when extractable
7. `parse_status`: `valid`, `partial`, or `invalid`
8. `unknown_mappings`: optional record of unmappable raw values by field

Identifier-bearing fields in this payload must resolve to task-defined `frame_id`, `conflict_id`, `option_id`, and `evidence_id` values when those constructs are present in the task family. When no valid mapping is available, the normalizer must emit an explicit unknown or null state rather than inventing a new identifier.

This v1 benchmark view is the scoring contract for the initial benchmark slice. Raw agent artifacts remain available for diagnosis, but metric modules should not depend on agent-specific payload shapes.

Future task families may define additional normalized views derived from the same core normalized envelope without requiring changes to the runner or telemetry envelope.

## 14. Metric Definitions

### 14.1 Conflict Retention Ratio

Definition:

`conflicts_preserved / source_conflict_count`

Interpretation:
higher is better; measures whether disagreement survives synthesis.

### 14.2 Frame Preservation Score

Definition:

`represented_relevant_frames / total_relevant_frames`

Interpretation:
higher is better; measures whether multiple analytical frames survive.

### 14.3 Option Breadth

Definition:

count of distinct generated candidate actions after normalization.

Interpretation:
higher is better up to task-reasonable bounds; detects option compression.

### 14.4 Path Dependence

Definition:

mean pairwise divergence across normalized outputs generated from registered perturbations of the same base evidence bundle.

Interpretation:
lower is better for robustness; higher indicates hidden dependence on evidence order.

For v1, the harness should support one primary path-dependence method:

1. group runs by `comparison_group_id`, where all members share the same task, agent, prompt, model, seed, study protocol, and base bundle, differing only by the registered perturbation instance
2. compare normalized artifacts, not raw strings
3. for each valid pair of runs in the group, compute:
   Jaccard distance over `represented_frames`
   Jaccard distance over `preserved_conflict_ids`
   Jaccard distance over `generated_option_ids`
   binary disagreement over `selected_option_id`
4. define the pairwise divergence score as the unweighted mean of the available component distances for that pair
5. define the group path-dependence score as the mean of pairwise divergence scores across all valid pairs in the group
6. report both the scalar score and the supporting field-level disagreement counts
7. if required grouped peers or bundle lineage are missing, mark the metric `unassessable` rather than imputing a score

Lexical similarity and judge-model scoring may be added later, but they are post-v1 extensions unless explicitly registered as alternative metric implementations.

### 14.5 Supporting Diagnostics

The system should also compute:

1. minority frame survival rate
2. unique document utilization count
3. option selection concentration
4. parse failure rate
5. invalid run rate

## 15. Execution Flow

### 15.1 Single Run

1. Load experiment configuration.
2. Resolve task set into tasks.
3. Expand a single run specification.
4. Materialize `cell_id`, `attempt_id`, and comparison metadata if the run belongs to a perturbation study.
5. Build base evidence bundle.
6. Apply a registered perturbation operator when required by the study protocol.
7. Execute the configured agent.
8. Emit or persist boundary step records for input, divergence if applicable, commit, and summary.
9. Normalize agent artifacts into the benchmark scoring schema.
10. Score metrics against the metric subject defined by the protocol and metric grouping contract.
11. Derive assessability state and any review obligations.
12. Persist run outputs.

### 15.2 Full Experiment

1. Load experiment config.
2. Expand all combinations into run specs.
3. Execute runs sequentially in v1.
4. Preserve one record per attempt and track the aggregate-selected attempt for each cell using the deterministic retry policy.
5. Write per-run telemetry to JSONL.
6. Build metric subjects from persisted records according to metric and protocol grouping requirements.
7. Ask the study protocol to materialize admissible metric subjects from persisted records and declared metric projection contracts.
8. Compute metrics after each run or as a post-pass.
9. Aggregate by task, case, family, agent, prompt, evidence provider, model, comparison group, and protocol-defined units as required by each metric.
10. Emit experiment summary tables, plots, and obligation summaries.

## 16. Output Artifacts

Each experiment should generate:

1. `runs.jsonl` containing normalized run records.
2. `metrics.jsonl` containing per-run scores.
3. `summary.json` containing aggregate statistics.
4. `failures.jsonl` for invalid or errored runs.
5. optional `figures/` directory for report-ready charts.
6. optional `attempts.jsonl` when the implementation separates attempt history from final run views.
7. optional `repro_bundle/` containing config, registry snapshot, and environment metadata.
8. `obligations.jsonl` containing assessability failures, compatibility issues, and review debt items.
9. optional `steps.jsonl` containing boundary step records when step-level tracing is enabled.

## 17. Configuration Strategy

All configurable choices should live in files rather than inline code where practical:

1. prompt templates
2. evidence provider presets
3. model definitions
4. task-set definitions
5. experiment definitions
6. module registry definitions
7. artifact schema definitions

Configuration precedence should be:

`defaults < config files < CLI overrides`

For v1, experiment configuration should be sufficient to determine:

1. the normalizer used for each agent-task-family combination
2. whether a run is a single-run benchmark cell or part of a grouped perturbation study
3. that retries append attempts and do not resume an incomplete attempt in place
4. which metrics score single runs versus grouped comparisons
5. which study protocol governs grouping, provenance, and admissibility checks for the experiment
6. which module-selection override wins when multiple compatible modules are available

## 18. Validation and Testing Plan

### 18.1 Unit Tests

Required coverage:

1. task schema validation
2. experiment config validation
3. metric computation on fixed fixtures
4. telemetry normalization
5. evidence bundle determinism and perturbation lineage integrity
6. registry resolution and plugin compatibility checks
7. study protocol validation and protocol-metric compatibility checks
8. assessability transitions when correlation or bundle-lineage metadata is missing
9. obligation creation for parse failure, unsupported metrics, and missing grouped-run peers
10. normalization mapping from raw artifacts to task-defined identifiers and explicit unknown states

### 18.2 Integration Tests

Required coverage:

1. one end-to-end run on a synthetic task
2. one multi-run experiment expansion
3. one path-dependence experiment with seeded shuffles
4. one newly added task family running without changes to the experiment runner
5. one traced run emitting input, divergence, commit, and summary step records
6. one experiment producing an `unassessable` outcome when required trace integrity is broken
7. one fixture-based experiment verifying expected metric ordering across known synthetic outputs
8. one grouped metric running through protocol-defined grouping without metric-specific runner branching

### 18.3 Acceptance Tests

Release gates for v1:

1. `run_experiment` succeeds on a documented config.
2. output files are written to expected directories.
3. metrics are reproducible across repeated seeded runs.
4. fixture tasks with known expected relationships yield the documented metric ordering and diagnostics.
5. a new registered module can be added and exercised without modifying core orchestration code.
6. rerunning a failed cell preserves attempt history and yields one unambiguous aggregate result for that cell.
7. one path-dependence experiment scores from comparison-group metadata without ad hoc postprocessing.
8. step records make the core run boundaries visible on at least one documented workflow.
9. harness statuses and summaries never use pass/fail language that could be mistaken for approval.
10. one metric that consumes grouped subjects can be added without changing runner logic.

## 19. Implementation Phases

### Phase 1: Foundations

Deliverables:

1. repository scaffold
2. typed schemas
3. task loader and validator
4. telemetry writer
5. 12 synthetic tasks
6. 5 real-document tasks
7. baseline direct pipeline
8. registry mechanism for task families, evidence providers, perturbation operators, study protocols, agents, and metrics

Exit criteria:

1. one task runs end to end
2. one JSONL output can be scored

### Phase 2: Pipelines and Sweeps

Deliverables:

1. all four agent pipelines
2. prompt variant support
3. evidence provider presets
4. one study protocol implementation for standard benchmark runs and one for perturbation studies
5. experiment config loader
6. grid expansion and execution runner
7. 20 to 25 total tasks

Exit criteria:

1. one named experiment runs automatically across multiple cells

### Phase 3: Metrics and Analysis

Deliverables:

1. all four primary metrics
2. evidence perturbation workflow
3. aggregation utilities
4. first figures and summary tables
5. one non-core extension module to verify modularity in practice

Exit criteria:

1. at least one documented experiment summary matches expected fixture behavior and metric diagnostics

### Phase 4: Expansion and Polish

Deliverables:

1. full 40 to 50 task suite
2. README and reproducibility instructions
3. technical report draft
4. polished figures
5. example experiment configs for multiple studies

Exit criteria:

1. a reviewer can clone the repo and reproduce a demo experiment

## 20. Risks and Mitigations

### Risk 1: Overbuilding infrastructure

Mitigation:
keep v1 sequential, local, and file-based.

### Risk 2: Annotation burden for real tasks

Mitigation:
limit real-document tasks to a small, high-quality initial set.

### Risk 3: Metrics become subjective or brittle

Mitigation:
use explicit task annotations and simple interpretable formulas first.

### Risk 4: Agent outputs are hard to parse

Mitigation:
use structured response templates and validation with fallback failure logging.

### Risk 4b: Successful runs are mistaken for approval or scientific validity

Mitigation:
use obligation-oriented assessment states, explicit non-claims, and separate executable, reproducible, and scientifically interpretable readiness levels.

### Risk 5: Too many experiment dimensions

Mitigation:
restrict v1 to 1 to 2 models, a small provider set, and a small prompt set.

### Risk 6: Plugin surface becomes vague or inconsistent

Mitigation:
define explicit registries, typed interfaces, and artifact schema versioning from the start.

### Risk 7: Trace integrity breaks grouped comparisons silently

Mitigation:
require stable correlation identifiers, bundle lineage, and comparison-group metadata; mark affected metrics unassessable when these are missing.

### Risk 8: Transcript and fixture coverage is mistaken for completeness

Mitigation:
use golden transcripts to protect known critical paths, but state explicitly that they guard remembered scenarios rather than proving coverage completeness.

## 21. Recommended Initial Build Decisions

1. Implement the harness in Python.
2. Use Pydantic or equivalent typed schemas for tasks, telemetry, and configs.
3. Store tasks as YAML for readability and experiment configs as YAML.
4. Use JSONL for run-level telemetry and metrics outputs.
5. Keep experiment execution sequential first; parallelism can be added later.
6. Build metrics from normalized artifacts rather than raw strings.
7. Version all extension-facing schemas explicitly.
8. Treat evidence providers as a generalized base-input interface, not as owners of perturbation semantics.
9. Treat step-level telemetry as visibility instrumentation, not as a control or approval mechanism.
10. Name run and experiment statuses so they cannot be confused with pass/fail certification.
11. Require identifier-bearing annotation objects for every scored entity instead of free-text lists.
12. Make study protocol selection explicit in every experiment config that uses grouped or perturbation-based metrics.

## 22. Open Questions

These decisions should be resolved before implementation begins in earnest:

1. Which exact model interfaces will v1 support?
2. Will evidence provision be simulated from task-local documents only, or include embeddings and precomputed bundles?
3. How will output divergence be measured for path dependence:
   lexical similarity, structured artifact difference, or judge model scoring?
4. How much raw model output should be retained for reproducibility versus cost or privacy?
5. What is the minimum annotation standard for real-document tasks?
6. Which first extension module should be used to test modularity beyond the initial benchmark family?
7. What is the exact core normalized envelope shape, and which benchmark views are derived from it in v1?
8. Which plugin loader kinds will v1 officially support?

## 23. Immediate Next Steps

1. Convert this plan into repository issues or milestones.
2. Scaffold the repository structure and package layout.
3. Implement schemas for base tasks, family annotations, experiments, telemetry envelopes, and artifact payloads first.
4. Implement the registry mechanism before adding multiple pipelines.
5. Add a minimal end-to-end runner with one synthetic fixture task.
6. Lock the first experiment config around conflict retention before broadening scope.
7. Add one extra task family beyond the original four to validate extensibility early.
8. Add one documented traced workflow showing input, divergence, commit, and summary boundaries end to end.
9. Finalize the grouped metric subject contract before implementing path-dependence scoring.
10. Define the module resolution algorithm and plugin loader contract before adding third-party extensions.
11. Separate the core normalized envelope from the benchmark-specific normalized view before implementing more than one task family.

## 24. Acceptance Summary

The technical plan is complete when the implementation can support this workflow without code edits:

1. define or select a task set
2. define an experiment config
3. run the experiment
4. collect telemetry
5. score structural metrics
6. compare pipelines
7. generate reproducible results
8. register a new decision-space task family or metric module without changing core orchestration logic

That is the core standard the DecisionSpace Harness should be built to meet.

## 25. Experiment Classes and Scientific Validity Addendum

This section defines the post-v1 scientific protocol layer unless a later implementation phase explicitly promotes a requirement into the v1 core.

The v1 harness core must leave room for these capabilities in schemas and registries, but v1 does not need to fully enforce every scientific validity gate below.

This addendum defines the classes of decision-space experiments the harness should support and the minimum requirements for running them in a reproducible and scientifically valid way.

The core design principle is:

The harness must support modular experimentation at two levels:

1. software modularity
2. scientific protocol modularity

The first allows new modules to be added without rewriting the system. The second ensures new experiments remain interpretable, comparable, and methodologically defensible.

### 25.1 Supported Classes of Decision-Space Experiments

The harness should be designed to support at least the following experiment classes.

1. Conflict preservation experiments.
   Question:
   Does the system retain meaningful disagreement rather than smoothing it away?

2. Frame diversity or schema lock experiments.
   Question:
   Does the system preserve multiple analytical frames or collapse into a dominant one?

3. Option-space compression experiments.
   Question:
   Does the system narrow the set of candidate actions before selection?

4. Evidence path dependence experiments.
   Question:
   How sensitive are outputs to evidence ordering, retrieval depth, or bundle composition?

5. Constraint-enforcement experiments.
   Question:
   Do executable structures such as DAGs or policy rules reduce invalid reasoning paths?

6. Counterfactual invariance experiments.
   Question:
   Are outputs stable under proxy-only or otherwise non-causally relevant perturbations?

7. Noise and misspecification robustness experiments.
   Question:
   How do results change when evidence quality, retrieval quality, or structural assumptions are degraded?

8. Drift and temporal stability experiments.
   Question:
   Do path properties or structural metrics shift under temporal or distributional change?

9. Cross-domain transfer experiments.
   Question:
   Do the same metrics, task patterns, or structural interventions generalize across domains?

10. Ablation and intervention experiments.
    Question:
    Which component or structural change actually drives the observed effect?

11. Auditability and human-review experiments.
    Question:
    Are the produced paths, options, and constraints understandable and inspectable by analysts?

12. Multi-run stability experiments.
    Question:
    Are decisions and path artifacts stable across repeated stochastic runs?

### 25.2 Scientific Protocol Layer

Post-v1, each experiment should have a protocol definition in addition to an execution config.

The protocol definition should specify:

1. research question
2. hypothesis or comparison claim
3. unit of analysis
4. task family or families
5. task construction method
6. perturbation or intervention design
7. pairing, blocking, or stratification rules
8. metrics and primary endpoints
9. secondary diagnostics
10. exclusion rules
11. aggregation plan
12. threats to validity

The harness should treat this protocol as a first-class artifact rather than informal documentation once the protocol layer is implemented.

### 25.3 Study Protocol Schema

Each study should have a protocol file such as:

```yaml
study_id: proxy_invariance_finance_v1
title: Proxy invariance under decision-space constraints
research_question: Does constrained execution reduce proxy-driven instability?
hypothesis:
  primary: constrained_agent has lower proxy_dependence than unconstrained_agent
unit_of_analysis: counterfactual_pair
task_families:
  - dag_constrained_finance
task_set: finance_proxy_pairs_v1
design:
  type: paired_counterfactual
  reruns_per_case: 5
  strata:
    - normal
    - borderline
    - proxy_conflict
  perturbations:
    - proxy_only_swap
    - structure_noise_low
primary_metrics:
  - counterfactual_proxy_invariance
  - structural_violation_rate
secondary_metrics:
  - path_fidelity
  - accuracy_guardrail
aggregation:
  group_by:
    - agent_config
    - stratum
  summary_statistics:
    - mean
    - median
    - ci_95
validity:
  construct_risks:
    - proxy feature may correlate with label in generator
  internal_risks:
    - prompt leakage across paired cases
  external_risks:
    - synthetic stylization limits domain generalization
```

### 25.4 Task Family Validity Contract

Each task family must declare not only its schema, but also its validity constraints.

Each task family registration should include:

1. construct being measured
2. required annotations
3. allowed perturbation types
4. admissible metrics
5. invalid metric-task combinations
6. minimum sample structure
7. known failure modes
8. recommended controls
9. expected threats to validity

This prevents weak or incompatible experiments from appearing legitimate simply because they execute successfully.

### 25.5 Metric Specification Requirements

Each metric module must declare:

1. target construct
2. mathematical definition
3. expected input artifact schema
4. normalization rules
5. failure conditions
6. interpretation direction
7. admissible task families
8. robustness checks
9. known confounds

Metrics should not be treated as reusable by default; they are reusable only when their assumptions match the task family and protocol.

### 25.6 Perturbation and Intervention Operators

The harness should represent perturbations as registered experimental operators rather than ad hoc task edits.

Examples include:

1. evidence order shuffle
2. retrieval depth change
3. proxy-only attribute swap
4. synthetic structure noise injection
5. DAG edge deletion or insertion
6. evidence omission
7. temporal slice shift

Each operator should define:

1. what it changes
2. what it must preserve
3. valid task families
4. seed behavior
5. expected interpretation

This is necessary for scientifically valid reuse of perturbation studies.

### 25.7 Provenance and Audit Requirements

To support reproducibility, each run must log provenance metadata beyond the basic execution envelope.

Required provenance fields:

1. task generator version
2. annotation schema version
3. study protocol version
4. prompt template version
5. model identifier and version
6. evidence provider version
7. metric version
8. perturbation operator version
9. aggregation rule version
10. seed source and seed value

Without these fields, repeatability may exist operationally while scientific reproducibility remains weak.

### 25.8 Statistical Reporting Requirements

The harness should support reporting rules appropriate for empirical studies rather than only benchmark summaries.

For publishable studies, the reporting layer should support:

1. effect sizes
2. confidence intervals
3. variance across reruns
4. stratified summaries
5. paired comparison summaries where applicable
6. invalid-run accounting
7. sensitivity to perturbations
8. metric coverage diagnostics

The spec does not require heavy statistical automation in v1, but it should require the data products needed to compute these summaries reliably.

### 25.9 Reproducibility Standards by Experiment Class

Different experiment classes require different minimum controls.

1. Counterfactual experiments require paired identifiers, perturbation provenance, and invariance rules.
2. Drift experiments require temporal or distribution split definitions and stable evaluation windows.
3. Ablation experiments require explicit component toggles and controlled non-target variation.
4. Multi-run stability experiments require repeated seeds and aggregated variance reporting.
5. Cross-domain experiments require domain labels, metric comparability notes, and domain-specific validity statements.

Post-v1, the harness should reject or warn on experiment configs that omit required controls for the declared study type.

### 25.10 Scientific Validity Gates

An experiment should be considered scientifically ready only if it satisfies all of the following:

1. task family is registered and validity contract is present
2. protocol file is present and versioned
3. metrics are compatible with task family and artifact schema
4. perturbations are declared through registered operators
5. seeds and rerun policy are specified
6. provenance logging is complete
7. aggregation plan is defined
8. threats to validity are explicitly documented

This gate should sit alongside the engineering acceptance criteria once the protocol layer is promoted from extension to enforced workflow.

### 25.11 Implications for Reuse

With this addendum, reuse should mean more than reusing code.

The harness should support reuse at four levels:

1. code reuse:
   agent, metric, task, and evidence modules can be reused directly
2. protocol reuse:
   study designs can be adapted across domains without being rebuilt informally
3. metric reuse:
   metrics can be reused only when assumptions are explicitly compatible
4. reporting reuse:
   figures and summaries can be regenerated from standardized outputs

This is the level of reuse needed if the harness is intended to support multiple papers, domains, and structural claims over time.

## 26. Inference and Validation Addendum

This section also describes post-v1 methodological requirements. The v1 core should preserve the metadata needed to support these features later, but it is not required to implement every inference-oriented validation rule in the first release.

This addendum defines the minimum methodological requirements needed for the harness to support scientifically defensible empirical claims, not only executable experiments.

### 26.1 Decision-Space Ontology

The harness should use a minimal shared ontology so constructs remain comparable across task families.

Core entities:

1. interpretation:
   a representation of how evidence is framed, grouped, or explained
2. action:
   a candidate decision, recommendation, or intervention available to the system
3. path:
   an ordered sequence of reasoning, retrieval, or execution steps connecting evidence to an action
4. constraint:
   a rule, structure, or executable boundary that restricts allowed paths
5. invalid path:
   a path that violates task-defined structure, policy rules, or experimental constraints
6. perturbation:
   a controlled change to inputs, order, structure, or metadata used to probe stability or robustness

Every task family must define how these entities are instantiated in that family.

### 26.2 Study Types and Allowed Claims

The harness must distinguish between descriptive, comparative, and causal study types.

1. descriptive benchmark:
   allowed claim:
   systems differ on observed structural metrics under a fixed benchmark design
2. comparative intervention study:
   allowed claim:
   changing a specified component is associated with metric differences under controlled conditions
3. causal ablation study:
   allowed claim:
   removing or changing a single component changes outcomes under a controlled intervention design
4. robustness study:
   allowed claim:
   system behavior changes under prespecified perturbations or misspecification regimes
5. transfer study:
   allowed claim:
   a metric or intervention generalizes across declared domains within the tested setup

The harness should not imply stronger causal claims than the declared study type supports once study typing is part of the enforced protocol workflow.

### 26.3 Estimands and Units of Inference

Each study protocol must declare:

1. unit of assignment
2. unit of observation
3. unit of aggregation
4. primary estimand

Examples:

1. single-run benchmark:
   unit of observation:
   run
2. multi-run stability study:
   unit of observation:
   run
   unit of aggregation:
   case
3. counterfactual invariance study:
   unit of observation:
   paired case
   unit of aggregation:
   pair
4. drift study:
   unit of observation:
   case within time slice
   unit of aggregation:
   slice or domain

The reporting layer should preserve enough data to estimate these units correctly.

### 26.4 Default Aggregation Rules

The harness should provide default aggregation rules by study type.

1. repeated-run studies:
   aggregate within case first, then across cases
2. paired counterfactual studies:
   compute within-pair differences first, then aggregate across pairs
3. stratified studies:
   report stratum-specific effects before pooled effects
4. multi-domain studies:
   report domain-specific results before pooled summaries
5. ablations:
   compare only cells that differ in the targeted component

Once design-aware aggregation is implemented, global pooling without respect to design structure should be treated as invalid unless explicitly justified.

### 26.5 Statistical Reporting Minimums

For paper-facing studies, the harness should require outputs sufficient to report:

1. sample sizes by condition and slice
2. mean or median estimates as appropriate
3. uncertainty intervals
4. effect sizes
5. variance across reruns when reruns exist
6. invalid-run counts
7. exclusion counts
8. sensitivity summaries under perturbation

The spec does not require one fixed inferential method, but every study protocol must declare the intended summary family:

1. descriptive interval estimate
2. paired difference estimate
3. bootstrap interval
4. permutation-based comparison
5. model-based estimate

### 26.6 Annotation and Synthetic Generator Validation

Schema-valid annotations are not sufficient for scientific validity.

When human annotation is used, the harness should require:

1. annotation guidelines
2. annotator provenance
3. quality-control sample
4. agreement or adjudication record

When synthetic task generation is used, the harness should require:

1. generator version
2. generator parameters
3. slice construction logic
4. label-generation logic
5. perturbation-generation logic
6. validation checks that intended invariances and violations are actually present

Synthetic studies should not be considered scientifically ready unless the generating process is auditable.

### 26.7 Negative Controls and Placebo Checks

Each paper-facing study should include at least one negative control where possible.

Examples:

1. a perturbation that should not change the decision if the metric is well targeted
2. a structure change irrelevant to the measured construct
3. an evidence reorder expected to preserve outcome under a robust system

The purpose is to detect metrics that respond to arbitrary instability rather than the target construct.

Protocols should explicitly mark:

1. positive controls
2. negative controls
3. expected null effects

### 26.8 Metric Admission Standard

New metric modules must satisfy a minimum evidence standard before being used in paper-facing studies.

Each new metric should include:

1. formal definition
2. justification for the construct being measured
3. admissible task families
4. examples where the metric should increase
5. examples where the metric should remain unchanged
6. known failure cases
7. at least one calibration or sanity-check study

Metrics that lack these artifacts may still be used exploratorily, but should be labeled exploratory rather than confirmatory.

### 26.9 Exploratory Versus Confirmatory Analyses

The harness should support explicit labeling of analyses as:

1. confirmatory
2. exploratory
3. diagnostic

Confirmatory analyses require:

1. versioned protocol
2. prespecified primary metrics
3. declared exclusion rules
4. declared aggregation rules

Exploratory analyses may be broader, but outputs should be labeled accordingly in summaries and reports.

### 26.10 Computational Reproducibility

Scientific reproducibility requires environment capture in addition to seeds and configs.

Each experiment run should record:

1. dependency lock or environment manifest version
2. Python version
3. model backend version
4. tokenizer version where relevant
5. hardware class where materially relevant
6. operating system information

The harness should support exporting a reproducibility bundle containing:

1. experiment config
2. study protocol
3. registry snapshot
4. environment manifest
5. task and annotation versions
6. run outputs

### 26.11 Trace Review and Audit Protocol

For studies making claims about observability, auditability, or path quality, telemetry alone is insufficient.

Such studies should define:

1. what a reviewable trace consists of
2. which artifacts are shown to reviewers
3. how ambiguous traces are adjudicated
4. whether reviewers are blinded to condition
5. what criteria define successful observability

This requirement prevents weak auditability claims based solely on the presence of logs.

### 26.12 Scientific Readiness Gates

An experiment should be considered ready for paper-facing interpretation only if all of the following are true:

1. ontology mapping is declared for the task family
2. study type is declared and compatible with the claim language
3. estimand and unit of aggregation are declared
4. annotation or generator validation artifacts are present
5. negative controls are included where applicable
6. metrics satisfy the admission standard
7. confirmatory versus exploratory status is declared
8. computational environment is captured
9. provenance logging is complete
10. invalid-run and exclusion accounting are available

### 26.13 Implications for the Harness

With this addendum, the harness should support three distinct readiness levels:

1. executable:
   the experiment runs successfully
2. reproducible:
   the experiment can be rerun with stable inputs and environment metadata
3. scientifically interpretable:
   the experiment satisfies protocol, validation, and inferential requirements

The system should make these levels visible rather than treating successful execution as equivalent to scientific validity when the scientific protocol layer is enabled.
