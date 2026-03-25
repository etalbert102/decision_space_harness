# DecisionSpace Harness Technical Specification Plan

## 1. Purpose

Build vs buy note: keep the core research framing, decision-space concepts, and scientific claims fully in-house; no external package should define the benchmark semantics.

DecisionSpace Harness is a reusable evaluation harness for measuring how LLM-agent pipelines compress, preserve, or reshape the space of interpretations and actions available during evidence synthesis. In v1, the system is scoped to benchmark-style comparisons, prompt and evidence sweeps, and a small number of repeatable empirical studies.

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

Build vs buy note: keep goal-setting and system boundaries in-house; external packages should serve these goals, not reshape them.

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

Build vs buy note: success criteria around reproducibility, extensibility, and metric validity are custom product requirements; package choices should be evaluated against them rather than treated as goals themselves.

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

Build vs buy note: all research questions and the mapping from system behavior to scientific claims should remain custom.

The v1 harness must support the following research questions:

1. Do answer-first pipelines smooth over legitimate disagreement in evidence?
2. Do synthesis pipelines collapse multi-frame evidence into a narrower interpretive schema?
3. How sensitive are outputs to evidence ordering, evidence depth, and prompt framing?
4. Do structured agent workflows preserve a broader candidate action space than standard RAG baselines?
5. Which pipeline choices materially improve structural robustness without requiring model changes?
6. What other structural decision-space properties can be studied once the harness supports new task families and metrics?

## 5. System Scope

Build vs buy note: use mature libraries for generic infrastructure inside the scope, but keep scope boundaries and non-goals explicit in-house.

### 5.1 In Scope

1. Task definition and storage.
2. Evidence bundle generation and perturbation.
3. Agent pipeline execution over controlled inputs.
4. Telemetry collection for intermediate and final outputs.
5. Metric computation from task metadata and run artifacts.
6. Experiment configuration, expansion, execution, and aggregation.
7. Export of results for analysis and report generation.
8. Stable extension points for broader decision-space experiments after v1.

### 5.2 Out of Scope

1. Human-in-the-loop annotation tooling in v1.
2. Online retrieval from live web sources during evaluation by default.
3. Fine-tuning or model training.
4. Real-time serving infrastructure.
5. Full interactive dashboards in v1.

## 6. Conceptual Architecture

Build vs buy note: keep the architecture, execution boundaries, and judgment-anchor model in-house; only the plumbing beneath modules should be delegated to packages.

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
3. commit boundary: final answer selection, artifact finalization, and persisted attempt record emission
4. attempt_summary boundary: per-attempt finalization, assessability, and obligation emission
5. summary boundary: experiment-level aggregation, diagnostics, and obligation reporting

This architecture separates six concerns:

1. task semantics
2. experimental design
3. evidence provisioning
4. pipeline behavior
5. measurement logic
6. result presentation

The architecture should treat the following as replaceable modules rather than fixed benchmark components, even if some remain built-in in v1:

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

Build vs buy note: requirements for task semantics, normalization, metrics, and assessability are custom; generic validation, serialization, and CLI behavior are good package candidates.

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
2. Support multiple evidence provider types in v1, at minimum local document bundles and optional precomputed retrieval outputs.
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
8. Emit explicit boundary events or equivalent step records for input, divergence, commit, `attempt_summary`, and experiment-level `summary` stages.

### 7.5 Telemetry Layer

The system must:

1. Log one JSON object per run step or one normalized object per completed attempt, depending on the selected mode.
2. Include enough information to recompute metrics offline.
3. Preserve raw model outputs when permitted by configuration.
4. Track timing, seeds, errors, and retries.
5. Store outputs in a stable directory structure for later aggregation.
6. Separate stable run envelope fields from extensible artifact payloads so new modules do not require schema churn.
7. Preserve superseded attempts rather than overwriting them, while making the aggregate-selected attempt unambiguous for aggregation.
8. Mark runs or experiments unassessable when trace integrity required for comparison or scoring is missing.
9. Treat attempt-level telemetry as the canonical persisted source of truth and derive selected-run views from it deterministically.

### 7.6 Metrics Layer

The system must:

1. Compute metrics deterministically from task metadata and telemetry.
2. Distinguish between missing data, zero scores, normalization-invalid attempts, and unassessable metric subjects.
3. Support per-subject, per-task-family, and per-experiment aggregation.
4. Expose both scalar scores and supporting diagnostic counts.
5. Allow new metric modules to be registered independently and bound to specific task families or artifact types.
6. Validate that required normalized fields and comparison-group structure are present before scoring.
7. Produce obligations and diagnostics for human review when assessability or compatibility conditions fail.

## 8. Non-Functional Requirements

Build vs buy note: use external packages where they improve reproducibility, inspectability, and simplicity, but avoid package choices that obscure provenance or add avoidable operational complexity.

1. Reproducibility: runs must be seedable and configuration-driven.
2. Inspectability: all important intermediate artifacts must be observable in logs.
3. Modularity: new experiments and most new decision-space modules should require configuration changes and registration, not edits to core orchestration code.
4. Simplicity: the v1 implementation should remain understandable by a single researcher.
5. Portability: the harness should run on a standard local development machine.
6. Extensibility: new metrics, tasks, evidence providers, and agent types must fit existing interfaces.
7. Backward compatibility: adding a new task family or metric should not break existing experiment configs or historical artifacts.
8. Honesty of claims: the harness must distinguish visibility, reproducibility, and scientific interpretability rather than collapsing them into a single pass state.

## 9. Repository Structure

Build vs buy note: keep the repository layout custom, but assume standard Python tooling such as `pytest`, `pydantic`, `typer`, and `pandas` will shape the internal module boundaries.

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

Build vs buy note: implement schemas with `pydantic` and parse YAML with `PyYAML`, but keep task-family ontology, identifier semantics, normalized scoring fields, and assessability rules in-house.

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

To preserve room for post-v1 scientific methodology without widening v1 enforcement scope, task-family schemas and registrations should also reserve optional ontology-mapping slots for broader entities such as:

1. `interpretation_entities`
2. `action_entities`
3. `path_entities`
4. `constraint_entities`
5. `perturbation_entities`

These fields may be absent or empty in v1. They exist to avoid forcing a future schema break when later task families need to express paths, constraints, invalid paths, or richer intervention structure.

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
analysis_label: exploratory
target_use: benchmark
readiness_target: executable
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
protocol_artifact: null
seeds:
  - 11
  - 22
output_dir: outputs/experiments/conflict_smoothing_v1
```

In this schema:

1. `study_protocol` identifies the registered execution and grouping module used by the runner
2. `protocol_artifact`, when present, points to a versioned scientific protocol document that records study-design intent beyond execution settings
3. `analysis_label` declares whether the workflow is `exploratory`, `confirmatory`, or `diagnostic`
4. `target_use` declares whether the outputs are intended for `benchmark`, `demo`, or `paper_facing` use
5. `readiness_target` declares the highest readiness level the workflow intends to satisfy, such as `executable`, `reproducible`, or `scientifically_interpretable`

For v1, `protocol_artifact` may be absent. The important design choice is that the executable protocol module and the optional scientific protocol artifact are distinct concepts rather than one overloaded field.

The intent fields above are execution-governance metadata, not substitutes for `protocol_artifact`. They exist so validation can determine strict workflow requirements before execution begins. When omitted, v1 should default them to `analysis_label=exploratory`, `target_use=benchmark`, and `readiness_target=executable`.

To reduce drift and copy-paste risk, v1 experiment configs should not introduce separate first-class fields for scientific semantics such as study type, units, primary metrics, aggregation plan, or validity notes. When those semantics are needed, they should come from `protocol_artifact`.

When `protocol_artifact` is present, it should take precedence for scientific semantics. If the resolved execution semantics implied by `study_protocol` disagree with the `protocol_artifact` on overlapping fields, the runner should emit an explicit `protocol_alignment_mismatch` flag during config validation rather than silently merging them.

For v1, the overlap set checked by `protocol_alignment_mismatch` should be explicit and limited to:

1. study type
2. unit of observation or analysis, when the protocol module exposes one
3. unit of aggregation, when the protocol module exposes one
4. primary metrics or endpoints, when the protocol module exposes them
5. exclusion rules, when the protocol module exposes them
6. aggregation plan, when the protocol module exposes one
7. threats to validity or validity notes, when the protocol module exposes them

Fields outside this overlap set should not trigger `protocol_alignment_mismatch` in v1.

Experiment configs should also support optional module overrides:

1. task-family-specific validators
2. artifact schema selection
3. aggregator implementation
4. reporter selection
5. normalizer selection
6. perturbation operator selection
7. study protocol selection

Override resolution must be deterministic. For v1, module selection precedence should be:

`registry default < task-family default < experiment override < explicit cell override`

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
2. attempt execution state values should use a fixed terminal set: `completed`, `failed`
3. aggregation should use the latest successful attempt for a cell when any successful attempt exists
4. if no successful attempt exists, aggregation should use the latest terminal non-success attempt only for failure accounting, not as a substitute successful score
5. superseded attempts must remain preserved in telemetry
6. the aggregate-selected attempt for each cell must be explicit in persisted outputs

Attempt-level telemetry should be the canonical source of truth for v1. Any selected-run or aggregate-ready view must be derived from attempt records plus the deterministic selection policy rather than maintained as an independent peer source of truth.

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
4. `attempt_summary`
5. `summary`

These records are visibility artifacts. They do not certify correctness, authority, or completeness.

Each completed attempt should emit an attempt record similar to:

```json
{
  "event_id": "evt_20260323T153012Z_conflict_smoothing_v1_policy_04_baseline_direct_top5_seed11_attempt1",
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
  "execution_state": "completed",
  "normalization_state": "valid",
  "supersedes_attempt_id": null,
  "error": null,
  "assessability": {
    "status": "assessable",
    "reasons": []
  },
  "review": {
    "state": "no_new_obligations_created",
    "obligations": []
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
    "schema": "decision_space_benchmark_normalized/v1",
    "diagnostics": [],
    "unknown_mappings": [],
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

For v1, persisted attempt records should be immutable once written. Derived views such as selected-run views, failure summaries, and metric subjects should be reproducible from canonical attempt telemetry plus explicit derivation rules.

For v1 serialization, canonical attempt records should carry the four state axes explicitly as:

1. `execution_state`
2. `normalization_state`
3. `assessability.status` plus `assessability.reasons`
4. `review.state` plus any associated `review.obligations`

Derived selected-run views should add:

1. `selected_attempt_id`
2. `selection_role`, with values `metric_scoring` or `failure_accounting`
3. `eligible_for_metric_scoring`

For v1, a selected-run view should be a derived full-view projection of the selected attempt rather than a thin pointer only. It should retain the same stable envelope fields and normalized artifacts needed for scoring, while adding the selected-run metadata above. This keeps selected-run consumers simple while preserving traceability back to canonical attempt telemetry.

For v1, metrics should score against `normalized_artifacts`, not agent-specific raw payloads. Agents may emit richer task-family-specific artifacts, but every benchmarked run must end with a normalized scoring payload produced either:

1. directly by the agent, or
2. by a registered postprocessor or normalizer applied after agent execution

If normalization fails, the attempt record should still be preserved when execution itself completed, while metrics that depend on missing normalized fields must treat the affected metric subject as `unassessable`.

The v1 normalization layer must also preserve explicit unknown states. A normalizer must not invent task-independent identifiers merely to satisfy the scoring schema.

For v1, the harness should implement one normalized scoring family only: `decision_space_benchmark_normalized`.

The stable normalized envelope for that family should contain:

1. `schema`
2. `payload`
3. `diagnostics`
4. `unknown_mappings`

For the initial benchmark slice, the first payload version should be `decision_space_benchmark_normalized/v1`.

That v1 payload should contain:

1. `represented_frames`
2. `preserved_conflict_ids`
3. `generated_option_ids`
4. `selected_option_id`
5. `final_answer_text`
6. `cited_evidence_ids`
7. `parse_status`

The runner and telemetry layer should depend only on the stable normalized envelope plus schema id and version, together with the top-level attempt `normalization_state`, not on the concrete payload field list. Metric modules should declare the normalized fields they require through their projection contract and score only when those required fields are present. A more general core normalized envelope and multiple payload versions remain valid in v1 so long as the benchmarked metrics can resolve their declared field requirements.

Identity and reproducibility rules for v1:

1. `cell_id` is the stable logical identity of a planned experimental unit
2. `attempt_id` is the stable identity of one execution attempt of that cell and should be derived deterministically from `cell_id` plus `attempt_index`
3. `event_id`, when present on canonical attempt telemetry, is an event identifier for a persisted record and is not the canonical logical identity for comparison or reproducibility
4. reproducibility claims must be anchored to `cell_id`, `attempt_id`, registry versions, prompt version, model identifier, provider identifier, decoding parameters, and applied seed
5. persisted provenance should include the exact Ollama model identifier and, when available, a content digest or immutable model tag rather than only a friendly alias such as `local_model`

### 10.7 Provenance and Compatibility Metadata

To keep extension behavior machine-checkable rather than implicit, every persisted attempt record and every registry entry should expose enough metadata for compatibility validation.

Minimum compatibility-relevant persisted metadata should include:

1. task family id and version
2. annotation schema id and version
3. artifact schema id and version
4. normalized schema id and version
5. evidence provider id and version
6. perturbation operator id and version when applicable
7. study protocol id and version when applicable
8. metric ids and versions used for scoring
9. prompt template id and version
10. model provider identifier, concrete model identifier, and decoding parameters

To keep later scientific-validity upgrades additive rather than invasive, the persisted metadata model should also reserve optional namespaces for:

1. execution provenance
2. scientific provenance
3. environment provenance

For v1, these namespaces may be partially populated. The key requirement is that new provenance requirements can be added inside these containers without changing the run-record envelope shape.

The runner should validate these metadata against declared module capabilities before execution and again before scoring grouped metrics.

If trace integrity fails, such as missing correlation across grouped runs or missing bundle lineage for perturbation comparisons, the relevant metric computation should become `unassessable` rather than silently degrading to a numeric score.

### 10.8 Assessment Status and Obligations

Following the fidelity-framework model, harness assessment outputs should create review obligations rather than approval states.

Recommended assessability statuses:

1. `assessable`
2. `unassessable`: trace integrity, compatibility, or required artifacts are missing

Recommended review statuses:

1. `no_new_obligations_created`: no new issues were detected relative to the configured checks
2. `obligations_present`: the run or experiment completed, but review-worthy issues were detected

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
7. `protocol_alignment_mismatch` between resolved execution semantics and `protocol_artifact`

These states should be modeled as separate axes rather than overloaded flags:

1. execution state: `completed`, `failed`
2. normalization state: `valid`, `partial`, `invalid`
3. assessability state: `assessable`, `unassessable`
4. review state: `no_new_obligations_created`, `obligations_present`

The runner, metrics layer, and reporters should consume these axes independently so future modules do not need to reinterpret the meaning of `invalid`, `failed`, or `unassessable`.

Recommended interpretation rules for v1:

1. if model or runner execution fails before artifact production, set `execution_state=failed`
2. if execution completes but normalization cannot produce a usable scoring payload, set `execution_state=completed` and `normalization_state=invalid`
3. metric results that require missing normalized fields must be `unassessable` rather than coercing the whole run into a failed execution state
4. review obligations are additive and may be present for either assessable or unassessable results

## 11. Registry and Plugin Model

Build vs buy note: keep v1 on an internal registry implemented in plain Python; consider `pluggy` or Python entry points via `importlib.metadata` only if post-v1 third-party plugins become a real requirement.

The harness should use explicit registries so new modules can be added without modifying the runner.

### 11.1 Required Registries

1. task family registry
2. annotation schema registry
3. evidence provider registry
4. agent registry
5. normalizer registry
6. metric registry
7. perturbation operator registry
8. study protocol registry

For v1, aggregation and reporting may remain built-in implementation modules behind stable interfaces. A separate artifact-schema registry is optional in v1 if artifact schemas are versioned and validated in code or configuration without dynamic plugin loading.

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

To keep the scientific-methodology layer refactorable, registry entries should also permit optional future-facing metadata such as:

1. target construct
2. admissible task families
3. allowed perturbation types
4. invalid compatibility combinations
5. known failure modes
6. threats to validity
7. required protocol features
8. readiness level such as `benchmark`, `exploratory`, or `paper_facing`

These fields may be advisory only in v1. They should be stored in registry metadata before the harness begins enforcing them.

Registry compatibility should be machine-checkable. A module should be selectable only when its declared requirements are satisfied by the task family, normalized schema, study protocol, and run grouping available in the experiment definition.

Plugin loading should also be a documented contract, not an implicit import convention. For v1, a simple internal Python registry keyed by `(module_id, version)` is sufficient. Dynamic third-party plugin loading is a post-v1 extension unless it is required by a concrete benchmark use case.

Module loading failures should surface as configuration or startup errors before run execution begins.

### 11.2 Extension Principle

A new decision-space module should be addable by:

1. implementing the module against a declared interface
2. registering it in configuration
3. referencing it in an experiment config

Core orchestration code should not need to change unless the extension introduces an entirely new execution primitive.

## 12. Module Design

Build vs buy note: offload commodity module internals to packages where practical, but keep interfaces and contracts custom so the harness owns execution semantics rather than a framework.

### 12.1 `tasks`

Build vs buy note: use `pydantic` and `PyYAML` for schema validation and file loading; keep task-family dispatch, annotation validation rules, and identifier semantics in-house.

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

Build vs buy note: keep evidence-bundle semantics and lineage custom; only basic IO, parsing, and utility helpers should come from standard libraries or lightweight helpers.

Responsibilities:

1. Build evidence bundles from task evidence items or other registered evidence sources.
2. Build a base bundle before any registered perturbation is applied.
3. Apply provider-specific selection logic only.
4. Return ordered evidence bundles with metadata.

Interfaces:

1. `get_base_evidence(task, provider_config, seed) -> EvidenceBundle`

The evidence layer should not own experimental perturbation semantics beyond producing a base bundle and stable lineage metadata.

### 12.3 `perturbation_operators`

Build vs buy note: keep perturbation semantics fully custom because they encode the experimental manipulation; no external package should define comparison-group meaning.

Responsibilities:

1. Transform a base evidence bundle or other task-linked inputs under a declared experimental operator.
2. Preserve lineage metadata linking the derived bundle back to its base bundle and operator instance.
3. Declare what properties the operator is intended to preserve and what dimensions it changes.

Interfaces:

1. `apply(task, base_bundle, operator_config, seed) -> PerturbedInput`
2. `describe_constraints() -> PerturbationConstraints`

### 12.4 `model_provider`

Build vs buy note: use the `openai` Python client against Ollama's OpenAI-compatible endpoint when possible, with `httpx` as a thin fallback transport; do not build a bespoke HTTP client stack.

The v1 harness uses local inference through Ollama, exposing an OpenAI-compatible API at a local endpoint.

Responsibilities:

1. Provide a uniform generation interface to agent modules.
2. Manage connection to the local Ollama instance.
3. Echo back resolved generation parameters for provenance logging.
4. Support optional JSON format mode when the model and prompt support it.

Interface:

```python
class ModelProvider:
    def generate(self, messages: list[dict], config: GenerationConfig) -> ModelResponse

class GenerationConfig:
    temperature: float
    top_p: float
    top_k: int | None
    seed: int | None
    max_tokens: int
    stop: list[str] | None
    format: str | None  # "json" or None

class ModelResponse:
    text: str
    model: str
    tokens_used: int
    generation_params: dict  # actual params applied, echoed for provenance
```

v1 model decisions:

1. One Ollama-hosted model at a fixed quantization serves as `local_model` in experiment configs. Multi-model comparison is post-v1.
2. The provider wraps Ollama's `/v1/chat/completions` endpoint. If a cloud API is needed later, a second provider implementation can be added without changes to the agent layer.
3. JSON format mode (`format: "json"`) may be enabled per agent configuration when the model supports it reliably, but agents must not depend on it — all agents must tolerate free-text output and fall back to prompt-based extraction.
4. Ollama's `seed` parameter provides deterministic output for the same model on the same hardware. This is the primary reproducibility mechanism at the model level.

Provenance fields logged per generation call:

1. model name as reported by Ollama, which encodes architecture and quantization (e.g. `llama3:8b-instruct-q5_K_M`)
2. Ollama server version
3. all decoding parameters: `temperature`, `top_p`, `top_k`, `seed`, `max_tokens`, `stop`
4. whether JSON format mode was requested
5. tokens consumed
6. immutable model digest or equivalent immutable model reference when available
7. a minimal environment fingerprint sufficient to distinguish exact reproduction from approximate reproduction across machines

### 12.5 `agents`

Build vs buy note: keep prompts, parsing strategy, artifact contracts, and normalization handoff custom; external libraries should be limited to model client and utility support.

Responsibilities:

1. Transform task plus evidence inputs into agent-specific prompts.
2. Call the model provider to execute generation.
3. Parse outputs into a common artifact envelope with schema-specific payloads.
4. Hand off raw artifacts to a registered normalizer when the agent does not emit a compatible normalized artifact directly.

Interfaces:

1. `run_agent(run_context) -> AgentResult`
2. `parse_output(raw_output) -> AgentArtifacts`
3. `describe_capabilities() -> AgentCapabilities`

The model provider is injected into `run_context`. Agents construct prompts and call `run_context.model.generate()`; they do not manage connections or decoding parameters directly.

Output format strategy:

1. All four agents produce free-text output by default. Prompt templates instruct the model to return structured content, but the harness does not depend on JSON mode for correctness.
2. When JSON format mode is enabled for a given agent-model combination and the model produces valid JSON, the normalizer may use it as a fast path. When JSON mode is unavailable or produces malformed output, the normalizer falls back to text extraction from the raw output.
3. This means the normalizer is the critical-path component for all agents, not only for `baseline_direct`. Normalizer reliability should be validated early in phase 1.

Minimum `AgentResult` contract for v1:

1. raw model output text
2. task-family-specific artifact payload
3. parse status
4. cited evidence identifiers when available
5. enough structured fields to support registered normalization
6. model provenance echoed from `ModelResponse`

Planned agent implementations:

1. `baseline_direct`
2. `retrieve_then_synthesize`
3. `option_generation`
4. `structured_conflict_preserving`

### 12.6 `metrics`

Build vs buy note: keep all metric logic custom; external packages such as `pandas` may help aggregate outputs, but they should not define scoring semantics.

Responsibilities:

1. Score protocol-materialized metric subjects using task annotations and canonical telemetry.
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

For v1, a metric's `ProjectionContract` must also declare its authoritative source view:

1. `attempts`: consume canonical attempt telemetry directly
2. `selected_runs`: consume only the deterministic selected-run view derived from attempts

When `selected_runs` is used, only records with `selection_role=metric_scoring` and `eligible_for_metric_scoring=true` may be materialized into metric subjects.

When a metric consumes `selected_runs`, it should be able to rely on the selected-run view exposing the same scoring-relevant normalized fields as the selected attempt record, not only an indirect pointer.

### 12.7 `normalizers`

Build vs buy note: keep normalizers fully in-house because the mapping from raw model output to task-defined identifiers is core benchmark IP.

Responsibilities:

1. Convert agent-specific artifacts into the stable normalized scoring family and active payload version.
2. Apply task-family-aware normalization rules without pushing benchmark logic into the core runner.
3. Mark normalization failures explicitly and preserve diagnostics.

Interfaces:

1. `normalize(task, agent_result, run_context) -> NormalizedArtifacts`
2. `supports(task_family, agent_config, artifact_schema) -> bool`

### 12.8 `study_protocols`

Build vs buy note: keep study protocols fully custom because grouping, admissibility, and unit-of-analysis rules are central experimental design choices.

Responsibilities:

1. Define the unit of analysis, grouping rules, rerun policy, and required controls for an experiment class.
2. Validate that an execution config satisfies protocol-specific requirements before runs are expanded.
3. Supply grouping and aggregation hints to metrics and reporting modules.

Interfaces:

1. `validate_experiment(config) -> ValidationResult`
2. `materialize_subjects(records, projection_spec) -> list[MetricSubject]`
3. `required_provenance() -> list[str]`
4. `declared_semantics() -> ProtocolSemantics`

Study protocols should be the sole authority for:

1. grouping persisted records into comparison units
2. validating grouped-subject completeness
3. deriving `comparison_group_id`, `case_id`, and related correlation metadata semantics
4. rejecting inadmissible partial groups before metric scoring begins

This keeps grouped metrics extensible without pushing protocol-specific branching back into the experiment runner or metric implementations.

The registered study protocol module is distinct from any optional `protocol_artifact` carried with an experiment. In v1, the module owns execution and grouping semantics; the artifact, when present, captures study-design intent for later scientific reuse and reporting.

For v1, `declared_semantics()` should expose the subset of protocol semantics that can participate in alignment checks, such as:

1. study type, when declared
2. unit of observation or analysis, when declared
3. unit of aggregation, when declared
4. primary metrics or endpoints, when declared
5. exclusion rules, when declared
6. aggregation plan, when declared
7. threats to validity or validity notes, when declared

To reduce operational drift, v1 should avoid duplicating scientific-semantic fields in experiment config. When `protocol_artifact` is present, it is authoritative for scientific semantics, and the validation path should compare it against the resolved execution semantics implied by `study_protocol`, emitting a visible `protocol_alignment_mismatch` flag when they disagree.

For v1 readiness behavior:

1. `analysis_label`, `target_use`, and `readiness_target` are the authoritative pre-execution workflow-intent inputs for v1 validation
2. when omitted, they default to `exploratory`, `benchmark`, and `executable`
3. benchmark, demo, or exploratory workflows with `readiness_target=executable` may omit `protocol_artifact` and `repro_bundle/`
4. any workflow with `analysis_label=confirmatory`, `target_use=paper_facing`, or `readiness_target=scientifically_interpretable` must provide `protocol_artifact`
5. any workflow with `analysis_label=confirmatory`, `target_use=paper_facing`, or `readiness_target` of `reproducible` or `scientifically_interpretable` must emit `repro_bundle/`

To preserve future scientific protocol modularity, study-protocol definitions should also allow optional declaration of:

1. study type
2. unit of assignment
3. unit of observation
4. unit of aggregation
5. primary estimand or comparison claim
6. exclusion rules
7. aggregation plan
8. threats to validity

For v1, these fields may be informational or defaulted. The important design choice is that the protocol object, not the runner, owns these semantics once they become enforced.

### 12.9 `telemetry`

Build vs buy note: use `orjson`, `pathlib`, and simple JSONL writers for persistence, but keep the telemetry envelope, lineage fields, and obligation semantics custom.

Responsibilities:

1. Normalize runtime artifacts into stable JSONL records.
2. Persist logs, raw outputs, and derived summaries.
3. Preserve compatibility between envelope fields and extensible payloads.
4. Preserve boundary-level step records needed to reconstruct judgment structure.

Interfaces:

1. `write_attempt_record(record, path)`
2. `write_selected_run_view(record, path)`
3. `write_step_record(record, path)`
4. `load_attempt_records(path) -> list[AttemptRecord]`
5. `load_selected_run_views(path) -> list[SelectedRunView]`

Selected-run views should be treated as derived caches or convenience views. They may be loaded directly when a metric's projection contract explicitly selects `selected_runs`, but they must remain regenerable from canonical attempt telemetry and the deterministic selection policy.

### 12.10 `experiments`

Build vs buy note: use `typer` or `click` for CLI entrypoints and standard scheduling/control flow in Python, but keep grid expansion, retry semantics, and protocol composition custom.

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

Build vs buy note: pipeline behavior, prompt structure, and expected artifacts should remain custom; only model invocation should rely on external client packages.

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
3. raw output or structured fields sufficient for normalization into the active normalized scoring family and payload version

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

For v1 benchmarking, all four agent configurations must be transformed into a common normalized scoring family before metric computation.

The stable normalized envelope should contain:

1. `schema`
2. `payload`
3. `diagnostics`
4. `unknown_mappings`

The initial benchmark payload version should be `decision_space_benchmark_normalized/v1`.

The minimum v1 payload should include:

1. `represented_frames`: normalized frame identifiers present in the final synthesis
2. `preserved_conflict_ids`: normalized conflict identifiers preserved in the synthesis
3. `generated_option_ids`: normalized candidate action identifiers
4. `selected_option_id`: selected action identifier when applicable
5. `final_answer_text`: final synthesized answer text
6. `cited_evidence_ids`: evidence items referenced by the answer when extractable
7. `parse_status`: `valid`, `partial`, or `invalid`

Identifier-bearing fields in this payload must resolve to task-defined `frame_id`, `conflict_id`, `option_id`, and `evidence_id` values when those constructs are present in the task family. When no valid mapping is available, the normalizer must emit an explicit unknown or null state rather than inventing a new identifier.

This normalized family is the scoring boundary for the initial benchmark slice. Raw agent artifacts remain available for diagnosis, but metric modules should not depend on agent-specific payload shapes.

Metric modules should instead declare the normalized fields they require through their projection contract. A metric must score only against the fields it explicitly requires rather than depending on the entire payload shape. This keeps field additions, removals, and renames more local to normalizers, adapters, and the affected metrics.

For v1 scoring, metric behavior must be deterministic across the attempt-level `normalization_state`:

1. `valid`: metric may score normally
2. `partial`: metric may score only if the fields required by that metric are present and all missing fields are recorded in diagnostics
3. `invalid`: metric must not emit a numeric score and must instead mark the result `unassessable` with an explicit obligation

Future task families may define additional normalized payload versions or adapters without requiring changes to the runner or telemetry envelope. For v1, the preferred compatibility mechanism is schema versioning plus adapters between payload versions rather than freezing one field list into all core modules.

## 14. Metric Definitions

Build vs buy note: keep primary metrics custom; optional supporting text diagnostics may reuse `scikit-learn` or similar utilities for tokenization or vectorization.

### 14.1 Conflict Retention Ratio

Definition:

`conflicts_preserved / source_conflict_count`

Interpretation:
higher is better; measures whether disagreement survives synthesis.

Scoring rules:

1. `conflicts_preserved` is the count of distinct normalized `preserved_conflict_ids`
2. the denominator is the count of distinct task-declared expected conflict identifiers for the scored task
3. duplicate mentions count once
4. unknown mappings do not contribute to the numerator
5. if the task declares no scorable conflicts, the metric is `unassessable`, not zero
6. if required normalized fields are missing, the metric is `unassessable`

### 14.2 Frame Preservation Score

Definition:

`represented_relevant_frames / total_relevant_frames`

Interpretation:
higher is better; measures whether multiple analytical frames survive.

Scoring rules:

1. the numerator is the count of distinct normalized `represented_frames` intersected with task-declared `relevant_frame_ids`
2. duplicate mentions count once
3. unknown mappings do not contribute to the numerator
4. if the task declares no relevant frames, the metric is `unassessable`, not zero
5. if required normalized fields are missing, the metric is `unassessable`

### 14.3 Option Breadth

Definition:

count of distinct generated candidate actions after normalization.

Interpretation:
higher is better up to task-reasonable bounds; detects option compression.

Scoring rules:

1. the score is the count of distinct normalized `generated_option_ids`
2. duplicate mentions count once
3. unknown mappings do not contribute to the count
4. when task-declared `candidate_option_ids` exist, reports should also include normalized coverage against that declared option set
5. if the task family does not define candidate actions or the required normalized fields are absent, the metric is `unassessable`

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
5. normalization-invalid attempt rate
6. bag-of-words Jaccard distance over `final_answer_text` across perturbation group pairs, reported alongside the primary path-dependence score as a prose-level divergence diagnostic — not a primary metric

## 15. Execution Flow

Build vs buy note: keep execution order, retry policy, and scoring-phase boundaries custom; use standard Python control flow rather than a workflow orchestration framework in v1.

### 15.1 Single Run

1. Load experiment configuration.
2. Resolve task set into tasks.
3. Expand a single run specification.
4. Materialize `cell_id`, `attempt_id`, and comparison metadata if the run belongs to a perturbation study.
5. Build base evidence bundle.
6. Apply a registered perturbation operator when required by the study protocol.
7. Execute the configured agent.
8. Emit or persist boundary step records for input, divergence if applicable, commit, and `attempt_summary`.
9. Normalize agent artifacts into the active benchmark normalized family and payload version.
10. Derive attempt-level assessability inputs and any review obligations that are knowable from the attempt in isolation.
11. Persist attempt outputs.

Single-run execution should not require the runner to score grouped metrics immediately. For v1, metric scoring is a separate phase over protocol-materialized subjects built from persisted records.

### 15.2 Full Experiment

1. Load experiment config.
2. Expand all combinations into run specs.
3. Execute runs sequentially in v1.
4. Persist one immutable canonical record per attempt and track the aggregate-selected attempt for each cell using the deterministic retry policy.
5. Derive selected-run views from canonical attempt telemetry using the deterministic attempt-selection policy.
6. Ask the study protocol to materialize admissible metric subjects from canonical attempt telemetry, using derived selected-run views only when a metric's projection contract explicitly declares `selected_runs` as its authoritative source view.
7. Ensure any selected-run view used for scoring includes only records marked `selection_role=metric_scoring` and `eligible_for_metric_scoring=true`.
8. Compute metrics as a post-pass over those materialized subjects. Immediate per-attempt scoring is optional only for metrics whose required subject is exactly one completed attempt.
9. Aggregate by task, case, family, agent, prompt, evidence provider, model, comparison group, and protocol-defined units as required by each metric.
10. Emit experiment-level `summary` outputs including aggregate tables, plots, and obligation summaries.

Experiment summaries should also reserve a separate readiness section so later methodology gates can be added without overloading execution or assessability states. For v1, this section may expose:

1. executable status
2. reproducible status
3. scientifically interpretable status as `not_evaluated` unless a stricter protocol layer is enabled

For v1, `reproducible` should not be reported as satisfied unless required provenance is complete and the experiment emitted or can export the declared `repro_bundle/` contents. Likewise, `scientifically_interpretable` should remain `not_evaluated` unless the workflow declares that target and passes the stricter protocol checks.

## 16. Output Artifacts

Build vs buy note: serialize outputs with `orjson` and analyze them with `pandas`; keep artifact schemas and subject/result semantics custom.

Each experiment should generate:

1. `attempts.jsonl` containing immutable canonical attempt records.
2. `runs.jsonl` containing derived selected-attempt run views, with one aggregate-selected full-view record per cell.
3. `metrics.jsonl` containing per-subject metric results.
4. `summary.json` containing aggregate statistics.
5. `failures.jsonl` for derived summaries of failed attempts, unassessable metric subjects, or selection outcomes that require explicit failure accounting.
6. optional `figures/` directory for report-ready charts.
7. conditionally required `repro_bundle/` containing experiment config, resolved `study_protocol` identifier, `protocol_artifact` when present or required, registry snapshot, environment manifest or equivalent metadata, task and annotation versions, and the canonical outputs needed to reproduce reported results.
8. `obligations.jsonl` containing assessability failures, compatibility issues, and review debt items.
9. optional `steps.jsonl` containing boundary step records when step-level tracing is enabled.

For v1 artifact semantics:

1. `attempts.jsonl` is the canonical persisted source of truth
2. `runs.jsonl` must be derivable from `attempts.jsonl` plus the deterministic attempt-selection policy
3. derived files must never introduce facts that cannot be traced back to canonical attempt telemetry
4. when a cell has at least one successful attempt, its selected-run view must point to the latest successful attempt and use `selection_role=metric_scoring`
5. when a cell has no successful attempt, its selected-run view may be present only for failure accounting and must use `selection_role=failure_accounting` and `eligible_for_metric_scoring=false`
6. each selected-run view should carry the selected attempt's full stable envelope and normalized artifacts in addition to `selected_attempt_id`, `selection_role`, and `eligible_for_metric_scoring`
7. `repro_bundle/` may be omitted only for workflows whose validated intent is exploratory, benchmark-or-demo use, and `readiness_target=executable`
8. when `repro_bundle/` is required, it should include or manifest-link the exact `attempts.jsonl` and `runs.jsonl` artifacts referenced by metrics and summaries

For v1, each metric result record should include at minimum:

1. `subject_type`
2. `subject_id`
3. `metric_id`
4. `metric_version`
5. numeric score or explicit `unassessable` status
6. diagnostics and obligation references

To keep later inferential and reporting upgrades additive, metric result records should also reserve optional fields for:

1. `study_type`
2. `unit_of_aggregation`
3. `analysis_label` such as `confirmatory`, `exploratory`, or `diagnostic`
4. `sample_size`
5. `exclusion_count`

These fields need not be populated universally in v1. When present, they should be sourced from authoritative workflow-intent fields such as `analysis_label`, from `protocol_artifact`, or from protocol-derived study metadata rather than duplicated experiment-config mirrors.

## 17. Configuration Strategy

Build vs buy note: use `PyYAML` plus `pydantic` or `pydantic-settings` for config loading and validation; keep override precedence and module resolution semantics in-house.

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
7. which workflow-intent requirements apply through `analysis_label`, `target_use`, and `readiness_target`

In v1, experiment config should avoid duplicating scientific-semantic fields that belong in `protocol_artifact`. Workflow-intent fields such as `analysis_label`, `target_use`, and `readiness_target` are allowed because they govern validation and artifact requirements rather than scientific content. When `protocol_artifact` is present, it takes precedence for scientific semantics, and any disagreement between it and the resolved execution semantics implied by `study_protocol` over the declared overlap set should surface as a `protocol_alignment_mismatch` validation flag before execution begins.

For reproducibility, each persisted attempt record must also record the resolved prompt template version, model identifier, immutable model reference when available, provider identifier, decoding settings, any seed actually applied at generation time, and enough environment metadata to distinguish exact from approximate reruns.

## 18. Validation and Testing Plan

Build vs buy note: use `pytest`, `pytest-cov`, and snapshot tooling such as `syrupy`; keep fixture design and acceptance criteria custom to the harness.

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
11. deterministic derivation of selected-run views from canonical attempt telemetry
12. `protocol_alignment_mismatch` detection when resolved execution semantics disagree with `protocol_artifact`
13. defaulting and validation of `analysis_label`, `target_use`, and `readiness_target`
14. required `protocol_artifact` presence for confirmatory, scientifically interpretable, or paper-facing workflows
15. required `repro_bundle/` emission rules for reproducible, confirmatory, or paper-facing workflows

### 18.2 Integration Tests

Required coverage:

1. one end-to-end run on a synthetic task
2. one multi-run experiment expansion
3. one path-dependence experiment with seeded shuffles
4. one newly added task family running without changes to the experiment runner
5. one traced run emitting input, divergence, commit, and `attempt_summary` step records, plus an experiment-level `summary` record
6. one experiment producing an `unassessable` outcome when required trace integrity is broken
7. one fixture-based experiment verifying expected metric ordering across known synthetic outputs
8. one grouped metric running through protocol-defined grouping without metric-specific runner branching
9. one derived `runs.jsonl` view matching the deterministic selection policy applied to `attempts.jsonl`
10. one experiment config that surfaces a `protocol_alignment_mismatch` flag when the resolved execution semantics disagree with `protocol_artifact`
11. one selected-run consumer reading a full-view `runs.jsonl` record without needing to chase attempt pointers for scoring fields
12. one strict workflow emitting a required `repro_bundle/` with the declared contents

### 18.3 Acceptance Tests

Release gates for v1:

1. `run_experiment` succeeds on a documented config.
2. output files are written to expected directories.
3. metrics are reproducible across repeated seeded runs.
4. fixture tasks with known expected relationships yield the documented metric ordering and diagnostics.
5. a new registered module can be added and exercised without modifying core orchestration code.
6. rerunning a failed cell preserves attempt history and yields one unambiguous aggregate result for that cell.
7. one path-dependence experiment scores from comparison-group metadata without ad hoc postprocessing.
8. step records make the attempt-level boundaries visible on at least one documented workflow and preserve a distinct experiment-level `summary` record.
9. harness statuses and summaries never use pass/fail language that could be mistaken for approval.
10. one metric that consumes grouped subjects can be added without changing runner logic.
11. regenerating `runs.jsonl` from `attempts.jsonl` yields the same selected-attempt view used in summaries and metrics.
12. a disagreement between resolved execution semantics and `protocol_artifact` is surfaced explicitly before execution and does not override the protocol artifact.
13. confirmatory, scientifically interpretable, or paper-facing workflows reject missing `protocol_artifact`.
14. workflows targeting reproducible, confirmatory, or paper-facing outputs emit `repro_bundle/` with environment metadata, task or annotation versioning, and the canonical outputs referenced by summaries and metrics.

## 19. Implementation Phases

Build vs buy note: package adoption should reduce v1 build cost, especially for schema, CLI, model client, serialization, analysis, and testing layers, while leaving the research core untouched.

### 19.0 v1 MVP Boundary

To keep the initial build aligned with the non-functional simplicity goal, v1 should explicitly include only:

1. sequential local execution
2. internal registries only
3. one normalized scoring family: `decision_space_benchmark_normalized`, with one initial payload version `v1`
4. two study protocols at most: `single_run` and `perturbation_group`
5. built-in aggregation and reporting modules behind stable interfaces
6. step-level tracing on at least one documented workflow, not necessarily on every run path

The following are post-v1 unless pulled forward by a concrete implemented use case:

1. dynamic third-party plugin loading
2. multiple normalized views derived from a more general core envelope
3. generalized reporter plugin infrastructure
4. generalized aggregation plugin infrastructure

### Phase 1: Foundations

Deliverables:

1. repository scaffold
2. typed schemas
3. task loader and validator
4. telemetry writer
5. 12 synthetic tasks
6. 5 real-document tasks
7. baseline direct pipeline
8. registry mechanism for task families, evidence providers, perturbation operators, study protocols, agents, metrics, and normalizers
9. one v1 normalizer that produces `decision_space_benchmark_normalized/v1`
10. fixture tests for normalization states, unknown mappings, and unassessable metric outcomes

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

Build vs buy note: package choices should explicitly mitigate overbuilding and reproducibility risk; avoid adopting frameworks that add hidden state, opaque conventions, or unnecessary plugin complexity.

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

Build vs buy note: concrete package recommendations for v1 are `pydantic`, `PyYAML`, `openai`, `orjson`, `typer`, `pytest`, and `pandas`, with `pluggy` and `scikit-learn` deferred unless justified by implemented use cases.

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
13. Use Ollama for local inference behind a thin `ModelProvider` abstraction. One model at a fixed quantization for v1.
14. Treat all agent output as free text by default. JSON format mode is an optional fast path, not a correctness dependency.
15. Retain all raw model output in telemetry. Local inference removes cost and privacy constraints on output logging.
16. Log Ollama model name, server version, and all decoding parameters with every generation call for provenance.

## 22. Open Questions

Build vs buy note: unresolved questions about evidence provision, annotation standards, and extension modules are custom design questions, not package-selection questions.

These decisions should be resolved before implementation begins in earnest:

1. ~~Which exact model interfaces will v1 support?~~ **Resolved.** v1 uses Ollama local inference via an OpenAI-compatible endpoint, wrapped in a thin `ModelProvider` abstraction. See section 12.4.
2. Will evidence provision be simulated from task-local documents only, or include embeddings and precomputed bundles?
3. ~~How will output divergence be measured for path dependence?~~ **Resolved.** v1 uses Jaccard distance over normalized artifact sets (`represented_frames`, `preserved_conflict_ids`, `generated_option_ids`) plus binary disagreement over `selected_option_id`, as specified in section 14.4. Lexical similarity and judge-model scoring are post-v1 extensions. Bag-of-words Jaccard over `final_answer_text` may be added as a supporting diagnostic but is not a primary metric.
4. ~~How much raw model output should be retained for reproducibility versus cost or privacy?~~ **Resolved.** Local inference eliminates cost and privacy concerns. All raw model output should be retained.
5. What is the minimum annotation standard for real-document tasks?
6. Which first extension module should be used to test modularity beyond the initial benchmark family?
7. ~~Which concrete model settings must be persisted to make reruns meaningfully reproducible across providers?~~ **Resolved.** See section 12.4 provenance fields and section 10.7 provenance namespaces. v1 should persist the concrete model identifier, immutable model reference when available, decoding parameters, seed, and environment metadata needed to distinguish exact from approximate reruns.

## 23. Immediate Next Steps

Build vs buy note: the first implementation pass should adopt external packages only where they collapse boilerplate immediately, especially schema validation, config loading, model calls, JSONL writing, CLI, and testing.

1. Convert this plan into repository issues or milestones.
2. Scaffold the repository structure and package layout.
3. Implement schemas for base tasks, family annotations, experiments, telemetry envelopes, and artifact payloads first.
4. Implement the registry mechanism before adding multiple pipelines.
5. Add a minimal end-to-end runner with one synthetic fixture task.
6. Lock the first experiment config around conflict retention before broadening scope.
7. Add one extra task family beyond the original four to validate extensibility early.
8. Add one documented traced workflow showing input, divergence, commit, and `attempt_summary` boundaries per attempt, plus an experiment-level `summary`.
9. Finalize the grouped metric subject contract before implementing path-dependence scoring.
10. Define the module resolution algorithm before adding non-core modules.
11. Keep the v1 implementation on one normalized scoring family with one initial payload version, while allowing later payload-version adapters without changing core orchestration.

## 24. Acceptance Summary

Build vs buy note: acceptance should judge whether the in-house scientific core remains clear and reproducible while external packages stay confined to commodity infrastructure.

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

---

For the post-v1 scientific methodology reference (experiment classes, scientific validity gates, inference and validation requirements), see `scientific_methodology_reference.md`.
