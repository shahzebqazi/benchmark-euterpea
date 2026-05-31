# Benchmark Methodology

`benchmark-euterpea` is a small, original benchmark suite for evaluating model competence and agent compliance under deterministic grading.

The benchmark starts with music theory because the domain has symbolic correctness, compact prompts, and failures that can be audited by a human with domain knowledge. It then adds agent-compliance prompts and Euterpea-oriented stubs to show that the same pattern can extend from facts, to instruction following, to symbolic program reasoning.

## Lifecycle

1. Propose a task through GitHub Issues with capability, verifier idea, contamination risk, and expected failure modes.
2. Write an original `instruction.md` that does not expose the expected answer.
3. Encode the expected behavior in `metadata.json` and `verifier.py`.
4. Run local Ollama batches with fixed options and batch ids.
5. Preserve raw JSON artifacts with prompt, model, options, raw answer, pass/fail, failure reason, latency, and source path.
6. Summarize curated reports into `data/reports/latest.json` and the GitHub Pages hiscores.
7. Promote repeated failures into the failure corpus, verifier regression cases, or new task proposals.

## Grading Policy

The verifier owns correctness. A model does not pass because its explanation sounds plausible; it passes because its observable output satisfies the task contract.

Strictness is intentional. In music theory, enharmonic spelling can be the point of the task. In compliance tasks, extra prose can be the failure even if the embedded fact is correct. In Euterpea-style tasks, code-looking text should not pass if the task asks for evaluated symbolic output.

## Contamination

Contamination is managed at the task level. Common music facts are not secret, so the benchmark does not pretend they are. Instead, it avoids copied exercise wording, keeps task variants original, documents exposure risk, and uses issue review to decide when a task is too public or too predictable to remain diagnostic.

## Verifier Quality

Every official verifier should have positive examples, negative examples, and explicit failure reasons. The verifier should be narrow enough to make grading reproducible and clear enough that a failure teaches the task author something.

## Run Provenance

Each run records:

- schema version
- run timestamp
- batch id and sample index
- task id, path, and metadata
- model name and Ollama options
- prompt shown to the model
- raw answer
- pass/fail and failure reason
- latency and Ollama timing metrics when available

This is the minimum evidence needed to debug a score instead of arguing from a leaderboard number.

## API-Backed Larger Models

Small local models are useful for fast iteration, but larger model comparisons should use the same task prompts, verifier contracts, and generation options. Ollama Cloud runs are allowed when the raw run records the remote host and the authentication source without storing the API key.

For API-backed smoke checks, use `--repeat 1` until the task set is complete. A full comparison should rerun the selected small and larger models under one shared batch id after each approved benchmark section has enough deterministic tasks to make the report meaningful.

Candidate sub-30B larger models for the next smoke comparison:

- `qwen3:14b`
- `gemma3:27b`
- `mistral-small3.2:24b`

Example cloud smoke command:

```bash
python3 scripts/run_batch.py --model qwen3:14b --repeat 1 --batch-id api-large-smoke-v1 --ollama-url https://ollama.com --temperature 0.2 --num-predict 32
```

## What This Is Not

This is not a claim that small local models are representative of frontier systems. It is not a final leaderboard. It is a compact demonstration of benchmark authorship: original tasks, deterministic verifiers, provenance, failure analysis, and a public reporting surface.
