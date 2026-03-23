
Final Artifact
Name
DecisionSpace Harness
One-sentence description
An evaluation harness for measuring how LLM-agent pipelines reshape the space of interpretations and actions when synthesizing evidence.

What Makes This High ROI
It demonstrates exactly the skills this type of role hires for:
Capability
Demonstrated by
Agent harness design
Multiple agent pipelines
Quantitative benchmarking
Reproducible tasks + metrics
Automated evaluation
Config sweep runner
Prompt sensitivity analysis
Prompt variants
Pipeline diagnostics
Structural metrics

This is stronger than typical candidate projects, which are usually:
chatbots
simple tool-use demos
prompt engineering notebooks

Core Concept
Most AI evals measure:
Did the model get the answer right?
OptionSpace Bench measures:
Did the system preserve meaningful alternatives before converging on an answer?
The artifact detects three structural failure modes:
Conflict smoothing — disagreement disappears
Frame collapse — problems reduced to a single perspective
Path dependence — early retrieval choices dominate outcome
These are measurable properties of agent pipelines, not just model accuracy.

System Architecture
Pipeline
Task
  → Evidence retrieval
  → Agent pipeline
  → Telemetry logging
  → Metric scoring
  → Aggregate evaluation


Benchmark Design
Total tasks
40–50 tasks
Split across:
Task type
Count
Synthetic structured tasks
30–35
Real document tasks
10–15

This is enough to look credible without exploding scope.

Task Family 1 — Conflict Preservation
Evidence contains legitimate disagreement.
Example:
Source A: recommend policy X
Source B: warns X creates risk Y
Source C: recommends alternative Z

Failure mode:
System outputs false consensus.

Task Family 2 — Frame Diversity
Evidence represents different causal frames.
Example frames:
legal
operational
economic
political
technical
Failure mode:
Model collapses problem into one dominant frame.

Task Family 3 — Retrieval Path Dependence
Different retrieval bundles produce different evidence ordering.
Failure mode:
Small retrieval perturbations produce large answer changes.

Real-Document Tasks
Sources:
news articles
think tank reports
policy briefs
technical reports
Manual annotation:
relevant_frames
conflict_points
candidate_actions

Only 10–15 tasks required.
Purpose:
Prevent the benchmark from looking artificial.

Agent Pipelines
Use four configurations.
1. Direct synthesis baseline
Evidence → answer

Purpose:
Simplest comparison.

2. Retrieve-then-synthesize
Retriever → top-k evidence → answer

Purpose:
Standard RAG pipeline.

3. Option-generation agent
Pipeline:
Evidence
→ generate candidate options
→ select option
→ answer

Purpose:
Encourages broader reasoning.

4. Conflict-preserving structured agent
Pipeline:
Evidence
→ list frames
→ list disagreements
→ generate options
→ select option
→ answer

Purpose:
Designed to preserve decision space.

Prompt / Configuration Evaluation
This is what makes the system look like eval infrastructure.
Each experiment sweeps across:
Prompt variants
default
structured reasoning
explicit disagreement preservation

Retriever settings
top-5
top-10

Models
Use 1–2 models max.
Example:
local open model
stronger API model
Do not build a large model matrix.

Telemetry Logging
Each run logs:
task_id
task_family
agent_config
prompt_variant
retriever_config
model
retrieved_docs
retrieved_frames
source_conflict_count
generated_options
final_answer
selected_option
conflicts_preserved
minority_frame_survived

Format:
JSONL

This is standard for eval pipelines.

Metrics
Keep metrics simple and interpretable.
1. Conflict Retention Ratio
conflicts_preserved / source_conflicts

Detects conflict smoothing.

2. Frame Preservation Score
Number of relevant frames represented after synthesis.
Detects frame collapse.

3. Option Breadth
Number of distinct candidate actions generated.
Detects option compression.

4. Path Dependence
Output variance under retrieval shuffle.
Detects hidden authority of early evidence.

Key Experiment
The most important result should show:
structured agents reduce decision-space compression.
Example output:
Agent
Conflict Retention
Baseline
0.28
Structured agent
0.61

This communicates the mechanism immediately.

Secondary Experiment
Retrieval perturbation
Shuffle retrieval order.
Measure output variance.
Expected pattern:
baseline variance > structured agent variance

This demonstrates path dependence reduction.

Repo Structure
optionspace-bench/
  README.md
  configs/
  data/
  src/
    tasks/
    agents/
    retrieval/
    metrics/
    runners/
    telemetry/
  notebooks/
  reports/
  outputs/

The repository should look clean and reproducible.

Four-Week Execution Plan
Week 1 — Foundations
Deliver:
repo scaffold
task schema
telemetry schema
12 synthetic tasks
5 real-document tasks
baseline pipeline running
Success condition:
One task runs end-to-end.

Week 2 — Agents and sweeps
Deliver:
all four agent pipelines
prompt/config sweep runner
20–25 total tasks
Success condition:
Grid experiments run automatically.

Week 3 — Metrics and experiments
Deliver:
all four metrics
retrieval perturbation experiment
first figures
Success condition:
One clear result appears.

Week 4 — Expansion and polish
Deliver:
40–50 tasks
README
technical report
reproducible experiment
polished figures
Success condition:
Reviewer can clone repo and run demo.

The One Claim the Report Should Make
Keep it narrow.
Recommended claim:
Agent pipelines that focus on answer synthesis can silently compress the space of interpretations and actions available to human decision-makers. Structured conflict-preserving workflows measurably retain more disagreement, frame diversity, and candidate options.
This claim is:
defensible
mechanism-level
aligned with your broader work

Interview-Ready Explanation
If asked what the artifact does:
You can say:
Most evaluation frameworks measure answer quality. This harness evaluates whether agent pipelines preserve the space of possible interpretations and actions before converging. That structural property is invisible to accuracy metrics but important for systems used in analysis or decision support.
That explanation is strong and concise.

Biggest Execution Risks
Overbuilding the system
Too many tasks
Complicated metrics
UI distractions
Avoid all of these.

Final Recommendation
Build OptionSpace Bench as:
a multi-task benchmark
an agent comparison harness
a prompt/configuration eval system
a decision-space telemetry framework
This combination produces the strongest possible artifact per unit effort for an agent/evals research role while also reinforcing your longer-term work on decision-space preservation.
Goal: Add a short addendum to the existing OptionSpace Bench plan that ensures the system functions as reusable experimental infrastructure (not just a benchmark). The addendum introduces two elements: an explicit experiment layer and task structure metadata. These changes require minimal engineering but allow the same harness to power multiple empirical studies.

Addendum: Experimental Infrastructure Layer
This addendum ensures OptionSpace Bench functions as a general experimental platform for studying structural properties of LLM reasoning pipelines, rather than a single benchmark.
Two additions close this gap:
Explicit experiment configuration layer
Task metadata describing evidentiary structure
Both allow new studies to run through configuration changes rather than code changes.

1. Experiment Configuration Layer
Experiments become a first-class concept in the system.
Previously the harness runs combinations of tasks, agents, prompts, and retrievers. The experiment layer defines which combinations correspond to a specific empirical study.
Experiment configuration file
Example:
experiment: conflict_smoothing

task_set: conflict_tasks

agents:
  - baseline
  - structured_conflict_preserving

prompt_variants:
  - default
  - disagreement_prompt

retriever_variants:
  - top5
  - top10

metrics:
  - conflict_retention
  - option_breadth

The experiment runner expands the grid automatically.
This creates a reproducible experimental pipeline:
Experiment
→ task selection
→ configuration grid
→ batch execution
→ metric aggregation


2. Task Metadata for Evidentiary Structure
Tasks must contain explicit metadata describing the structure of evidence.
This enables structural metrics to generalize across experiments.
Required metadata fields
Each task definition should include:
{
  "task_id": "policy_04",
  "query": "...",
  "documents": [...],

  "frames": ["legal", "economic", "operational"],

  "conflict_clusters": [
    ["doc1", "doc3"],
    ["doc2", "doc4"]
  ],

  "candidate_actions": [
    "policy_X",
    "policy_Y",
    "hybrid_option"
  ]
}

Field meanings:
Field
Purpose
frames
distinct analytical perspectives represented
conflict_clusters
groups of documents expressing opposing claims
candidate_actions
valid action space implied by the evidence

These annotations enable the harness to compute structural metrics.

3. Experiment Types Enabled by This Layer
With the experiment layer and task metadata, the same infrastructure supports multiple empirical studies.
Conflict Smoothing
Configuration:
tasks = conflict_tasks
metric = conflict_retention

Measures how disagreement changes during synthesis.

Schema Lock
Configuration:
tasks = frame_diversity_tasks
metric = frame_preservation

Measures collapse of analytical perspectives.

Retrieval Cascade
Configuration:
tasks = cascade_tasks
retrieval_order = permuted
metric = path_dependence

Measures sensitivity to evidence ordering.

Decision-Space Erosion
Configuration:
tasks = option_space_tasks
agents = baseline vs structured
metric = option_breadth

Measures collapse of candidate action space.

4. Experiment Runner Extension
Add an experiment runner module:
src/experiments/
    runner.py
    configs/

Execution example:
python run_experiment.py experiments/conflict_smoothing.yaml

The runner will:
load experiment configuration
generate configuration grid
execute runs
collect telemetry
compute metrics
output experiment results

5. Repository Update
Add experiment infrastructure to the repo structure.
optionspace-bench/
  experiments/
      configs/
      runner.py
  data/
      tasks/
  src/
      agents/
      metrics/
      telemetry/

Experiments become configuration files stored under experiments/configs.

6. Resulting System Architecture
After this addition the system becomes:
Task environment
→ Experiment configuration
→ Agent pipeline
→ Telemetry logging
→ Structural metrics
→ Experiment results

New studies require only:
new task set
or
new experiment config

No changes to the harness itself.

7. Strategic Outcome
With this addendum OptionSpace Bench functions simultaneously as:
Agent evaluation infrastructure
benchmarking agent pipelines
prompt/configuration evaluation
Empirical research platform
conflict smoothing experiments
schema lock experiments
retrieval cascade experiments
decision-space erosion experiments
The same infrastructure can support multiple papers and experimental studies.

Final Principle
The system should always be designed so that new experiments require configuration changes rather than code changes.
This ensures OptionSpace Bench remains a reusable research platform rather than a one-off benchmark.

