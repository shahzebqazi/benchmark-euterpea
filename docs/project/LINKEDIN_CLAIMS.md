# LinkedIn Claim Map

This file maps external application claims to repository proof. It is repo evidence only; do not edit LinkedIn materials from this workstream.

| External claim | Repo proof path |
| --- | --- |
| Original benchmark suite for model competence and agent compliance | `README.md`, `tasks/README.md`, `tasks/*/*/*/metadata.json` |
| Deterministic grading | `tasks/*/*/*/verifier.py`, `scripts/validate_repo.py`, `tests/fixtures/verifiers/*.json` |
| Verifier regression checks include negative cases | `tests/fixtures/verifiers/c-major-fifth.json`, `tests/fixtures/verifiers/json-only-status.json`, `scripts/validate_verifier_fixtures.py` |
| Expected answers stay outside prompts | `ARCHITECTURE.md`, `scripts/validate_repo.py`, `tasks/*/*/*/instruction.md` |
| Run provenance | `ARCHITECTURE.md`, `scripts/run_task.py`, `data/reports/latest.json` |
| Raw vs derived data boundary | `.gitignore`, `data/reports/README.md`, `scripts/summarize_runs.py` |
| Curated reports with pass rates, distributions, latency, batch ids, and source paths | `data/reports/latest.json`, `scripts/summarize_runs.py` |
| GitHub Pages hiscores | `scripts/build_site.py`, `docs/site/dist/hiscores.html` after local build, post-push URL `https://shahzebqazi.github.io/benchmark-euterpea/hiscores.html` |
| Issue-driven task intake | `.github/ISSUE_TEMPLATE/new-task.yml`, `docs/agentic/branch-and-review-policy.md` |
| CI and PR guardrails | `.github/workflows/ci.yml`, `.github/workflows/pr-policy.yml`, `.github/pull_request_template.md` |

## Current Evidence Boundary

The current curated report includes four model names, but only `llama3.2:3b` covers the full 13-task executable suite. `gemma3:1b`, `granite3.2:2b`, and `phi4-mini` currently cover `c-major-fifth` only. Local Ollama is blocked in this environment, so any external claim should say "curated snapshot" and avoid implying a complete four-model full-suite baseline until the operator runs the optional matrix in `docs/agentic/PRE_PUSH_CHECKLIST.md`.
