# Findings

This is a short public research note for hiring readers. It summarizes what the current benchmark catches, why the failures matter, and where the suite remains weak.

## What Models Failed

The current curated snapshot contains 520 schema-versioned raw runs from a 4-model x 13-task x 10-sample local baseline. `llama3.2:3b` passes 41/130 samples. `gemma3:1b`, `granite3.2:2b`, and `phi4-mini` each pass 30/130 samples. Every model covers the full executable suite in this report.

The first task still demonstrates why the suite is useful. Small local models have answered `E`, `F`, `G#`, explanatory prose, and exact `G` to the same prompt: "What is the fifth note in the key of C major?" The fact is elementary, but the spread separates models that know the symbolic answer, models that count incorrectly, models that drift into adjacent pitch names, and models that know the answer but violate an output-only constraint.

The expanded suite is designed to produce more diagnostic failures:

- Scale-degree errors such as returning a diatonic neighbor instead of the requested degree.
- Enharmonic errors such as replacing `Fx` with `G` when tonal spelling is the task.
- Key-signature errors such as confusing the accidental list with accidental count.
- Chord-spelling errors such as correct pitch classes with wrong format or delimiter.
- Compliance errors such as adding markdown, explanations, quotes, or extra JSON keys.
- Symbolic-reasoning errors such as transposing pitch names while dropping accidentals or octaves.

## Why The Failures Matter

A benchmark is useful when a failure points to a behavior worth improving. These tasks are small enough that the failure can be audited directly, but varied enough to reveal different competence boundaries: symbolic knowledge, exact spelling, structured output, multi-step instruction following, and representation-level reasoning.

This matters for agent and coding-data work because many production failures are not dramatic hallucinations. They are small contract violations: a model emits the right idea in the wrong format, silently substitutes an easier equivalent, ignores a constraint, or produces output that cannot be consumed by the next deterministic step.

## What The Verifier Catches

The verifiers catch observable behavior, not vibes. They reject extra prose when the task asks for only a note name. They reject invalid JSON when the task asks for JSON. They reject enharmonic shortcuts when spelling is the target capability. They emit failure reasons that identify whether the issue is likely a knowledge gap, spelling error, format error, instruction violation, or task ambiguity.

The harness also preserves raw answers, model names, options, latency, batch ids, source task paths, and summaries. That makes a score inspectable. A hiring reader can see not only that a model failed, but what it wrote and why the grader rejected it.

## What Remains Weak

The benchmark is still small. It needs at least 10 deterministic tasks per approved benchmark section, more model families, broader verifier regression fixtures, and failure-corpus promotion. The Euterpea tasks are currently stubs rather than full Haskell solver tasks. Contamination controls are documented, but future growth should include unpublished variants and review of task exposure. The GitHub Pages hiscores are a curated public snapshot, not a production leaderboard.

The next larger-model comparison should be API-backed rather than local-pull-based for this environment. Candidate sub-30B models are `qwen3:14b`, `gemma3:27b`, and `mistral-small3.2:24b`, but their scores should not be promoted into the public findings until the unfinished task expansion is complete and the small-model baselines can be rerun in the same report snapshot.

That is the intended state for this phase: small enough to inspect, complete enough to demonstrate a repeatable method, and honest about what evidence it does and does not provide.
