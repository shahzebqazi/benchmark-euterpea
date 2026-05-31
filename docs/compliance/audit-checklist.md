# Benchmark Audit Checklist

Use this before calling a task or result public.

- The prompt is original and short.
- The expected answer is not in `instruction.md`.
- `metadata.json` has id, capability, complexity, and expected behavior.
- The verifier has positive and negative checks.
- Baseline runs use a recorded batch id and options.
- Public reports come from generated summaries.
- Known failure modes are documented or promoted to fixtures.
