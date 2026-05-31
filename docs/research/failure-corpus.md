# Failure Corpus

Raw failures are useful benchmark material. They show where a model violated symbolic correctness, output format, or instruction constraints, and they help decide whether a task, verifier, or report needs improvement.

## Failure Types

- `knowledge_gap`: wrong music fact or concept.
- `spelling_error`: enharmonic pitch is correct-sounding but symbolically wrong for the task.
- `format_error`: answer contains prose, invalid JSON, wrong delimiter, or multiple answers.
- `instruction_violation`: model ignores an explicit constraint.
- `harness_error`: runner, model server, report, or verifier infrastructure failure.
- `ambiguous_task`: prompt or verifier needs clarification.

## Promotion Path

1. Save raw runs in `data/runs`.
2. Summarize curated public results in `data/reports`.
3. Inspect repeated failures by task/model/batch.
4. Promote stable patterns into failure-corpus notes or verifier regression fixtures.
5. Use novel failure patterns as candidates for new tasks.
6. Open verifier-bug or task-rewrite issues when the failure is caused by benchmark design rather than model behavior.

## Signal Standard

A failure becomes research signal when the observed answer is interpretable, reproducible enough to inspect, and tied to a capability the task intended to measure. One-off malformed output can still be useful, but public claims should distinguish examples from stable distributions.
