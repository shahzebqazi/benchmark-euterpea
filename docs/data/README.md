# Data Docs

Generated model outputs live in `data/runs`.

Raw run JSON is useful even when the answer fails. It records the exact prompt, raw answer, model name, pass/fail result, and failure reason. Keep raw outputs out of git by default; promote only small fixtures or curated summaries when they are needed for tests or documentation.

## RAG Use

Saving small-model outputs can support a retrieval corpus later.

Useful retrieval records:

- task metadata;
- prompt text;
- raw answer;
- verifier result;
- failure reason;
- model name and version tag;
- run timestamp;
- notes about repeated failure modes.

Potential applications:

- retrieve similar failures when designing new tasks;
- compare how model families fail on the same concept;
- build evaluator notes from observed answer patterns;
- support benchmark reports without rerunning every model;
- create a corpus of negative examples for verifier regression tests.

Do not feed expected answers back into model prompts. Keep RAG use limited to analysis, reporting, task design, or evaluator development unless a future experiment explicitly studies feedback loops.
