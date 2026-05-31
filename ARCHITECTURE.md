# Architecture

`benchmark-euterpea` is a small benchmark data platform slice. The current implementation is local and file-based, but the contracts are written so the same lifecycle can grow into queue-backed workers, durable storage, verifier regression, and researcher-facing dashboards.

## Runner Flow

1. `scripts/run_task.py` receives a model name, task directory, sampling options, repeat count, and batch id.
2. The runner validates the task directory contains `instruction.md`, `metadata.json`, and `verifier.py`.
3. It reads only `instruction.md` as the model-facing prompt.
4. It loads task metadata and imports the verifier module.
5. It calls Ollama `/api/generate` with fixed options for the sample.
6. It passes the raw model response to `verify(answer)`.
7. It writes one immutable raw run JSON file under `data/runs/`.
8. `scripts/run_batch.py` discovers task directories and invokes `run_task.py` for each task.
9. `scripts/summarize_runs.py` reads raw runs and writes `data/reports/latest.json`.
10. `scripts/build_site.py` turns the derived report and task metadata into `docs/site/dist/`.

## Task Directory Contract

```text
tasks/<capability>/<complexity>/<task-id>/
  instruction.md
  metadata.json
  verifier.py
```

`instruction.md` is the only prompt text shown to the model. It should not contain the expected answer unless the task is explicitly an exact-copy compliance task.

`metadata.json` records task identity and review context:

- `id`
- `capability`
- `complexity`
- `domain`
- `expected_answer`
- `expected_behavior`
- `expected_failure_modes`
- `contamination_risk`
- optional description fields

`verifier.py` owns correctness. It must expose:

```python
def verify(answer: str) -> tuple[bool, str | None]: ...
```

A pass returns `(True, None)`. A failure returns `(False, reason)` with a useful reason for debugging.

## Verifier Boundary

The verifier grades observable behavior, not intent or prose quality. It may normalize case and whitespace when the task contract allows that, but it should reject output that violates the contract: extra prose, invalid JSON, wrong spelling, wrong delimiter, multiple answers, or an easier enharmonic substitute.

Expected answers live in metadata and verifier code, not prompts. This makes prompt leakage detectable and keeps task correctness auditable.

## Raw Run JSON Schema

Each raw run is one model response. Current schema version: `1`.

Important fields:

- `schema_version`
- `run_at`
- `batch_id`
- `sample_index`
- `task_id`
- `task_path`
- `task_metadata`
- `model`
- `harness`
- `ollama_url`
- `ollama_options`
- `prompt`
- `raw_answer`
- `passed`
- `failure_reason`
- `latency_ms`
- `ollama_metrics`

Raw runs are source data. They are allowed to include awkward or failed model behavior because that behavior is the evidence.

## Derived Report Schema

`data/reports/latest.json` is a curated derived artifact generated from raw runs. Current schema version: `1`.

Top-level fields:

- `schema_version`
- `generated_at`
- `source_run_count`
- `results`

Each result groups a `(task_id, model)` pair and includes:

- `task_id`
- `model`
- `task_metadata`
- `runs`
- `passed`
- `failed`
- `pass_rate`
- `answer_distribution`
- `failure_distribution`
- `latency_ms_avg`
- `batch_ids`
- `source_files`
- `model_options`

Derived reports should be reproducible from raw runs and should preserve enough provenance to inspect surprising scores.

## Provenance Fields

Minimum provenance for a run:

- task id and source path
- prompt text actually shown to the model
- metadata snapshot at run time
- model name
- harness name
- Ollama options
- batch id and sample index
- timestamp
- raw answer
- verifier decision and failure reason
- latency and available Ollama timing metrics

Minimum provenance for a report:

- source run count
- batch ids
- source run files
- model/options samples
- generation timestamp

## Failure Handling

A benchmark failure is not a harness failure. `run_task.py` exits `1` when any sample fails so CI or shell workflows can notice, but it still writes completed run artifacts before returning. It exits `2` for harness errors such as missing task files, invalid metadata, verifier import errors, malformed verifier return values, Ollama request failures, or write collisions. `run_batch.py` preserves that boundary across tasks: `1` means one or more benchmark samples failed, while `2` means one or more task runs hit a harness/runtime error.

Failure reasons should teach something. Good reasons distinguish knowledge gaps, symbolic spelling errors, output-format violations, instruction violations, ambiguous prompts, and infrastructure errors.

## Validation And CI

`python3 scripts/validate_repo.py` checks:

- task metadata has required fields
- task ids are unique
- task directories contain prompt, metadata, and verifier
- verifiers import and satisfy the return contract
- verifiers accept their own metadata `expected_answer`
- non-copy prompts do not obviously contain expected answers
- derived report shape is valid

CI compiles Python files, validates the repository, regenerates the report, and builds the site. It intentionally avoids requiring Ollama so pull requests stay lightweight.

## Scaling Path

The current local file layout can scale without changing task semantics:

- Replace direct Ollama calls with worker jobs.
- Put task definitions and run requests into a queue.
- Store raw run artifacts in object storage.
- Index runs in a database by task, model, batch, verifier version, and timestamp.
- Run verifier regression suites whenever verifiers change.
- Add reviewer workflows for task proposals, contamination review, and failure-corpus promotion.
- Publish dashboards from derived reports rather than raw mutable state.
- Add access controls and retention rules for private runs.

## Reliability Risks And Mitigations

- Prompt leakage: expected answers stay outside prompts; validation catches obvious leaks.
- Verifier bugs: verifier contract smoke tests require the metadata expected answer to pass; future fixtures should add negative cases.
- Overclaiming from small samples: docs and site call reports curated snapshots, not final leaderboards.
- Raw/derived confusion: raw runs live in `data/runs`; reports and site are generated derived artifacts.
- Non-reproducible scores: run artifacts capture model, options, prompt, batch id, timestamp, and task metadata.
- Task contamination: task proposals document contamination risk and avoid copied exercise wording.
- Harness fragility: local CI avoids Ollama dependency and validates repository contracts independently of model availability.
