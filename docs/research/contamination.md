# Contamination Policy

This benchmark uses original prompts and verifiers.

Music facts are common in training data, so contamination cannot mean "unknown fact." It means the task wording, task set, verifier, and report are authored for this benchmark instead of copied from a textbook, public quiz, or existing benchmark.

## Rules

- Do not copy textbook exercises verbatim.
- Do not put expected answers in `instruction.md`, except explicit exact-copy compliance tasks.
- Prefer parameterized coverage matrices for common facts.
- Keep some future task variants unpublished when the benchmark grows.
- Retire, mark, or rotate tasks if they become too exposed to be useful.
- Track contamination risk in task metadata and issue proposals.

## Review Questions

- Is the prompt wording original?
- Is the expected answer hidden from the model-facing instruction?
- Is the task testing a common fact, a symbolic trap, or instruction compliance?
- Could a model pass by memorizing a public quiz item rather than performing the target behavior?
- Should this task remain public, become a private variant, or be replaced by a generated family?
