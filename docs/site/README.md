# Site

The public report is generated into `docs/site/dist/` by `scripts/build_site.py` from task metadata and `data/reports/latest.json`.

Rebuild after report or task changes:

```bash
python3 scripts/summarize_runs.py
python3 scripts/build_site.py
```

Preview locally:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs/site/dist
```

Then open http://127.0.0.1:8765/

Pages:

- `index.html` — benchmark report and scope
- `hiscores.html` — model baseline comparison
- `tasks.html` — task catalog and coverage roadmap
- `methodology.html` — evaluation methodology
- `workflow.html` — review workflow and community run reproduction
- `references.html` — external methodology anchors
