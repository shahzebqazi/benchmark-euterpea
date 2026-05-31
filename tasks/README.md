# Tasks

Tasks are grouped first by capability area, then by complexity.

```text
tasks/<capability>/<complexity>/<task-id>/
  instruction.md
  verifier.py
  metadata.json
```

The model sees only `instruction.md`. Expected answers and acceptance rules live in `verifier.py` and task metadata.

## Capability Areas

- `music-theory`: symbolic correctness over scale degrees, intervals, key signatures, enharmonic spelling, and chord spelling.
- `agent-compliance`: exact-output constraints, structured-output constraints, and multi-step instruction following.
- `euterpea-stubs`: Haskell/Euterpea-oriented symbolic music prompts before full solver tasks exist.

## Current Executable Tasks

- `c-major-fifth`: fifth scale degree in C major.
- `d-major-third`: third scale degree in D major.
- `f-major-key-signature`: single accidental in F major.
- `b-flat-major-key-signature`: number of flats in Bb major.
- `a-minor-relative-major`: relative major of A minor.
- `e-sharp-enharmonic`: enharmonic spelling trap.
- `g-sharp-minor-leading-tone`: double-sharp leading tone in harmonic minor.
- `c-major-triad-spelling`: comma-separated chord spelling.
- `output-only-token`: exact arbitrary token compliance.
- `json-only-status`: parseable one-key JSON compliance.
- `multi-step-output`: follow a two-step instruction and output only the final result.
- `transpose-line`: reason over an Euterpea-style pitch list.
- `haskell-duration-sum`: sum symbolic durations in quarter-note units.

## Complexity Levels

- `basic`: one-step answers with deterministic grading.
- `intermediate`: multi-step tasks, spelling traps, or constrained structured output.
- `advanced`: future tasks combining domain knowledge, code modification, tool use, or repository state.

## Verifier Standard

Verifiers should be strict by default. They may normalize whitespace and case when the task says exact note names, but they should reject extra prose, multiple answers, wrong enharmonic spelling, invalid JSON, or output that satisfies the fact while violating the instruction.

Failure reasons should identify the useful lesson: knowledge gap, symbolic spelling error, format violation, instruction violation, verifier ambiguity, or harness issue.
