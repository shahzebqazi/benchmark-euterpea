# Reports

Curated benchmark summaries live here.

- `latest.json`: current public summary consumed by the GitHub Pages site.
- Commit curated report JSON that has been regenerated from local raw runs and reviewed for public claims.
- Do not commit full local raw run corpora by default; raw run JSON stays in `data/runs/` and is ignored unless a human explicitly approves selected sample publication.
- The generated site in `docs/site/dist/` stays local/CI-generated and should be rebuilt from the committed report before publishing.

Generate a report from raw runs:

```bash
python3 scripts/summarize_runs.py
```

Build the static hiscore site:

```bash
python3 scripts/build_site.py
```

Reports include model/task pass rates, answer distributions, failure distributions, latency averages, batch ids, schema version, source run count, model options, and source file paths. Source paths are provenance pointers into local or reviewed raw runs; the report must still contain enough aggregate evidence to stand on its own in a public clone. Public summaries are curated snapshots rather than final leaderboard claims.
