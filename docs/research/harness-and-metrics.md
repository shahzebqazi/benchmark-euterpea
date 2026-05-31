# Harness And Metrics

The canonical local harness is `scripts/run_task.py` against Ollama `/api/generate`.

## Required Run Fields

- `schema_version`
- `run_at`
- `batch_id`
- `sample_index`
- `task_id`
- `task_metadata`
- `model`
- `harness`
- `ollama_options`
- `prompt`
- `raw_answer`
- `passed`
- `failure_reason`
- `latency_ms`
- `ollama_metrics`

## Comparison Rules

- Use the same task prompt for every model.
- Use the same sample count for every model in a report.
- Record temperature, seed, and token limits.
- Report pass rate and answer distribution.
- Treat failures as benchmark data, not noise.
