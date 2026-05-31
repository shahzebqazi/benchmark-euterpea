# Tasks

Tasks are grouped first by capability area, then by complexity.

```text
tasks/<capability>/<complexity>/<task-id>/
  instruction.md
  verifier.py
  metadata.json
```

The model sees only `instruction.md`. Expected answers and acceptance rules live in `verifier.py` and task metadata.

## Task Quality Gates

New tasks should follow the same benchmark-integrity principles that the site reports:

- Original prompt: write a fresh instruction for this benchmark rather than copying a public exercise, issue, or patch.
- Hidden answer: keep expected answers and accepted variants out of `instruction.md`.
- Prompt-verifier bijection: the verifier should test exactly the behavior requested by the prompt, no more and no less.
- Acceptance breadth: accept every intended correct observable output, not one private wording or implementation shape.
- Contamination review: document common-source exposure and avoid stronger claims when the task is likely familiar.
- Fixture promotion: repeated failures should become negative verifier fixtures or ambiguity-review cases.

Datacurve's DeepSWE is the methodological model for future coding-agent tasks: short natural prompts, original work, behavioral verifiers, and clean environments. This repo cannot yet grade long-horizon repo edits, so coding-aligned tasks must remain harness-compatible until a patch/test runner exists.

## Capability Areas

Tasks currently live under implementation-oriented capability directories, but public reporting groups them into benchmark sections. Each section should reach at least 10 deterministic tasks before stronger section-level claims are made:

- Music Theory Recognition
- Tonal Spelling & Enharmonics
- Rhythm & Duration Reasoning
- Symbolic Transformation
- Symbolic Music / Euterpea
- Instruction / Output Compliance
- Structured Output Fidelity
- Multi-Step Constraint Following
- Representation Translation
- Verifier Robustness / Ambiguity Cases

Current directories:

- `music-theory`: symbolic correctness over scale degrees, intervals, key signatures, enharmonic spelling, and chord spelling.
- `agent-compliance`: exact-output constraints, structured-output constraints, and multi-step instruction following.
- `euterpea-stubs`: Haskell/Euterpea-oriented symbolic music prompts before full solver tasks exist.

## Current Executable Tasks

The executable suite now includes the original 13 contracts plus a first research-backed expansion wave across music recognition, tonal spelling, rhythm, symbolic transforms, Euterpea-style reasoning, compliance, structured output, multi-step constraints, representation translation, and verifier robustness. The generated task catalog is the source of truth for the full current list.

Original seed tasks:

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

## Algebraic Task Direction

Future complex tasks should use human-written verifiers over canonical algebraic structures. The model may output a compact string, JSON object, or Haskell/Euterpea-like expression, but the verifier should parse it into typed domain values before comparing behavior.

Useful structures include:

- `Pitch`: note name, accidental, and optional octave.
- `Interval`: quality and number.
- `Key`: tonic and mode.
- `Duration`: primitive durations plus dotted or summed forms.
- `Melody`: ordered pitch sequence.
- `Transform`: transpose, invert, retrograde, map, or compose operations.

This supports harder task families without subjective grading:

- category-theory-shaped tasks such as identity transforms, transform composition, and functor-like mapping over melodies;
- lazy-evaluation tasks such as finite prefixes of generated motifs or streams;
- generative-AI tasks where the model creates a constrained symbolic object and the verifier checks invariants rather than taste.

Keep verifiers deterministic and human authored. Generative tasks should pass only when their parsed structure satisfies explicit invariants.

## Research-Backed Backlog

Each benchmark section should grow beyond the first examples. A section needs at least 10 deterministic executable tasks before the project makes stronger section-level claims.

- Music Theory Recognition: scale-degree variants, key-signature counts and accidental lists, relative and parallel keys, interval qualities, mode recognition, and chord-quality labels.
- Tonal Spelling & Enharmonics: double accidentals, harmonic-minor leading tones, altered scale degrees, chord spelling, seventh-chord spelling, and enharmonic near misses.
- Rhythm & Duration Reasoning: duration sums, rest arithmetic, simple meter fit, dotted values, beat counts, and bar-completion tasks.
- Symbolic Transformation: pitch-list transposition, octave preservation, interval shifts, retrograde, inversion, duration scaling, and transform composition.
- Symbolic Music / Euterpea: Euterpea-style `Pitch`, `Dur`, `Music`, `transpose`, `trans`, and `scaleDurations` reasoning that can later become solver-backed Haskell tasks.
- Instruction / Output Compliance: exact-token output, no prose, no markdown, branch-policy decisions, no-secret redaction, no-main-commit decisions, and expected-answer leakage checks.
- Structured Output Fidelity: strict JSON objects, allowed enums, exact arrays, nested music structures, patch-summary JSON, and later delimiter-constrained CSV or TSV.
- Multi-Step Constraint Following: hidden intermediate reasoning, ordered transformations, music-plus-final-answer constraints, agent procedure compliance, and short prompts with discoverable constraints.
- Representation Translation: pitch strings to JSON, JSON to compact notation, plain language to symbolic output, Euterpea expression to compact output, and coding-artifact summaries.
- Verifier Robustness / Ambiguity Cases: near-miss fixtures, punctuation strictness, accepted-variant boundaries, false-positive traps, false-negative traps, and ambiguity review before scored promotion.
