# benchmark-euterpea

`benchmark-euterpea` is a small original benchmark data-platform slice for evaluating model competence and agent compliance under deterministic grading.

The repo is intentionally modest in scale, but complete in shape: task definitions, deterministic verifiers, local Ollama runners, immutable raw run artifacts, derived reports, validation checks, methodology docs, and a generated engineer-facing report site. Music theory is the first controlled domain because it has symbolic correctness, easy-to-audit failures, and a path into Haskell/Euterpea solver tasks. The SWE story is the data pipeline: provenance, contracts, raw-vs-derived data, repeatable summaries, and clear failure handling.

This is not a prompt-engineering project. Prompts are kept short and stable; expected answers live outside prompts in metadata and verifier code. The goal is benchmark integrity and reproducible evaluation behavior, not making weak models score higher.

## Quick Start

Run one task against a local Ollama model:

```bash
python3 scripts/run_task.py --model llama3.2:3b --task-dir tasks/music-theory/basic/c-major-fifth --repeat 3 --batch-id local-task-smoke
```

Run the full executable batch:

```bash
python3 scripts/run_batch.py --model llama3.2:3b --repeat 1 --batch-id local-batch-smoke
```

Summarize raw runs into a curated derived report:

```bash
python3 scripts/summarize_runs.py --batch-id local-batch-smoke
```

Build the static report site:

```bash
python3 scripts/build_site.py
```

Validate task contracts, verifier contracts, prompt leakage checks, and report shape:

```bash
python3 scripts/validate_repo.py
```

View the generated site locally by opening:

```text
docs/site/dist/index.html
```

Public report:

- GitHub Pages report: https://shahzebqazi.github.io/benchmark-euterpea/
- GitHub Pages hiscores: https://shahzebqazi.github.io/benchmark-euterpea/hiscores.html
- Curated JSON report: `data/reports/latest.json`
- Architecture: `ARCHITECTURE.md`
- Findings: `docs/research/findings.md`

## Task Lifecycle

1. Propose a task through GitHub Issues with capability, verifier idea, contamination risk, and expected failure modes.
2. Add `instruction.md`, `metadata.json`, and `verifier.py` under `tasks/<capability>/<complexity>/<task-id>/`.
3. Keep the model-facing prompt in `instruction.md`; keep expected answers in metadata and verifier code.
4. Run one task or a batch through the Ollama runner.
5. Preserve raw run JSON in `data/runs/` with prompt, model, options, raw answer, pass/fail, failure reason, latency, batch id, and source path.
6. Summarize curated runs into `data/reports/latest.json`.
7. Build the static report site from repository data.
8. Promote repeated failures into the failure corpus, verifier regression cases, or new task proposals.

## Current Scope

The suite includes deterministic tasks across three capability areas:

- Symbolic music theory: scale degrees, relative keys, key signatures, enharmonic traps, and chord spelling.
- Agent compliance: exact output, JSON-only output, and multi-step instruction following.
- Euterpea/Haskell stubs: symbolic pitch transposition and duration reasoning over Euterpea-like representations.

See `tasks/README.md` and the generated task catalog for the current task list.

## Data Model

Raw local runs are source data. Public reports are curated derived artifacts.

- Raw run files in `data/runs/` contain one model response and all provenance needed to debug it.
- Derived reports in `data/reports/` aggregate model/task pass rates, answer distributions, failure distributions, latency averages, batch ids, source files, and model/options samples.
- The static site in `docs/site/dist/` is generated from the derived report and task metadata.

## Repository Layout

- `tasks/`: benchmark task contracts: prompt, metadata, verifier.
- `scripts/run_task.py`: one-task Ollama runner that writes immutable JSON run artifacts.
- `scripts/run_batch.py`: batch runner over discovered tasks.
- `scripts/summarize_runs.py`: raw-to-derived report generator.
- `scripts/validate_repo.py`: metadata, verifier, prompt leakage, and report validation.
- `scripts/build_site.py`: static engineer-facing report site generator.
- `data/runs/`: raw run artifacts.
- `data/reports/`: curated derived reports.
- `docs/research/`: methodology, contamination, verifier quality, provenance, failure corpus, and findings.
- `.github/workflows/ci.yml`: lightweight validation for task/report/site integrity.
- `.github/ISSUE_TEMPLATE/new-task.yml`: task backlog intake.

## Methodology Anchors

- Original prompts and task variants; no copied quiz bank.
- Expected answers stay outside prompts.
- Deterministic strict grading with explicit failure reasons.
- Raw failures are preserved as evaluation data, not discarded as noise.
- Public reports are curated snapshots with provenance, not claims of broad model ranking.
- Music is the first controlled domain, not the product boundary.

## Scaling Path

The current repo is a local slice. The same contracts can scale into workers, queues, object storage, database-backed run indexes, verifier regression suites, dashboards, reviewer workflows, and researcher-facing task triage without changing the core boundary: prompt in, raw model output out, deterministic verifier decides, provenance stays attached.
