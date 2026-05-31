# Harness And Metrics

The canonical harness is `scripts/run_task.py` against Ollama `/api/generate`. It defaults to local Ollama at `http://localhost:11434`, and can also target an authenticated remote Ollama host with `--ollama-url` plus an API key loaded from the environment or `~/.env`.

## Required Run Fields

- `schema_version`
- `run_at`
- `batch_id`
- `sample_index`
- `task_id`
- `task_metadata`
- `model`
- `harness`
- `ollama_url`
- `ollama_auth`
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
- Default benchmark runs use 10 samples per task/model. Use `--repeat 1` only for smoke checks.
- Record temperature, seed, and token limits.
- Report accuracy, pass/fail counts, and answer distribution.
- Treat failures as benchmark data, not noise.

## Authenticated Ollama Hosts

Set `OLLAMA_API_KEY` in the shell or in `~/.env` before running an API-backed benchmark. The runner sends the key as a bearer token when present, but records only the environment variable name in raw run artifacts.

Use `--ollama-url https://ollama.com` for direct Ollama Cloud runs. If the configured URL already ends in `/api`, the runner calls `/generate` under that path; otherwise it calls `/api/generate`.
