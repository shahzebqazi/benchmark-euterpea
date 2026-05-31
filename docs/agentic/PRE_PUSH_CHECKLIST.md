# Pre-Push Checklist

Use this after the application materials are complete and the user is ready to publish. Do not push this repository earlier.

## Current Local Status

- Branch target: `feature/pre-push-ready`.
- Public remote: `https://github.com/shahzebqazi/benchmark-euterpea`.
- Remote publication is intentionally pending user approval.
- Latest local audit found `ollama list` blocked by a local filesystem error: `mkdir /Users/sqazi/.ollama/models: file exists: ensure path elements are traversable`.
- Because Ollama is blocked, the checked-in curated report is honest partial evidence, not a fabricated four-model full-suite baseline.

## Validation Before Push

Run from the repo root:

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

Expected result: each command exits `0`. `validate_repo.py` may warn when the latest report is partial by model coverage; that warning is acceptable until a full matrix is run.

## Optional Full Baseline

If Ollama works locally, run the full target matrix before publishing a stronger report:

```bash
python3 scripts/run_batch.py --model llama3.2:3b --repeat 5 --batch-id baseline-20260531-llama3.2-3b
python3 scripts/run_batch.py --model granite3.2:2b --repeat 5 --batch-id baseline-20260531-granite3.2-2b
python3 scripts/run_batch.py --model gemma3:1b --repeat 5 --batch-id baseline-20260531-gemma3-1b
python3 scripts/run_batch.py --model phi4-mini --repeat 5 --batch-id baseline-20260531-phi4-mini
python3 scripts/summarize_runs.py \
  --batch-id baseline-20260531-llama3.2-3b \
  --batch-id baseline-20260531-granite3.2-2b \
  --batch-id baseline-20260531-gemma3-1b \
  --batch-id baseline-20260531-phi4-mini
python3 scripts/build_site.py
python3 scripts/check_links.py
```

Do not hand-edit or fabricate JSON runs. If a model is unavailable, leave the report partial and document the reason in `docs/research/findings.md`.

## Publish Steps

1. Review `git status` and confirm there are no secrets or private traces.
2. Confirm the local commit series is on `feature/pre-push-ready`.
3. Push only after the application is complete:

```bash
git push -u origin feature/pre-push-ready
```

4. Open a PR into `main`, let CI and PR policy checks run, and request human review for public claims and raw-data publication decisions.
5. After merge, enable GitHub Pages through the repository Pages workflow if it is not already active.
6. Verify public URLs:
   - `https://github.com/shahzebqazi/benchmark-euterpea`
   - `https://shahzebqazi.github.io/benchmark-euterpea/`
   - `https://shahzebqazi.github.io/benchmark-euterpea/hiscores.html`
