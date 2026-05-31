# Verifier Authoring

Verifiers own expected answers. Prompts do not.

## Checklist

- The verifier accepts every intended correct form.
- The verifier rejects common wrong answers and extra prose when exact output is required.
- Failure reasons are specific enough to debug.
- Positive and negative examples exist for regression tests.
- The verifier grades observable behavior, not implementation style.

For solver tasks, grade the behavior of the submitted code or generated file. Avoid rewarding code that merely prints a hardcoded answer unless the task explicitly asks for one constant.
