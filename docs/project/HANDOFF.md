# Handoff: Repo-Wide Audit And Benchmark Platform Development

## Intent

`benchmark-euterpea` should read as a small but complete benchmark data platform slice, not a music toy and not a prompt-engineering experiment.

Primary framing:

> benchmark-euterpea is a small original benchmark suite for evaluating model competence and agent compliance under deterministic grading. Music theory is the first controlled domain because it has symbolic correctness, easy-to-audit failures, and a path into Haskell/Euterpea solver tasks.

For Datacurve Software Engineer review, emphasize the data-engine infrastructure:

- task lifecycle;
- deterministic verifier boundary;
- raw vs derived data separation;
- run provenance;
- validation and CI;
- reporting and site generation;
- failure corpus and root-cause analysis;
- credible scaling path to workers, queues, storage, dashboards, and researcher workflows.

Do not optimize prompts to raise weak-model scores. Do not frame this as prompt engineering. The goal is benchmark integrity, reproducibility, and reliable infrastructure.

## Current State

- Local repo: `/Users/sqazi/Git/public/benchmark-euterpea`.
- Public remote: `https://github.com/shahzebqazi/benchmark-euterpea`.
- Agent work should happen on `feature/pre-push-ready`; do not work directly on `main`.
- Remote publication is intentionally blocked until the user says the application is complete and asks to push.
- The current curated report is a full 4-model x 13-task x 10-sample baseline.
- Local Ollama weights live at `~/Git/Config/my-ai-models/ollama/models` (`~/.ollama/models` symlinks there). Playbook repo: `~/Git/configuration/my-ai-models/`.
- Current report/site should be described as a reproducible local baseline, still modest in task breadth.
- Do not touch `/Users/sqazi/Git/Personal/social/linkedin`; another agent owns application materials.

## Implemented Platform Artifacts

Core runner/reporting:

- `scripts/run_task.py`: one-task Ollama runner with schema version, task metadata, batch/sample IDs, model options, timestamps, latency, raw answer, pass/fail, failure reason, and Ollama metrics.
- `scripts/run_batch.py`: discovers task directories and runs a model across the executable suite.
- `scripts/summarize_runs.py`: turns raw `data/runs/*.json` files into curated `data/reports/latest.json`.
- `scripts/validate_repo.py`: validates task metadata, unique ids, verifier imports/contracts, metadata expected-answer pass cases, negative verifier fixtures, prompt leakage, and report shape.
- `scripts/validate_verifier_fixtures.py`: runs curated positive and negative verifier cases from `tests/fixtures/verifiers/`.
- `scripts/build_site.py`: generates an engineer-facing static site from task metadata and the latest report.

Docs and methodology:

- `README.md`: benchmark data-platform framing, quick start, task lifecycle, raw/derived data model, scaling path.
- `ARCHITECTURE.md`: runner flow, task contract, verifier boundary, raw run schema, derived report schema, provenance, failure handling, CI, scaling path, reliability risks.
- `docs/research/`: methodology, contamination, verifier authoring, run provenance, failure corpus, signal vs noise, findings, why-this-benchmark-exists.
- `.github/ISSUE_TEMPLATE/new-task.yml`: task proposal intake with capability, prompt, verifier, contamination risk, and expected failure modes.
- `.github/workflows/ci.yml`: compile, validate, summarize, build site.
- `.github/workflows/pages.yml`: GitHub Pages deployment.
- `.github/workflows/pr-policy.yml`: branch-prefix enforcement and auto PR review smoke checks.
- `.github/pull_request_template.md`: benchmark integrity, validation, human-review, and agent-handoff checklist.
- `docs/agentic/branch-and-review-policy.md`: agent branch policy, PR flow, human approval triggers, and merge discipline.

Current task breadth:

- 13 executable tasks total.
- Music theory: scale degrees, key signatures, relative keys, enharmonic traps, chord spelling.
- Agent compliance: exact output, JSON-only output, multi-step output.
- Euterpea/Haskell stubs: symbolic pitch transposition, duration reasoning.

## Latest Baseline

Report: `data/reports/latest.json`.

Source run count: 520 schema-versioned raw runs from batch `baseline-20260531-10sample-v1`.

Model coverage:

- `llama3.2:3b`: 13 tasks covered, 41/130 samples passed.
- `gemma3:1b`: 13 tasks covered, 30/130 samples passed.
- `granite3.2:2b`: 13 tasks covered, 30/130 samples passed.
- `phi4-mini`: 13 tasks covered, 30/130 samples passed.

Notable failures:

- `c-major-fifth`: answered `E`, expected `G`.
- `a-minor-relative-major`: answered `F# minor`, expected `C major`.
- `g-sharp-minor-leading-tone`: answered `Bb`, expected `Fx`.
- `multi-step-output`: added prose and repeated the wrong letter.
- `transpose-line`: explained instead of outputting only `D4,F#4,A4`.

Required next benchmark work:

- Add more tasks. User target: minimum 10 deterministic tasks per approved benchmark section.
- Keep the current 10-sample repeat policy for accuracy estimates.
- Multi-model runner now exists at `scripts/run_matrix.py`; use it for smoke/full local matrix reruns.
- Preserve reproducibility details in issues when external users or agents run individual models.


## Branch, PR, And Review Governance

AI coding agents must work on scoped branches and merge through pull requests into `main`. Branch prefixes are enforced by `.github/workflows/pr-policy.yml`:

- `feature/*`
- `bugfix/*`
- `docs/*`
- `tests/*`
- `audit/*`
- `ui/*`
- `chore/*`

Auto PR review is implemented as lightweight GitHub Actions checks:

- branch prefix policy;
- Python compile;
- repository contract validation;
- report generation smoke test;
- static site build smoke test.

Human prompts/approval are required before changing verifier acceptance behavior, report schema versions, CI/deploy/security, raw data publication, public benchmark claims, or merging to `main`. See `docs/agentic/branch-and-review-policy.md` and `.github/pull_request_template.md`.

## UX/UI Agent Status

The UX/UI agent has already reworked `scripts/build_site.py` significantly. The site now has a paper/report-style visual direction: editorial hero, abstract, contribution sections, pipeline diagram, result snapshot cards, pass-rate bars, section-level technical evidence summaries, task catalog grouped by benchmark section, methodology page, review workflow page, references page, and reproducible-run guidance.

Current quality is improved from the original and user feedback is positive. The site supports model comparison, a horizontally scrollable task/model matrix sized around four visible model columns, expandable technical evidence list items by benchmark section, compact provenance summaries, references, and a clone-and-run contribution path. Raw answer distributions, source paths, model options, and full provenance should remain in `data/reports/latest.json`, not pushed into public page tables.

Recent user-directed site changes:

- Move/merge the current evidence section into the Results Snapshot page.
- Merge Coverage and Limitations into a centered homepage section.
- Add a References page and footer links.
- Redo footer around reproducibility and contribution.
- Keep task catalog centered on approved benchmark sections.
- Show task expansion target: minimum 10 tasks per section.
- Replace raw failure/answer/provenance tables with section-level technical summaries and compact charts.
- Rename the results evidence heading to avoid "section" in the title: "Evidence by benchmark."
- Make evidence summaries expandable list items with nerd-style icons per benchmark section.
- Make the score matrix horizontally scrollable for additional models and remove section-summary rows from that matrix.
- Reformat the methodology page toward a formal CS paper methodology section, including Datacurve-aligned review criteria.
- Rebuild the methodology page using `https://deepswe.datacurve.ai/blog#methodology` as the spec. Mirror the structure, adapted to this repo: "Repository/domain selection" instead of repository selection; "Task construction"; "Quality assurance"; "Evaluation harness"; and "Harness limitations / future native-harness comparison." The page should explicitly cover prompt/verifier artifacts, behavioral verification, verifier flakiness checks, regression/negative fixtures, human review, multiple-model diagnostic rollouts, and the current local Ollama harness boundary.

Remaining UI/site follow-up:

- Review generated pages in browser after any copy/layout changes.
- Consider splitting `scripts/build_site.py` if further UI growth makes it hard to maintain.
- Richer failure-corpus promotion remains future work; the public site should summarize evidence while preserving raw audit data in JSON artifacts.
- Add DeepSWE-style interactive result graphs. The current site does not yet match the two primary graph patterns on `https://deepswe.datacurve.ai/`: score plotted against cost/time/output-token efficiency and a leaderboard-style model comparison with date, model count, best/all effort-level controls, and per-model pass rate, average cost, average time, and output-token metrics.
- For this repo, graph controls should map to available benchmark data rather than inventing missing fields. Current raw reports have latency and Ollama token/timing metrics when present, but not monetary cost or effort-level metadata. Add placeholders or disabled controls only if clearly labeled as unavailable.
- Rebuild the matrix/data experience using `https://deepswe.datacurve.ai/data` and `https://deepswe.datacurve.ai/data/trials` as the product spec. The Results Snapshot should grow into a data-browser page with tabs for Heatmap, Tasks, and Trials:
  - Heatmap: task x model-effort grid, pivot control for tasks/model efforts, source selector, model grouping control, all/exclude errored/only passed filters, display as numbers or color-only, and color-by controls such as pass rate, average latency/duration, token counts, trials, and errors.
  - Tasks: searchable task catalog with language/domain/section filters, task cards, stable task URLs, and compact task descriptions. For this repo, filters should use benchmark section, capability, complexity, and domain instead of programming language/repository.
  - Trials: searchable table of individual run records with outcome, model, task, latency/duration, token/timing metrics where available, batch id, and error state. Do not dump raw answers by default; expose raw-answer detail only behind an intentional drill-down if needed for audit.
  - Preserve the current public-site principle: summarize evidence visually while keeping full raw/provenance details in JSON artifacts.
- Methodology rewrite details from DeepSWE spec:
  - Repository/domain selection: explain why music theory, agent compliance, and Euterpea-style symbolic tasks are the controlled domain slice; note that true repo-level coding tasks are future work.
  - Task construction: every task ships model-facing prompt, executable verifier, and metadata/reference expected behavior; verifiers test observable behavior rather than implementation style.
  - Reliability checks: verifier import/contract validation, expected-answer pass check, prompt leakage checks, negative fixtures, and future repeated/flakiness checks.
  - Quality assurance: prompt-verifier bijection, acceptance breadth, realism, and environment cleanliness; tasks below this bar should return for revision.
  - Evaluation harness: local/Ollama `run_task.py` and `run_batch.py` are held fixed across models so comparisons reflect model behavior rather than per-model scaffolding.
  - Limitations: current harness grades single text responses, not long-horizon repo edits; future work should add artifact/patch execution before claiming DeepSWE-style coding-agent coverage.

When checking UX/UI work, inspect generated pages in browser, not only the source. The local site should be rebuilt with:

```bash
python3 scripts/summarize_runs.py
python3 scripts/build_site.py
```

Then open `http://127.0.0.1:8765/` or serve `docs/site/dist` if needed.

## Required Repo-Wide Audit

Before major new feature work, perform a repo-wide audit for bugs, correctness issues, and maintainability risks. Treat this like a pre-interview readiness review.

Audit scope:

1. Runner correctness
   - Confirm `run_task.py` distinguishes benchmark failure from harness failure clearly.
   - Check whether `run_batch.py` should continue on failed benchmark tasks but fail only on harness errors, or whether current nonzero behavior is intended.
   - Verify output filename safety and collision behavior.
   - Verify `--output` behavior with repeats.
   - Confirm model options are recorded consistently and are comparable across models.
   - Add support for multi-model batches without shell loops.

2. Verifier correctness
   - Review every verifier for overly strict/overly loose normalization.
   - Add negative fixtures, not just positive smoke tests.
   - Add a `tests/fixtures/verifiers/*.json` or similar fixture format.
   - Add `scripts/validate_verifier_fixtures.py`.
   - Ensure failure reasons classify root cause instead of only restating expected answer.

3. Task design
   - Check prompts for hidden ambiguity.
   - Check metadata consistency and contamination fields.
   - Revisit tasks where punctuation-only failures may be too strict or intentionally strict; document the policy.
   - Add file-output compliance task if the harness supports artifact checking later.

4. Raw/derived data
   - Confirm raw run schema matches `ARCHITECTURE.md`.
   - Confirm derived report schema includes source files, batch ids, model options, answer distribution, failure distribution, and task metadata.
   - Add report-level totals by model and benchmark section, not only task/model rows.
   - Add model/task matrix data to `latest.json` or compute it in the site generator.

5. Site generation
   - Audit `scripts/build_site.py` for readability; it is now large and may need internal helpers split by page or component.
   - Check accessibility: heading order, contrast, table overflow, mobile layout.
   - Check visual regressions in browser on `index.html`, `hiscores.html`, `tasks.html`, `methodology.html`, `workflow.html`.
   - Ensure generated site does not expose expected answers too prominently outside report context.

6. CI and validation
   - Ensure CI does not require Ollama.
   - Add fixture-based verifier validation.
   - Add report generation smoke test on checked-in sample data.
   - Add Pages build validation before deploy.
   - Consider a separate workflow for optional local/full benchmark runs, not required for PRs.

7. AGENTIC/GitHub agent readiness
   - Add docs for agentic SDLC workflow, guardrails, tool policy, state/memory, and multi-agent review roles if this repo is going to demonstrate GitHub Agentic AI Developer alignment.
   - Do not overbuild actual cloud-agent automation yet; start with governance docs and artifacts.

## Known Bug/Risk Candidates

- `run_batch.py` increments `failures` for any nonzero `run_task.py`; currently benchmark failures and harness failures are conflated at batch level.
- `run_task.py` returns `1` for benchmark failures and `2` for harness/runtime errors, but `run_batch.py` collapses both to one failure count.
- `scripts/build_site.py` is a single large generated-site script; maintainability will degrade as visual/report complexity grows.
- Full-suite model baseline now exists, but section breadth is weak. Each approved benchmark section needs at least 10 deterministic tasks.
- Verifier validation includes initial negative fixtures for two tasks; broaden fixture coverage across all task families.
- Punctuation failures such as `F.` vs `F` are currently strict; that is defensible for exact-output tasks, but the policy should be explicit per task family.
- `data/runs` may be git-ignored while report `source_files` point to paths that will not exist in public clone if raw runs are not committed; decide whether selected curated raw runs should be committed or reports should embed enough provenance without relying on those files.

## External Run And Issue Workflow

Users and agents should be able to clone the repo, run one model locally, and open an issue with enough detail for maintainers or repo agents to recreate the result.

Documented workflow:

```bash
git clone https://github.com/shahzebqazi/benchmark-euterpea.git
cd benchmark-euterpea
git rev-parse HEAD
ollama pull <model>
python3 scripts/run_batch.py --model <model> --repeat 10 --batch-id external-<model>-<date> --temperature 0.2 --num-predict 32
python3 scripts/summarize_runs.py --batch-id external-<model>-<date>
python3 scripts/build_site.py
```

Issue must include:

- commit SHA;
- model name and Ollama version;
- batch id;
- repeat count and generation options;
- exact reproduction commands;
- pass-rate summary by section/task;
- notable failures with observed answer and verifier reason;
- whether the finding suggests a new task, verifier fixture, ambiguity fix, or failure-corpus entry.

The issue template `.github/ISSUE_TEMPLATE/model-failure.yml` has been expanded for this.

## Multi-Model Ollama Plan

The first full local matrix has been run. Keep this plan for future reruns and for building a dedicated matrix runner.

Short-term implementation:

1. Use `scripts/run_matrix.py` to keep single-model batch semantics clean while coordinating repeated `--model` runs.
2. Run all currently installed local Ollama models: `llama3.2:3b`, `phi4-mini:latest`, `gemma3:1b`, and `granite3.2:2b`.
3. For each model, run all discovered tasks with the same batch id, sample count, temperature, `num_predict`, and optional seed.
4. Use a batch id convention like:
   - `local-ollama-20260531-matrix-v1`
   - per-model output filenames already include model name.
5. Preserve benchmark failures but continue the matrix unless there is a harness error that prevents a model from running.
6. Return a final exit code that distinguishes:
   - `0`: all benchmark samples passed and no harness errors;
   - `1`: benchmark failures occurred but all runs completed;
   - `2`: one or more harness/model/runtime errors occurred.
7. Summarize with:

```bash
python3 scripts/summarize_runs.py --batch-id local-ollama-20260531-matrix-v1
python3 scripts/build_site.py
```

Potential command design:

```bash
python3 scripts/run_matrix.py   --model llama3.2:3b   --model phi4-mini:latest   --model gemma3:1b   --model granite3.2:2b   --repeat 10   --batch-id local-ollama-20260531-matrix-v1   --temperature 0.2   --num-predict 32
```

Do not run very large repeats without checking runtime and disk churn. Start with `--repeat 1` across all four models for smoke. Then run the default `--repeat 10` after report/site behavior is confirmed.

After the first matrix run, update `data/reports/latest.json` and the generated site so the public report answers:

- Which models were run?
- What is each model's overall pass rate?
- Which tasks separate the models?
- What answer distributions and failure reasons recur by model/task?
- Which batch ids, source run files, and model options support each row?

## Development Priorities

1. Generate more benchmark tasks until every approved section has at least 10 tasks.
2. Add a multi-model matrix runner if shell loops become too brittle.
3. Broaden verifier fixtures beyond the first two task contracts.
4. Repo-wide audit and bug fixes, especially batch exit semantics and report/source provenance.
5. Add AGENTIC-aligned docs only after benchmark infra remains coherent.
6. Re-run the 4-model x 10-sample baseline after task expansion.

## Validation Commands

Run these after substantive code/site changes:

```bash
python3 -m py_compile scripts/*.py $(python3 - <<'PY'
from pathlib import Path
print(" ".join(str(path) for path in Path("tasks").glob("**/verifier.py")))
PY
)
python3 scripts/validate_verifier_fixtures.py
python3 scripts/validate_repo.py
python3 scripts/summarize_runs.py
python3 scripts/build_site.py
python3 scripts/check_links.py
```

For full multi-model work, pass all target `--batch-id` values to `scripts/summarize_runs.py`.

## Guardrails

- Do not commit unless explicitly asked.
- Do not touch `/Users/sqazi/Git/Personal/social/linkedin`.
- Do not optimize prompts to make weak models pass.
- Do not inflate claims beyond the sample size.
- Do not add heavy UI/cloud infrastructure before the scripts and schemas are stable.
- Keep expected answers out of model-facing prompts unless the task is explicitly exact-copy compliance.
- Treat raw failures as benchmark data, not embarrassments to hide.
