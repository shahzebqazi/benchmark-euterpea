# Agent prompt — benchmark-euterpea pre-push upgrade (benchmark-euterpea standard)

Copy everything below the line into a new agent session.

**Repo root:** `~/Git/public/benchmark-euterpea/`  
**Public remote (do not push until user completes application):** https://github.com/shahzebqazi/benchmark-euterpea  
**Reference standard:** This repo’s own `ARCHITECTURE.md`, `AGENTS.md`, `scripts/validate_repo.py`, and `.github/workflows/*`  
**Cross-reference (read-only):** `~/Git/Personal/shahzebqazi/lambda-terminal` — example of a **already-public** portfolio repo (CI green, tagged release, 46 tests). Borrow **shipping discipline**, not domain logic.

**Hard rule:** **Do not `git push`** or publish to GitHub Pages until the user explicitly says the application is complete and asks you to push.

---

## Mission

Upgrade `benchmark-euterpea` from **strong local slice** to **push-ready public artifact** that matches the standard this repo already documents — so a Datacurve (or any lane-A) reviewer can clone, validate, skim the site, and trust the claims in ~2 minutes.

Current gaps (audit 2026-05-31):

- Local tree is complete; **`main` has zero commits**; GitHub remote is **empty**
- `data/reports/latest.json` reflects **one model** (`llama3.2:3b`); plan calls for **four models × 5 repeats** baseline
- LinkedIn/Datacurve materials already link to this repo and hiscores — URLs must work **after** user-triggered push, not before
- `docs/project/HANDOFF.md` may be stale vs working tree — reconcile

---

## Read first (strict order)

| # | Path | Why |
|---|------|-----|
| 1 | `AGENTS.md` | Guardrails, branch policy, no prompt optimization |
| 2 | `ARCHITECTURE.md` | Contracts: tasks, verifiers, raw/derived, provenance |
| 3 | `README.md` | Public framing and quick start |
| 4 | `docs/project/HANDOFF.md` | Intended state vs gaps |
| 5 | `docs/agentic/branch-and-review-policy.md` | Branch prefixes, PR flow |
| 6 | `scripts/validate_repo.py` | Single source of “repo is healthy” |
| 7 | `.github/workflows/ci.yml` + `pages.yml` + `pr-policy.yml` | CI/Pages expectations |
| 8 | `data/reports/README.md` | Raw vs curated publish policy |
| 9 | `docs/research/findings.md` | Honest public narrative |
| 10 | `~/Git/Personal/social/linkedin/applications/resumes/datacurve/2026-05-31_software-engineer/REQUIREMENTS.md` | External claims to satisfy |

Optional: `~/.cursor/plans/pages_benchmark_workflow_6f182265.plan.md` — baseline models and validation checklist.

---

## Target standard (definition of done)

The repo matches **benchmark-euterpea standard** when all of the following hold:

### A. Contract integrity

- [ ] `python3 scripts/validate_repo.py` exits 0
- [ ] All 13+ tasks have unique ids, full metadata, importable verifiers, no prompt leakage (except explicit compliance tasks)
- [ ] `data/reports/latest.json` has valid `schema_version`, reproducible from `data/runs/` via `summarize_runs.py`
- [ ] `python3 scripts/build_site.py` produces `docs/site/dist/` with working internal links

### B. Evidence quality (pre-push content)

- [ ] **Multi-model baseline** in curated report: at minimum the four models from the Pages plan — `llama3.2:3b`, `granite3.2:2b`, `gemma3:1b`, `phi4-mini` — each with **5 samples** on the full executable task suite (or document honestly if Ollama models unavailable locally)
- [ ] Report includes pass rates, failure distributions, latency averages, batch ids, source file paths per ARCHITECTURE
- [ ] `docs/research/findings.md` updated to reflect **actual** multi-model failures (not hypothetical)
- [ ] Site `hiscores.html` renders all models in report — not single-model-only

### C. Agent / contributor hygiene (match lambda-terminal’s public maturity where applicable)

| benchmark-euterpea (required) | lambda-terminal analogue |
|------------------------------|---------------------------|
| `AGENTS.md` | Already exists — keep current |
| Branch + PR policy workflows | Add if missing checks |
| Issue templates | Already exist — verify YAML valid |
| PR template | Fill risk / validation sections |
| `validate_repo.py` | lambda-terminal’s `swift test` — **you** own Python validator |
| Pre-push checklist doc | Create `docs/agentic/PRE_PUSH_CHECKLIST.md` |
| No secrets in git | `.gitignore` covers raw runs policy explicitly |

### D. Publish policy (document, don’t guess)

- [ ] `.gitignore` and `data/reports/README.md` state clearly:
  - What is committed (curated reports, generated site, sample runs vs full raw corpus)
  - What stays local-only
- [ ] No API keys, Ollama URLs with tokens, or private traces in tree
- [ ] Public site copy says **“curated snapshot”** not “leaderboard” (already in findings.md — keep)

### E. Git readiness (local only until user says push)

- [ ] Single coherent initial commit **or** logical commit series on `feature/pre-push-ready` branch (follow AGENTS.md — **no direct commits to `main` by agent** unless user overrides)
- [ ] `git status` clean after commits
- [ ] Prepare push instructions for user: `git push -u origin main`, enable Pages source, verify URLs
- [ ] **Do not push**

### F. LinkedIn alignment (repo files only — do not edit linkedin repo unless user asks)

Prepare `docs/project/LINKEDIN_CLAIMS.md` mapping:

| External claim | Repo proof path |
|----------------|-----------------|
| Deterministic grading | `tasks/*/verifier.py`, validate_repo |
| Run provenance | sample `data/runs/*.json` fields |
| Curated reports | `data/reports/latest.json` |
| GitHub Pages hiscores | `docs/site/dist/hiscores.html` (post-push URL) |
| Issue-driven tasks | `.github/ISSUE_TEMPLATE/new-task.yml` |

---

## Execution phases

### Phase 1 — Audit (read-only)

1. Run `validate_repo.py`, `summarize_runs.py`, `build_site.py`; capture output.
2. Inventory models present in `data/runs/` vs `latest.json`.
3. Grep for stale docs (“no commit”, “single model”, “toy question only”).
4. Produce audit table: file → issue → fix.

### Phase 2 — Baseline runs (if Ollama available)

1. Confirm local models: `ollama list` (or document skip reason in PRE_PUSH_CHECKLIST).
2. Run batch per plan, e.g.:

```bash
# Example — adjust batch ids; repeat=5 per model per task suite
python3 scripts/run_batch.py --model llama3.2:3b --repeat 5 --batch-id baseline-20260531-llama3.2-3b
python3 scripts/run_batch.py --model granite3.2:2b --repeat 5 --batch-id baseline-20260531-granite3.2-2b
python3 scripts/run_batch.py --model gemma3:1b --repeat 5 --batch-id baseline-20260531-gemma3-1b
python3 scripts/run_batch.py --model phi4-mini --repeat 5 --batch-id baseline-20260531-phi4-mini
```

3. `python3 scripts/summarize_runs.py` → refresh `latest.json`.
4. Rebuild site; open/check `hiscores.html` lists all models.

If Ollama unavailable: document in PRE_PUSH_CHECKLIST, keep best existing runs, **do not fabricate** JSON runs.

### Phase 3 — Hardening

1. Add verifier **negative fixtures** (at least 2 tasks) — wrong answer must fail with explicit reason.
2. Extend `validate_repo.py` if needed (schema_version on report, model count warning, site dist exists).
3. Add `docs/agentic/PRE_PUSH_CHECKLIST.md` (operator steps for post-application push).
4. Update `HANDOFF.md` to current truth.
5. Optional: `scripts/check_links.py` for site internal links.

### Phase 4 — CI parity local

```bash
python -m py_compile scripts/*.py $(find tasks -name 'verifier.py' -print)
python3 scripts/validate_repo.py
python3 scripts/summarize_runs.py
python3 scripts/build_site.py
```

Must match `.github/workflows/ci.yml` steps.

### Phase 5 — Commit (local)

- Branch: `feature/pre-push-ready` (preferred) or user-approved `main`
- Message example:

```
feat: pre-push baseline, multi-model report, and validation hardening
```

- **Do not push.**

---

## Non-goals

- Prompt tuning to raise weak-model scores
- Broad leaderboard productization
- Cloud deployment, queues, workers (document scaling path only)
- Editing `~/Git/Personal/social/linkedin` (separate agent)
- Pushing to GitHub or enabling Pages (user after application)

---

## Output format (agent response)

```markdown
## Audit summary
(table)

## Baseline / report status
(models, runs, pass rates — honest if incomplete)

## Files changed
(bullets)

## Validation output
(paste validate_repo + CI-equivalent results)

## PRE_PUSH_CHECKLIST for operator
(numbered — what user runs after application to go live)

## URLs to verify after push
- https://github.com/shahzebqazi/benchmark-euterpea
- https://shahzebqazi.github.io/benchmark-euterpea/
- https://shahzebqazi.github.io/benchmark-euterpea/hiscores.html

## Honest gaps remaining
(bullets)
```

---

## Success criteria

- [ ] Repo self-validates (`validate_repo.py` green)
- [ ] Multi-model report OR documented Ollama blocker with honest findings.md
- [ ] Site builds with all models visible on hiscores
- [ ] PRE_PUSH_CHECKLIST exists; HANDOFF not stale
- [ ] Local git commits ready; **remote still unpushed**
- [ ] Zero fabricated runs or cert/completion claims

---

## One-line launch

```text
Read ~/Git/public/benchmark-euterpea/docs/agentic/pre-push-upgrade-agent.md and execute the full mission below the first ---. Do not git push.
```
