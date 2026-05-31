# Task Contribution Workflow

Use GitHub Issues to collect real model failures and task proposals.

## Flow

1. Open an issue with the model, prompt, observed output, and expected behavior.
2. Decide whether the failure reflects a useful benchmark capability.
3. Write an original task prompt.
4. Put expected behavior in `metadata.json` and `verifier.py`, not the prompt.
5. Run diagnostic baselines.
6. Promote the task only after verifier checks pass.

Good tasks are short, behavior-focused, deterministic to grade, and difficult to satisfy by memorizing one public answer.
