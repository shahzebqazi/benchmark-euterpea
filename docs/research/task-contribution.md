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

## Coding-Agent Alignment

Coding-agent tasks should borrow Datacurve/DeepSWE principles without pretending this harness is a full repo-edit benchmark yet:

- prompts should be original and behavior-focused;
- verifiers should grade observable outputs, not private implementation style;
- accepted outputs should cover all intended correct forms;
- task metadata should record contamination risk and expected failure modes;
- true repository-edit tasks should wait for a harness that can capture patches and run tests.

Harness-compatible coding tasks can still test useful behavior today: branch-policy decisions, no-secret redaction, expected-answer leakage detection, patch-summary JSON, verifier false-positive classification, and command-output compliance.
