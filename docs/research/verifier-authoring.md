# Verifier Authoring

Verifiers own expected answers. Prompts do not.

## Checklist

- The verifier accepts every intended correct form.
- The verifier rejects common wrong answers and extra prose when exact output is required.
- Failure reasons are specific enough to debug.
- Positive and negative examples exist for regression tests.
- The verifier grades observable behavior, not implementation style.

For solver tasks, grade the behavior of the submitted code or generated file. Avoid rewarding code that merely prints a hardcoded answer unless the task explicitly asks for one constant.

## Datacurve-Aligned Review

Before promoting a verifier, check the same failure directions that matter in coding-agent benchmarks:

- False positives: the verifier passes an output that does not satisfy the prompt.
- False negatives: the verifier rejects an output that satisfies the observable contract.
- Prompt-verifier mismatch: the verifier checks unstated behavior or misses stated behavior.
- Over-narrow acceptance: the verifier only accepts the author's preferred shape.
- Flakiness: the verifier result depends on timing, environment, random ordering, or external state.

For this repository, verifiers should stay deterministic Python functions over raw model text until a richer artifact or patch harness exists.
