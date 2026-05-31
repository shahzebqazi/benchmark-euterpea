## Summary

- 

## Change Type

Select one or more:

- [ ] `feature/*`
- [ ] `bugfix/*`
- [ ] `docs/*`
- [ ] `tests/*`
- [ ] `audit/*`
- [ ] `ui/*`
- [ ] `chore/*`

## Validation

- [ ] `python3 scripts/validate_repo.py`
- [ ] `python3 scripts/summarize_runs.py --batch-id <batch-id>`
- [ ] `python3 scripts/build_site.py`
- [ ] `python3 -m py_compile scripts/*.py $(find tasks -name 'verifier.py' -print)`
- [ ] Browser checked generated site, if UI changed
- [ ] Not run; explain why:

## Benchmark Integrity

- [ ] Expected answers remain outside model-facing prompts, except explicit copy/compliance tasks.
- [ ] Verifier behavior is unchanged, or changes are explained below.
- [ ] Raw vs derived data boundary is preserved.
- [ ] Public claims match sample size and provenance.

## Human Review Required?

- [ ] No, routine change.
- [ ] Yes, verifier acceptance changed.
- [ ] Yes, report schema changed.
- [ ] Yes, CI/deploy/security changed.
- [ ] Yes, public benchmark claims changed.
- [ ] Yes, generated/raw data publication decision needed.

Notes for reviewer:

## Agent Handoff

What changed:

What was intentionally not changed:

Risks/open questions:

Suggested next branch:
