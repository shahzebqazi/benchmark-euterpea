# AGENTS.md

## Purpose

This repo is a small original benchmark suite for evaluating model competence and agent compliance under deterministic grading. Music theory is the first controlled domain because it has symbolic correctness, easy-to-audit failures, and a path into Haskell/Euterpea solver tasks.

The repo is a genuine benchmark data-platform slice, not a music toy or prompt-engineering experiment. The project emphasizes task lifecycle, deterministic verifiers, raw vs derived data, run provenance, validation, CI, reporting, failure corpus, and a scaling path to researcher tooling.

## Product Direction

- Keep the benchmark integrity story stronger than the music identity.
- Improve runner/report correctness before adding volume.
- Add verifier fixtures and multi-model Ollama matrix runs.
- Grow music theory breadth only with deterministic, auditable tasks.
- Bring in Euterpea/Haskell solver tasks after direct-answer and symbolic-reasoning coverage are stable.

## Methodology

- Use original tasks.
- Keep expected answers out of the model prompt.
- Verify deterministic behavior, not prose quality.
- Encode accepted answers explicitly.

## Stack

- Python harness.
- Ollama first.
- JSON results in `data/runs` first.
- Haskell/Euterpea later.

## Documentation Style

- Be direct.
- Cut filler.
- Prefer concrete next steps over positioning language.
- Frame the project as evaluation infrastructure for music-domain model competence, not as a novelty demo.

## Branch And Review Policy

AI coding agents must not work directly on `main`. Use scoped branches and merge through PRs:

- `feature/<short-name>` for new benchmark/platform capabilities.
- `bugfix/<short-name>` for behavior corrections.
- `docs/<short-name>` for documentation-only changes.
- `tests/<short-name>` for validation fixtures and CI checks.
- `audit/<short-name>` for repo-wide reviews and cleanup plans.
- `ui/<short-name>` for site/report presentation work.
- `chore/<short-name>` for mechanical maintenance.

See `docs/agentic/branch-and-review-policy.md`. PRs must pass auto-review checks and request human approval when verifier behavior, report schema, CI/deploy/security, raw data publication, or public claims change.

## Guardrails

- Do not commit changes unless explicitly asked.
- Do not merge to `main` without a PR and human approval.
- Do not optimize prompts to make weak models pass.
- Do not add a broad leaderboard, cloud deployment, or heavy UI before the runner/report schemas are stable.
- Do not store API keys, Ollama endpoint secrets, credentials, or generated private traces in git.
- Never write code merely to impress people.

