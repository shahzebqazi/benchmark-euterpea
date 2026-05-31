# PRD: benchmark-euterpea

## 1. Summary

Build a tiny benchmark harness for music-aware agents. The first version asks an Ollama model a basic music question and verifies the answer deterministically.

First benchmark task: "What is the fifth note in C major?"

Expected answer: `G`.

## 2. MVP

- Python CLI.
- Ollama request.
- One task directory under `tasks/music-theory/basic`.
- One verifier.
- One JSON result file under `data/runs`.

Do not add a leaderboard, cloud deployment, or dashboard yet.

## 3. Benchmark Rules

- Tasks must be original.
- The model sees only the instruction.
- The verifier owns expected answers.
- Results must include model name, pass/fail, raw answer, and failure reason.

## 4. First Task

Task id: `c-major-fifth`

Prompt:

```text
What is the fifth note in the key of C major? Answer with only the note name.
```

Verifier:

- Normalize whitespace and case.
- Pass only `G`.
- Fail explanations, multiple notes, or unrelated text.

## 5. Later Tasks

- One semitone above C.
- Number of notes in a diatonic key.
- Write an answer to a required file.
- Follow CLI navigation instructions.
- Avoid committing to `main`.

Haskell/Euterpea comes after this loop works.

## 6. Draft Task Layout

Proposed task layout:

```text
tasks/<capability>/<complexity>/<task-id>/
  instruction.md
  verifier.py
  metadata.json
```

Initial task path:

```text
tasks/music-theory/basic/c-major-fifth/
```

## 7. Data Layout

Generated model outputs live under `data/runs`.

Each result should keep:

- `task_id`
- `model`
- `prompt`
- `raw_answer`
- `passed`
- `failure_reason`

These outputs are data, not source. Keep raw run JSON out of git unless a small fixture is needed for tests or documentation.

