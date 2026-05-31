# Standards Mapping

Use this file to map repository artifacts to external certification or benchmark standards.

## Current Evidence

- Task prompts are separate from verifiers.
- Expected answers are not included in prompts.
- Raw outputs are saved with pass/fail and failure reason.
- Task layout supports capability and complexity categories.
- Run schema records metadata, options, timing, and Ollama metrics.
- Public reports are generated from raw runs instead of edited by hand.

## Gaps

- No formal standard or certificate text has been added to this repo yet.
- No private holdout set exists yet.
- No independent verifier review exists yet.

## Internal Benchmark Quality Matrix

| Requirement | Artifact | Status |
| --- | --- | --- |
| Prompt/verifier separation | `tasks/**/instruction.md`, `verifier.py` | Met for current task |
| Deterministic grading | task verifier contract | Met for current task |
| Harness provenance | `scripts/run_task.py` result schema | Met for local Ollama runs |
| Curated public reporting | `scripts/summarize_runs.py`, `data/reports/latest.json` | Met after report generation |
| Contamination policy | `docs/research/contamination.md` | Draft |
| Failure corpus policy | `docs/research/failure-corpus.md` | Draft |
| Verifier QA | `docs/research/verifier-authoring.md` | Draft |
| Issue-driven workflow | `.github/ISSUE_TEMPLATE` | Draft |
| Private benchmark split | none | Missing |

When certificate standards are added, link each requirement to the task, verifier, data schema, or research note that satisfies it.
