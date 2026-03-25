# DecisionSpace Harness Scientific Methodology Reference

This document contains the post-v1 scientific methodology appendices extracted from the original technical specification plan. It informs schema and registry design choices but does not expand the required v1 build.

For the v1 build specification, see `technical_specification_plan_v1.md`.

## 25. Experiment Classes and Scientific Validity Addendum

This section is an appendix. It informs post-v1 design and schema choices, but it does not expand the required v1 build beyond the MVP boundary defined earlier.

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

This section is also an appendix. It describes later methodological requirements and should not be read as mandatory v1 implementation scope unless a later phase explicitly promotes a requirement into core.

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
