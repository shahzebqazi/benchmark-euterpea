# Agent Branch And Review Policy

AI coding agents must work on scoped branches and merge through pull requests. `main` is the integration branch and should not receive direct agent edits except for emergency human-approved maintenance.

## Branch Names

Use one of these prefixes:

- `feature/<short-name>` for new benchmark/platform capabilities.
- `bugfix/<short-name>` for behavior corrections.
- `docs/<short-name>` for documentation-only changes.
- `tests/<short-name>` for validation fixtures and CI checks.
- `audit/<short-name>` for repo-wide reviews, findings, and cleanup plans.
- `ui/<short-name>` for site/report presentation work.
- `chore/<short-name>` for mechanical maintenance.

Examples:

```text
feature/ollama-model-matrix
bugfix/batch-exit-semantics
tests/verifier-negative-fixtures
ui/deslop-results-report
audit/repo-readiness-review
```

## Pull Request Flow

1. Create a scoped branch from latest `main`.
2. Make the smallest coherent change for the branch purpose.
3. Run validation locally when possible.
4. Open a PR into `main`.
5. Fill out the PR template with change type, validation, risk, and human-review needs.
6. Wait for auto review checks.
7. Prompt a human when the PR touches protected areas or changes benchmark meaning.
8. Merge only after CI and required human review pass.

## Auto PR Review

Auto review means repository checks that run on every PR and produce inspectable artifacts:

- branch-name policy check;
- Python compile check;
- repository contract validation;
- report generation smoke test;
- site build smoke test;
- optional future verifier fixture validation;
- optional future schema diff summary.

These checks do not replace human judgment. They catch mechanical and reproducibility failures before review.

## Human Prompt Required

Agents must explicitly ask for human approval before:

- changing verifier acceptance behavior for an existing task;
- deleting or rewriting raw run artifacts;
- changing report schema versions;
- changing CI, Pages deploy, or repository security settings;
- adding secrets, credentials, private endpoints, or tokens;
- publishing new public claims about model quality;
- merging to `main`;
- committing generated data that may be private or too large;
- force-pushing, rebasing shared branches, or rewriting history;
- broad refactors that obscure behavior under style changes.

## Agent Handoff Requirements

Every agent branch should leave a short handoff in the PR body:

- what changed;
- what was intentionally not changed;
- validation run;
- risks or open questions;
- whether human approval is required before merge;
- next suggested branch if work should continue.

## Merge Discipline

Prefer squash merge for small branches unless preserving commit history is useful for audit. Do not merge failing CI. Do not merge a PR that changes benchmark semantics without human review.
