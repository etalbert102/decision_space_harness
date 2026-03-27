# Decision Space Harness

Phase 3 implementation of the decision space harness.

Current slice:

- one synthetic task family
- one baseline direct agent
- one heuristic model provider
- one normalizer producing `decision_space_benchmark_normalized/v1`
- `single_run` and `perturbation_group` study protocols
- primary metrics for conflict retention, frame preservation, option breadth, and path dependence
- one lexical Jaccard extension metric
- canonical `attempts.jsonl` plus derived `runs.jsonl`
- optional `message_records.jsonl` for future A2A or multi-agent communication traces
- analysis outputs via `summary_table.json`, `summary_table.csv`, and `figures/metric_means.txt`

Run the sample experiment with:

```bash
source .venv/bin/activate
PYTHONPATH=src python -m decision_space_harness.experiments.runner experiments/configs/conflict_smoothing_v1.yaml
```

Run tests with:

```bash
source .venv/bin/activate
PYTHONPATH=src pytest
```
