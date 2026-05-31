# PRD: benchmark-euterpea

## 1. Summary

`benchmark-euterpea` is a small original benchmark data-platform slice for evaluating model competence and agent compliance under deterministic grading. Music theory is the first controlled domain because symbolic answers are easy to audit, failures are interpretable, and the path extends into Haskell/Euterpea solver tasks.

The product is evaluation infrastructure, not a music quiz app or prompt-tuning experiment.

## 2. Current product (shipped locally)

- **Task contracts:** `instruction.md`, `metadata.json`, `verifier.py` under `tasks/<capability>/<complexity>/<task-id>/`.
- **Runners:** `scripts/run_task.py`, `scripts/run_batch.py`, `scripts/run_matrix.py` (local Ollama, schema-versioned raw JSON in `data/runs/`).
- **Derived reporting:** `scripts/summarize_runs.py` → `data/reports/latest.json`.
- **Validation:** `scripts/validate_repo.py`, `scripts/validate_verifier_fixtures.py`, CI smoke checks.
- **Public artifact:** generated static site in `docs/site/dist/` (report, results snapshot, task catalog, methodology, workflow, references).

Default evaluation policy: **10 samples per task** for pass-rate estimates; use `--repeat 1` for smoke runs.

## 3. Benchmark rules (non-negotiable)

- Tasks must be original; expected answers stay out of model-facing prompts unless the task is explicit copy compliance.
- Verifiers own acceptance behavior; grade observable output, not prose quality.
- Raw runs are source data; public reports are curated derived snapshots with provenance.
- Do not optimize prompts to raise weak-model scores or inflate claims beyond sample coverage.

## 4. Approved benchmark sections

Each section should reach **at least 10 deterministic tasks** before stronger section-level public claims:

- Music Theory Recognition
- Tonal Spelling & Enharmonics
- Rhythm & Duration Reasoning
- Symbolic Transformation
- Symbolic Music / Euterpea
- Instruction / Output Compliance
- Structured Output Fidelity
- Multi-Step Constraint Following
- Representation Translation
- Verifier Robustness / Ambiguity Cases

Current executable suite: see `tasks/README.md` and the generated task catalog (48 tasks in the latest expansion wave; baseline report may lag until re-run).

## 5. Baseline and evidence

- Curated report: `data/reports/latest.json`.
- Latest full local matrix (when current): 4 models × 13 seed tasks × 10 samples (`baseline-20260531-10sample-v1`).
- After task expansion, re-run matrix and regenerate report/site before updating public pass-rate claims.

## 6. Near-term priorities

1. **Task breadth:** grow each approved section toward 10+ deterministic tasks.
2. **Verifier fixtures:** broaden negative/positive fixtures across task families.
3. **Report/schema:** section-level totals and matrix-friendly derived fields where the site needs them.
4. **Site:** DeepSWE-inspired data browser (heatmap / tasks / trials) using only fields present in raw reports; no invented cost or effort-level metrics.
5. **Harness future:** artifact/patch execution for coding-agent tasks (not in current text-only harness).

## 7. Explicit non-goals (for now)

- Cloud deployment, paid API orchestration, or broad leaderboard positioning.
- Prompt engineering as the primary evaluation method.
- Committing large raw run corpora to git (fixtures and curated reports only unless policy changes).
- Working directly on `main` or merging without PR + human review when integrity surfaces change.

## 8. Success criteria

- A clone can run one model, produce raw JSON, summarize a report, build the site, and open a failure issue with enough context to reproduce.
- CI validates tasks, verifiers, fixtures, report shape, and site build without Ollama.
- Public pages summarize evidence; full audit detail remains in JSON artifacts.
- Documentation (this PRD, `README.md`, `HANDOFF.md`, research docs) matches what the repo actually does.
