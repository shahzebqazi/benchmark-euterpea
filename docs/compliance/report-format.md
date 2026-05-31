# Report Format

Public reports live in `data/reports`.

`latest.json` contains:

- `schema_version`
- `generated_at`
- `source_run_count`
- `results`

Each result includes:

- `task_id`
- `model`
- `runs`
- `passed`
- `failed`
- `pass_rate`
- `answer_distribution`
- `failure_distribution`
- `latency_ms_avg`
- `batch_ids`

The GitHub Pages hiscores page renders this file without changing the reported data.
