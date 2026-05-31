# Signal vs Noise

The benchmark treats failures as data, but not every failure means the same thing.

## Signal

A failure is useful signal when it reveals a behavior the task was designed to measure:

- wrong symbolic music fact
- wrong enharmonic spelling where spelling is the target
- correct idea in the wrong machine-consumable format
- extra prose when output-only compliance is required
- invalid JSON when structured output is required
- multi-step instruction failure
- repeated answer distribution across runs or models

## Noise

A failure is likely noise or infrastructure debt when it comes from:

- ambiguous prompt wording
- verifier bug
- missing negative fixtures
- Ollama/server error
- task metadata mismatch
- report generation error
- overly broad normalization that hides the intended capability

## Promotion Rules

- Repeated signal becomes failure-corpus material.
- Ambiguous failures become task-rewrite issues.
- Verifier misses become verifier-bug issues and regression fixtures.
- Harness errors stay separate from model failures.
- Public reports should describe the limits of the sample instead of inflating conclusions.
