#!/usr/bin/env python3
"""Generate the GitHub Pages site."""

from __future__ import annotations

import html
import json
import statistics
import shutil
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "docs" / "site"
DIST_DIR = SITE_DIR / "dist"
REPORT_PATH = REPO_ROOT / "data" / "reports" / "latest.json"


GITHUB_URL = "https://github.com/shahzebqazi/benchmark-euterpea"


STYLE = """
:root {
  color-scheme: light;
  --bg: #f7f4ee;
  --paper: #fffdf8;
  --ink: #171717;
  --muted: #625d54;
  --faint: #91897b;
  --line: #d8d0c2;
  --line-strong: #aaa192;
  --accent: #4f46e5;
  --pass: #148044;
  --fail: #b42318;
  --warn: #9a5b0a;
  --unknown: #d8d0c2;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.58;
  text-rendering: optimizeLegibility;
}
a { color: var(--accent); text-underline-offset: 3px; }
.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(247, 244, 238, .94);
  border-bottom: 1px solid var(--line);
}
.header-inner, main, footer { max-width: 1180px; margin: 0 auto; padding: 0 24px; }
.header-inner { min-height: 62px; display: flex; align-items: center; justify-content: space-between; gap: 22px; }
.brand { color: var(--ink); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 750; text-decoration: none; }
nav { display: flex; flex-wrap: wrap; gap: 18px; }
nav a { color: var(--muted); font-size: .93rem; text-decoration: none; }
nav a:hover { color: var(--ink); text-decoration: underline; }
main { padding-top: 30px; padding-bottom: 74px; }
footer { border-top: 1px solid var(--line); color: var(--muted); padding-top: 28px; padding-bottom: 40px; }
h1, h2, h3 { line-height: 1.08; letter-spacing: -.03em; }
h1 { font-family: Georgia, "Times New Roman", serif; font-size: clamp(3rem, 7vw, 6.2rem); margin: 10px 0 18px; }
h2 { font-size: clamp(1.55rem, 3vw, 2.35rem); margin: 0 0 12px; }
h3 { font-size: 1.02rem; margin: 0 0 6px; }
p { margin-top: 0; }
code { background: #eee8dc; border: 1px solid var(--line); padding: 1px 5px; border-radius: 3px; font-size: .9em; }
pre { background: #181818; color: #f6efe4; border: 1px solid #303030; padding: 16px; overflow-x: auto; }
.eyebrow { color: var(--accent); font-size: .72rem; font-weight: 800; letter-spacing: .15em; text-transform: uppercase; }
.subtitle { max-width: 830px; color: #38332c; font-size: clamp(1.15rem, 2.2vw, 1.55rem); }
.muted { color: var(--muted); }
.small { font-size: .88rem; }
.section { margin-top: 50px; padding-top: 28px; border-top: 1px solid var(--line); }
.section:first-child, .hero + .section { border-top: 0; }
.section-head { display: grid; grid-template-columns: minmax(0, 1fr) minmax(280px, 470px); gap: 32px; align-items: end; margin-bottom: 18px; }
.lede { color: var(--muted); font-size: 1rem; }
.hero { padding: 34px 0 26px; border-bottom: 2px solid var(--ink); }
.hero-top { display: grid; grid-template-columns: minmax(0, 1fr) 260px; gap: 34px; align-items: end; }
.abstract { max-width: 940px; font-family: Georgia, "Times New Roman", serif; color: #28241f; font-size: 1.08rem; }
.stat-strip { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid var(--line-strong); border-bottom: 1px solid var(--line-strong); margin-top: 26px; }
.stat { padding: 13px 16px; border-right: 1px solid var(--line); }
.stat:last-child { border-right: 0; }
.stat strong { display: block; font-size: 1.55rem; line-height: 1; letter-spacing: -.04em; }
.stat span { color: var(--muted); font-size: .82rem; }
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 34px; }
.editorial-block { padding: 4px 0 0; }
.editorial-list { margin: 14px 0 0; padding: 0; list-style: none; border-top: 1px solid var(--line); }
.editorial-list li { padding: 11px 0; border-bottom: 1px solid var(--line); }
.pipeline { display: grid; grid-template-columns: 1fr 1fr 1fr; border: 1px solid var(--line-strong); background: var(--paper); }
.pipe-node { min-height: 118px; padding: 18px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); position: relative; }
.pipe-node:nth-child(3n) { border-right: 0; }
.pipe-node:nth-last-child(-n+3) { border-bottom: 0; }
.pipe-index { display: block; color: var(--faint); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .78rem; margin-bottom: 14px; }
.pipe-node b { display: block; }
.pipe-node span { color: var(--muted); font-size: .9rem; }
.integrity { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--line-strong); background: var(--paper); }
.integrity-step { padding: 18px; border-right: 1px solid var(--line); }
.integrity-step:last-child { border-right: 0; }
.integrity-step em { display: block; color: var(--muted); font-style: normal; font-size: .9rem; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; margin: 12px 0 0; background: var(--paper); }
th, td { border-bottom: 1px solid var(--line); padding: 10px 11px; text-align: left; vertical-align: top; }
th { background: #eee8dc; color: #443f38; font-size: .73rem; letter-spacing: .08em; text-transform: uppercase; }
tbody tr:hover td { background: #fbf8f1; }
.hero-graph { background: var(--paper); border: 1px solid var(--line-strong); padding: 18px; }
.model-row { display: grid; grid-template-columns: 180px minmax(180px, 1fr) 150px; gap: 14px; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--line); }
.model-row:last-child { border-bottom: 0; }
.stacked-bar { display: flex; height: 22px; border: 1px solid var(--line-strong); background: var(--unknown); }
.seg-pass { width: var(--pass-w); background: var(--pass); }
.seg-fail { width: var(--fail-w); background: var(--fail); }
.seg-unknown { width: var(--unknown-w); background: var(--unknown); }
.legend { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 12px; color: var(--muted); font-size: .86rem; }
.legend i { display: inline-block; width: 10px; height: 10px; margin-right: 5px; vertical-align: -1px; }
.pass-swatch { background: var(--pass); }
.fail-swatch { background: var(--fail); }
.unknown-swatch { background: var(--unknown); border: 1px solid var(--line-strong); }
.matrix-grid { display: grid; gap: 6px; min-width: 760px; }
.matrix-row { display: grid; grid-template-columns: 260px repeat(var(--cols), minmax(88px, 1fr)); gap: 6px; align-items: stretch; }
.matrix-head, .matrix-task { color: var(--muted); font-size: .86rem; }
.matrix-cell { display: grid; place-items: center; min-height: 34px; border: 1px solid var(--line); font-weight: 750; font-size: .82rem; }
.matrix-cell.pass { background: #dff0e5; color: #0f6a38; }
.matrix-cell.fail { background: #f7dedb; color: #9f1f17; }
.matrix-cell.partial { background: #f6e8c8; color: #81500a; }
.matrix-cell.empty { background: #ece6dc; color: var(--muted); }
.bar-list { display: grid; gap: 10px; }
.bar-row { display: grid; grid-template-columns: minmax(160px, 1fr) minmax(160px, 360px) 50px; gap: 12px; align-items: center; }
.thin-bar { height: 12px; background: #e6dfd3; border: 1px solid var(--line); }
.thin-bar span { display: block; width: var(--w); height: 100%; background: var(--pass); }
.thin-bar.fail span { background: var(--fail); }
.tag { display: inline-block; border: 1px solid var(--line); background: #f1eadf; padding: 1px 6px; margin: 1px 3px 1px 0; font-size: .78rem; white-space: nowrap; }
.schema-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }
.schema { background: #181818; color: #f6efe4; padding: 18px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .88rem; overflow-x: auto; }
.schema .comment { color: #a8a095; }
.timeline { border-left: 2px solid var(--ink); margin-left: 12px; }
.timeline-step { position: relative; padding: 0 0 24px 28px; }
.timeline-step::before { content: ""; position: absolute; left: -7px; top: 3px; width: 12px; height: 12px; border-radius: 50%; background: var(--ink); }
.gate { color: var(--warn); font-weight: 750; font-size: .82rem; text-transform: uppercase; letter-spacing: .08em; }
details { border-top: 1px solid var(--line); padding: 10px 0; }
summary { cursor: pointer; font-weight: 700; }
@media (max-width: 860px) {
  .header-inner, .hero-top, .section-head, .split, .schema-grid { display: block; }
  nav { gap: 10px; padding-bottom: 14px; }
  .stat-strip, .integrity, .pipeline { grid-template-columns: 1fr; display: grid; }
  .stat, .integrity-step, .pipe-node { border-right: 0; border-bottom: 1px solid var(--line); }
  .model-row { grid-template-columns: 1fr; }
}
"""


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def pct(value: float) -> str:
    return f"{round(value * 100, 1)}%"


def truncate(value: Any, limit: int = 92) -> str:
    text = str(value).replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "..."


def percent_bar(value: float, *, fail: bool = False) -> str:
    color_class = "fail" if fail else "pass"
    return f'<div class="thin-bar {color_class}" aria-label="{esc(pct(value))}"><span style="--w:{esc(pct(value))}"></span></div>'


def distribution(items: list[dict[str, Any]], key: str, *, empty: str = "none") -> str:
    if not items:
        return f'<span class="muted small">{esc(empty)}</span>'
    max_count = max(int(item.get("count", 0)) for item in items) or 1
    rows = []
    for item in items[:4]:
        count = int(item.get("count", 0))
        value = truncate(item.get(key, ""), 72)
        rows.append(
            '<div class="dist-row">'
            f'<span class="dist-label" title="{esc(item.get(key, ""))}">{esc(value)} x{esc(count)}</span>'
            f'{percent_bar(count / max_count, fail=key == "failure_reason")}'
            '</div>'
        )
    return '<div class="dist">' + "".join(rows) + "</div>"


def task_metadata_paths() -> list[Path]:
    return sorted((REPO_ROOT / "tasks").glob("**/metadata.json"))


def load_tasks() -> list[dict[str, Any]]:
    tasks = []
    for metadata_path in task_metadata_paths():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["_path"] = str(metadata_path.parent.relative_to(REPO_ROOT))
        tasks.append(metadata)
    return tasks


def report_summary(report: dict[str, Any], tasks: list[dict[str, Any]]) -> dict[str, Any]:
    results = report.get("results", [])
    runs = sum(int(result.get("runs", 0)) for result in results)
    passed = sum(int(result.get("passed", 0)) for result in results)
    failed = sum(int(result.get("failed", 0)) for result in results)
    models = sorted({result.get("model", "unknown") for result in results})
    pass_rate = passed / runs if runs else 0
    latencies = [float(result.get("latency_ms_avg", 0)) for result in results if result.get("latency_ms_avg") is not None]
    capability_counts: dict[str, int] = {}
    for task in tasks:
        capability_counts[task.get("capability", "unknown")] = capability_counts.get(task.get("capability", "unknown"), 0) + 1
    return {
        "runs": runs,
        "passed": passed,
        "failed": failed,
        "models": models,
        "pass_rate": pass_rate,
        "median_latency": statistics.median(latencies) if latencies else 0,
        "capability_counts": capability_counts,
    }


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} - benchmark-euterpea</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
    <a class="brand" href="index.html">benchmark-euterpea</a>
    <nav>
      <a href="index.html">Report</a>
      <a href="hiscores.html">Results Snapshot</a>
      <a href="methodology.html">Methodology</a>
      <a href="tasks.html">Task Catalog</a>
      <a href="workflow.html">Review Workflow</a>
      <a href="{GITHUB_URL}">GitHub</a>
    </nav>
    </div>
  </header>
  <main>
{body}
  </main>
  <footer>
    Generated from repository data. Raw local runs stay out of git; curated summaries feed this site.
  </footer>
</body>
</html>
"""


def load_report() -> dict[str, Any]:
    if not REPORT_PATH.exists():
        return {"generated_at": "not generated", "source_run_count": 0, "results": []}
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def pipeline_diagram() -> str:
    steps = [
        ("Task proposal", "capability, risk, expected failures"),
        ("Instruction", "model-facing prompt only"),
        ("Verifier", "hidden metadata and strict contract"),
        ("Raw run", "immutable model response with provenance"),
        ("Summary", "derived report grouped by model/task"),
        ("Failure corpus", "auditable repeated failure evidence"),
    ]
    nodes = []
    for index, (title, text) in enumerate(steps, start=1):
        nodes.append(
            '<div class="pipe-node">'
            f'<span class="pipe-index">{index:02d}</span>'
            f'<b>{esc(title)}</b>'
            f'<span>{esc(text)}</span>'
            '</div>'
        )
    return '<div class="pipeline">' + "".join(nodes) + "</div>"


def evidence_strip(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    summary = report_summary(report, tasks)
    stats = [
        (len(tasks), "task contracts"),
        (report.get("source_run_count", summary["runs"]), "raw run records"),
        (pct(summary["pass_rate"]), "snapshot pass rate"),
        (summary["failed"], "failed task/model rows"),
    ]
    return '<div class="stat-strip">' + "".join(
        f'<div class="stat"><strong>{esc(value)}</strong><span>{esc(label)}</span></div>' for value, label in stats
    ) + "</div>"


def capability_counts(tasks: list[dict[str, Any]], key: str = "capability") -> dict[str, int]:
    counts: dict[str, int] = {}
    for task in tasks:
        value = task.get(key, "unknown")
        counts[value] = counts.get(value, 0) + 1
    return counts


def coverage_table(tasks: list[dict[str, Any]]) -> str:
    rows = []
    for capability, count in sorted(capability_counts(tasks).items()):
        domains = sorted({task.get("domain", "unknown") for task in tasks if task.get("capability") == capability})
        rows.append(
            "<tr>"
            f"<td><strong>{esc(capability)}</strong></td>"
            f"<td>{esc(count)}</td>"
            f"<td>{esc(', '.join(domains))}</td>"
            "</tr>"
        )
    return f"""
      <table>
        <thead><tr><th>Capability</th><th>Tasks</th><th>Domains covered</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    """


def integrity_block() -> str:
    steps = [
        ("Prompt boundary", "Only instruction.md is model-facing; expected answers are not prompt content."),
        ("Verifier boundary", "verifier.py owns observable pass/fail behavior and strict failure reasons."),
        ("Raw artifact", "One JSON record preserves prompt, model, options, answer, decision, latency, and batch id."),
        ("Derived report", "latest.json and static pages summarize selected raw runs with provenance attached."),
    ]
    return '<div class="integrity">' + "".join(
        f'<div class="integrity-step"><h3>{esc(title)}</h3><em>{esc(text)}</em></div>' for title, text in steps
    ) + "</div>"


def failure_class(reason: str) -> str:
    text = reason.lower()
    if any(token in text for token in ("extra prose", "multiple tokens", "markdown", "invalid json", "extra keys")):
        return "output contract violation"
    if any(token in text for token in ("enharmonic", "spelling", "sharp", "flat")):
        return "symbolic spelling error"
    if any(token in text for token in ("duration", "counts notes", "scale-degree", "relative key")):
        return "symbolic reasoning error"
    return "exact-answer mismatch"


def model_summaries(report: dict[str, Any], tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    total_tasks = max(len(tasks), 1)
    for result in report.get("results", []):
        model = result.get("model", "unknown")
        entry = grouped.setdefault(
            model,
            {"model": model, "runs": 0, "passed": 0, "failed": 0, "tasks": set(), "batches": set(), "sources": set(), "options": set()},
        )
        entry["runs"] += int(result.get("runs", 0))
        entry["passed"] += int(result.get("passed", 0))
        entry["failed"] += int(result.get("failed", 0))
        entry["tasks"].add(result.get("task_id", "unknown"))
        entry["batches"].update(result.get("batch_ids", []))
        entry["sources"].update(result.get("source_files", []))
        entry["options"].update(result.get("model_options", []))
    summaries = []
    for entry in grouped.values():
        runs = entry["runs"]
        entry["pass_rate"] = entry["passed"] / runs if runs else 0
        entry["coverage"] = len(entry["tasks"]) / total_tasks
        summaries.append(entry)
    return sorted(summaries, key=lambda item: (-item["pass_rate"], item["model"]))


def model_comparison_chart(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    rows = []
    for entry in model_summaries(report, tasks):
        total = max(entry["runs"], 1)
        pass_w = entry["coverage"] * (entry["passed"] / total)
        fail_w = entry["coverage"] * (entry["failed"] / total)
        unknown_w = max(0, 1 - entry["coverage"])
        rows.append(
            '<div class="model-row">'
            f'<div><strong>{esc(entry["model"])}</strong><br><span class="muted small">{esc(len(entry["tasks"]))}/{esc(len(tasks))} tasks covered</span></div>'
            '<div class="stacked-bar" '
            f'style="--pass-w:{esc(pct(pass_w))};--fail-w:{esc(pct(fail_w))};--unknown-w:{esc(pct(unknown_w))}">'
            '<span class="seg-pass"></span><span class="seg-fail"></span><span class="seg-unknown"></span>'
            '</div>'
            f'<div><strong>{esc(pct(entry["pass_rate"]))}</strong><br><span class="muted small">{esc(entry["passed"])}/{esc(entry["runs"])} passed</span></div>'
            '</div>'
        )
    legend = (
        '<div class="legend">'
        '<span><i class="pass-swatch"></i>passed</span>'
        '<span><i class="fail-swatch"></i>failed</span>'
        '<span><i class="unknown-swatch"></i>not covered</span>'
        '</div>'
    )
    return '<div class="hero-graph">' + ("".join(rows) or '<p class="muted">No model runs reported yet.</p>') + legend + "</div>"


def score_matrix(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    models = [entry["model"] for entry in model_summaries(report, tasks)]
    result_by_key = {(result.get("task_id"), result.get("model")): result for result in report.get("results", [])}
    header = '<div class="matrix-row" style="--cols:{0}"><div></div>{1}</div>'.format(
        max(len(models), 1),
        "".join(f'<div class="matrix-head">{esc(model)}</div>' for model in models),
    )
    rows = []
    for task in sorted(tasks, key=lambda item: item.get("id", "")):
        cells = []
        for model in models:
            result = result_by_key.get((task.get("id"), model))
            if not result:
                cells.append('<div class="matrix-cell empty">not run</div>')
                continue
            rate = float(result.get("pass_rate", 0))
            css = "pass" if rate == 1 else "fail" if rate == 0 else "partial"
            cells.append(f'<div class="matrix-cell {css}">{esc(result.get("passed"))}/{esc(result.get("runs"))}</div>')
        rows.append(
            f'<div class="matrix-row" style="--cols:{max(len(models), 1)}">'
            f'<div class="matrix-task"><strong>{esc(task.get("id"))}</strong><br>{esc(task.get("domain"))}</div>'
            f'{"".join(cells)}</div>'
        )
    return '<div class="table-wrap"><div class="matrix-grid">' + header + "".join(rows) + "</div></div>"


def failure_distribution_chart(report: dict[str, Any]) -> str:
    counts: dict[str, int] = {}
    for result in report.get("results", []):
        for item in result.get("failure_distribution", []):
            klass = failure_class(item.get("failure_reason", ""))
            counts[klass] = counts.get(klass, 0) + int(item.get("count", 0))
    max_count = max(counts.values()) if counts else 1
    rows = []
    for label, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        rows.append(
            '<div class="bar-row">'
            f'<span>{esc(label)}</span>'
            f'{percent_bar(count / max_count, fail=True)}'
            f'<strong>{esc(count)}</strong>'
            '</div>'
        )
    return '<div class="bar-list">' + ("".join(rows) or '<p class="muted">No verifier failures in this report.</p>') + "</div>"


def first_answer(result: dict[str, Any]) -> str:
    answers = result.get("answer_distribution", [])
    return answers[0].get("answer", "") if answers else ""


def failure_examples_table(report: dict[str, Any]) -> str:
    rows = []
    for result in sorted(report.get("results", []), key=lambda item: (item.get("task_id", ""), item.get("model", ""))):
        if int(result.get("failed", 0)) == 0:
            continue
        metadata = result.get("task_metadata", {})
        reason = result.get("failure_distribution", [{}])[0].get("failure_reason", result.get("failure_reason", ""))
        rows.append(
            "<tr>"
            f"<td><strong>{esc(result.get('task_id'))}</strong><br><span class=\"muted small\">{esc(result.get('model'))}</span></td>"
            f"<td>{esc(metadata.get('expected_behavior', ''))}</td>"
            f"<td><code>{esc(truncate(first_answer(result), 140))}</code></td>"
            f"<td>{esc(reason)}</td>"
            "</tr>"
        )
    return f"""
      <table>
        <thead><tr><th>Task</th><th>Expected behavior</th><th>Observed answer</th><th>Verifier reason</th></tr></thead>
        <tbody>{''.join(rows) or '<tr><td colspan="4">No failure examples in this report.</td></tr>'}</tbody>
      </table>
    """


def observed_answers_table(report: dict[str, Any]) -> str:
    rows = []
    for result in sorted(report.get("results", []), key=lambda item: (item.get("task_id", ""), item.get("model", ""))):
        answers = "; ".join(f"{truncate(item.get('answer', ''), 80)} x{item.get('count', 0)}" for item in result.get("answer_distribution", [])[:3])
        rows.append(
            "<tr>"
            f"<td>{esc(result.get('task_id'))}</td>"
            f"<td>{esc(result.get('model'))}</td>"
            f"<td>{esc(answers)}</td>"
            "</tr>"
        )
    return f"""
      <table>
        <thead><tr><th>Task</th><th>Model</th><th>Observed answers</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    """


def provenance_table(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    rows = []
    for entry in model_summaries(report, tasks):
        sample_sources = sorted(entry["sources"])[:3]
        details = "".join(f'<li><code>{esc(source)}</code></li>' for source in sample_sources)
        rows.append(
            "<tr>"
            f"<td><strong>{esc(entry['model'])}</strong></td>"
            f"<td>{esc(', '.join(sorted(entry['batches'])))}</td>"
            f"<td>{esc(len(entry['sources']))} files<details><summary>sample paths</summary><ul>{details}</ul></details></td>"
            f"<td>{esc('; '.join(sorted(entry['options'])) or 'not recorded')}</td>"
            "</tr>"
        )
    return f"""
      <table>
        <thead><tr><th>Model</th><th>Batch ids</th><th>Source files</th><th>Model options</th></tr></thead>
        <tbody>{''.join(rows) or '<tr><td colspan="4">No provenance recorded.</td></tr>'}</tbody>
      </table>
      <p class="muted small">Report generated at {esc(report.get("generated_at"))}; source run count: {esc(report.get("source_run_count", 0))}.</p>
    """


def index_page(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    summary = report_summary(report, tasks)
    return page(
        "Engineer-facing benchmark",
        f"""
    <section class="hero">
      <div class="hero-top">
        <div>
          <div class="eyebrow">Benchmark data-platform slice</div>
          <h1>benchmark-euterpea</h1>
          <p class="subtitle">A small original benchmark suite for model competence and agent compliance under deterministic grading.</p>
        </div>
        <div class="muted small">
          Latest report: {esc(report.get("generated_at"))}<br>
          Baseline models: {esc(len(summary["models"]))}<br>
          Scope: local file-backed evaluation slice
        </div>
      </div>
      {evidence_strip(report, tasks)}
    </section>

    <section class="section">
      <div class="eyebrow">Abstract</div>
      <p class="abstract">benchmark-euterpea is a compact evaluation data platform for studying whether models can satisfy precise task contracts under deterministic grading. The first controlled domain is music theory because symbolic answers make correctness easy to audit, failures are interpretable, and the path naturally extends into Haskell/Euterpea-style solver tasks. The project is intentionally local and modest in sample size, but complete in shape: task definitions, hidden verifier metadata, strict verifiers, raw run artifacts, derived reports, validation checks, and a static report site. The engineering emphasis is not score maximization. It is the integrity of the benchmark lifecycle: preserving provenance, separating raw evidence from curated summaries, making failure modes reviewable, and keeping the contracts simple enough to scale into workers, queues, object storage, dashboards, and reviewer workflows.</p>
    </section>

    <section class="section split">
      <article class="editorial-block">
        <div class="eyebrow">What is being evaluated?</div>
        <h2>Symbolic correctness and compliance under strict contracts.</h2>
        <ul class="editorial-list">
          <li><strong>Music theory:</strong> scale degrees, key signatures, relative keys, chord spelling, and enharmonic traps.</li>
          <li><strong>Agent compliance:</strong> exact output, JSON-only output, and multi-step instruction following.</li>
          <li><strong>Euterpea stubs:</strong> symbolic pitch and duration reasoning that can grow toward Haskell solver tasks.</li>
        </ul>
      </article>
      <article class="editorial-block">
        <div class="eyebrow">What makes it auditable?</div>
        <h2>The artifact keeps boundaries visible.</h2>
        <ul class="editorial-list">
          <li>Expected answers live in metadata and verifier code, not in the model-facing prompt.</li>
          <li>Raw runs keep model outputs, options, latency, decisions, failure reasons, source paths, and batch ids.</li>
          <li>Public reports are derived snapshots, not mutable source data or broad model-ranking claims.</li>
        </ul>
      </article>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Pipeline</div>
          <h2>Evaluation dataflow, not prompt tuning.</h2>
        </div>
        <p class="lede">Each task moves through a reproducible chain from reviewable proposal to model-facing instruction, verifier, raw run artifact, derived report, and failure evidence.</p>
      </div>
      {pipeline_diagram()}
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Current evidence</div>
          <h2>What the latest report actually supports.</h2>
        </div>
        <p class="lede">The current snapshot is small by design. It demonstrates end-to-end benchmark infrastructure and exposes failures with enough context to audit them.</p>
      </div>
      <div class="split">
        <div>{model_comparison_chart(report, tasks)}</div>
        <div>
          <h3>Most common observed failure classes</h3>
          {failure_distribution_chart(report)}
          <p class="muted small">Failure classes are derived from verifier reasons for readability; full reasons remain available in the results page.</p>
        </div>
      </div>
      <p><a href="hiscores.html">Open the full results snapshot</a>.</p>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Benchmark integrity</div>
          <h2>Four boundaries keep the report reproducible.</h2>
        </div>
        <p class="lede">The project separates what the model sees, what the verifier knows, what raw evidence records, and what public pages summarize.</p>
      </div>
      {integrity_block()}
    </section>

    <section class="section split">
      <article>
        <div class="eyebrow">Coverage</div>
        <h2>Current task coverage</h2>
        <p class="muted">Music theory is the first symbolic control domain; agent-compliance and Euterpea stubs keep the SWE story visible.</p>
        {coverage_table(tasks)}
      </article>
      <article>
        <div class="eyebrow">Limitations</div>
        <h2>Current scope</h2>
        <p class="muted">This is a small local benchmark with a curated snapshot, not a broad model ranking. The current report may include partial model coverage when local Ollama is unavailable; the site shows uncovered task/model cells explicitly. Future work is more tasks, verifier fixtures, repeated baselines, reviewer workflows, and queue-backed execution.</p>
        <p><a href="methodology.html">Read methodology</a> · <a href="{GITHUB_URL}">Open GitHub</a></p>
      </article>
    </section>
""",
    )


def hiscores_page(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    summary = report_summary(report, tasks)
    return page(
        "Results Snapshot",
        f"""
    <section class="hero">
      <div class="eyebrow">Curated derived report</div>
      <h1>Model Baseline Comparison</h1>
      <p class="subtitle">A results-first view of every model benchmarked so far. Bars show pass/fail counts and task coverage so the snapshot remains honest at small scale.</p>
      {model_comparison_chart(report, tasks)}
      {evidence_strip(report, tasks)}
    </section>

    <section class="section split">
      <div>
        <div class="eyebrow">Failure distribution</div>
        <h2>What failed?</h2>
        {failure_distribution_chart(report)}
      </div>
      <div>
        <div class="eyebrow">Interpretation boundary</div>
        <h2>Curated snapshot, not a leaderboard.</h2>
        <p class="muted">This page compares only models present in <code>data/reports/latest.json</code>. The latest report has {esc(summary["runs"])} grouped runs across {esc(len(tasks))} task contracts and {esc(len(summary["models"]))} model baseline(s), with coverage cells marked when a model was not run on a task. It is evidence for the harness and failure modes, not a broad ranking claim.</p>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Score matrix</div>
          <h2>Task-by-model outcomes.</h2>
        </div>
        <p class="lede">The matrix is the compact benchmark view: tasks down the page, models across the page, deterministic verifier outcomes in each cell.</p>
      </div>
      {score_matrix(report, tasks)}
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Failure evidence</div>
          <h2>Verifier-visible failures.</h2>
        </div>
        <p class="lede">Failure examples show expected behavior, observed answer, and verifier reason. This is the most useful slice for improving task definitions and verifier fixtures.</p>
      </div>
      <div class="table-wrap">{failure_examples_table(report)}</div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Observed answers</div>
          <h2>Raw answer summary.</h2>
        </div>
        <p class="lede">Answer distributions are shown as compact evidence rather than ornamental per-row charts; repeated samples make disagreement visible when the raw runs are available.</p>
      </div>
      <div class="table-wrap">{observed_answers_table(report)}</div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Provenance</div>
          <h2>Where the report came from.</h2>
        </div>
        <p class="lede">Batch ids, source files, and model options are grouped by model instead of repeated inside every score row.</p>
      </div>
      <div class="table-wrap">{provenance_table(report, tasks)}</div>
    </section>
""",
    )


def methodology_page() -> str:
    return page(
        "Methodology",
        f"""
    <section class="hero">
      <div class="eyebrow">Methodology</div>
      <h1>Benchmark contracts before benchmark scores.</h1>
      <p class="subtitle">The project treats evaluation as a data lifecycle: task authorship, hidden verifier metadata, deterministic grading, immutable raw runs, derived reports, validation, and review.</p>
    </section>

    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Data lifecycle</div><h2>From proposed task to derived report.</h2></div><p class="lede">The same contract can stay local or move into queue-backed execution because every transition has a concrete artifact.</p></div>
      {pipeline_diagram()}
    </section>

    <section class="section">
      <h2>Task authorship</h2>
      <p>Tasks are authored for this benchmark rather than copied from quiz banks. Each task records capability, complexity, domain, expected behavior, expected failure modes, and contamination risk. Common music-theory concepts are allowed when wording and variants are original and the risk is documented.</p>
      <h2>Prompt/verifier boundary</h2>
      <p>The model sees <code>instruction.md</code>. Expected answers live in <code>metadata.json</code> and <code>verifier.py</code>. Verifiers grade observable behavior, not intent, and validation confirms each verifier imports correctly, returns the expected tuple contract, and accepts its metadata expected answer.</p>
      <h2>Run provenance</h2>
      <p>Every raw run preserves the model-facing prompt, model name, options, raw answer, verifier decision, failure reason, latency, batch id, sample index, task path, and metadata snapshot. This keeps surprising results inspectable without trusting the generated report.</p>
      <h2>Raw vs derived data</h2>
      <p>Raw run JSON files are source data. <code>data/reports/latest.json</code> and the static site are derived artifacts generated from selected raw runs. Public pages should summarize evidence, not become the mutable source of truth.</p>
      <h2>Failure taxonomy</h2>
      <p>Verifier failures are grouped for readability into output contract violations, symbolic spelling errors, symbolic reasoning errors, and exact-answer mismatches. The original verifier reason remains attached to failure examples so the taxonomy never replaces the underlying evidence.</p>
      <h2>Limitations</h2>
      <p>The current suite is intentionally small and local. It demonstrates a complete benchmark platform slice, not a comprehensive model ranking. Future work is repeated baselines, verifier regression fixtures, queue-backed workers, durable run storage, dashboards, and reviewer workflows.</p>
    </section>

    <section class="section schema-grid">
      <div>
        <div class="eyebrow">Raw run artifact</div>
        <pre class="schema"><span class="comment">schema_version</span>
run_at
batch_id
sample_index
task_id / task_path
task_metadata
model / harness / ollama_options
prompt
raw_answer
passed / failure_reason
latency_ms / ollama_metrics</pre>
      </div>
      <div>
        <div class="eyebrow">Derived report</div>
        <pre class="schema"><span class="comment">schema_version</span>
generated_at
source_run_count
results[]:
  task_id
  model
  runs / passed / failed / pass_rate
  answer_distribution
  failure_distribution
  latency_ms_avg
  batch_ids / source_files / model_options</pre>
      </div>
    </section>
""",
    )


def tasks_page() -> str:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for metadata in load_tasks():
        grouped.setdefault(metadata.get("capability", "unknown"), []).append(metadata)
    groups = []
    for capability, items in sorted(grouped.items()):
        rows = []
        for metadata in sorted(items, key=lambda item: (item.get("complexity", ""), item.get("id", ""))):
            failures = ", ".join(metadata.get("expected_failure_modes", []))
            rows.append(
                "<tr>"
                f"<td><strong>{esc(metadata.get('id'))}</strong><br><span class=\"muted small\"><code>{esc(metadata.get('_path'))}</code></span></td>"
                f"<td>{esc(metadata.get('capability'))}</td>"
                f"<td>{esc(metadata.get('domain'))}</td>"
                f"<td>{esc(metadata.get('complexity'))}</td>"
                f"<td>{esc(metadata.get('contamination_risk'))}</td>"
                f"<td>{esc(failures)}</td>"
                "</tr>"
            )
        groups.append(
            f"""
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Capability</div><h2>{esc(capability)}</h2></div><p class="lede">{esc(len(items))} task contracts</p></div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Task id</th><th>Capability</th><th>Domain</th><th>Complexity</th><th>Contamination risk</th><th>Expected failure modes</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </section>
"""
        )
    return page(
        "Tasks",
        f"""
    <section class="hero">
      <div class="eyebrow">Task catalog</div>
      <h1>Executable verifier contracts.</h1>
      <p class="subtitle">Tasks are grouped by capability and discovered from <code>tasks/**/metadata.json</code>. Expected answers are verifier metadata, not the headline of the public UI.</p>
    </section>
    <section class="section split">
      <div>
        <div class="eyebrow">Coverage</div>
        <h2>Capability and domain coverage.</h2>
        {coverage_table(load_tasks())}
      </div>
      <div>
        <div class="eyebrow">Catalog policy</div>
        <h2>Compact rows over task cards.</h2>
        <p class="muted">The catalog emphasizes contract metadata: task id, capability, domain, complexity, contamination risk, and expected failure modes. Expected answers stay out of the primary display because they are verifier metadata.</p>
      </div>
    </section>
    {"".join(groups)}
""",
    )


def workflow_page() -> str:
    steps = [
        ("Proposal", "Open a GitHub issue with capability, model-facing instruction, verifier idea, contamination risk, and expected failure modes.", "human approval required"),
        ("Contamination review", "Check copied wording, public exposure, and whether the task measures a meaningful symbolic or compliance behavior.", "human approval required"),
        ("Verifier review", "Add metadata and deterministic verifier code. Keep expected answers outside the prompt boundary.", "human approval required"),
        ("Validation", "Run repository checks for metadata, verifier contracts, leakage, report shape, and static site generation.", "automated gate"),
        ("Baseline run", "Collect local model outputs as raw run artifacts with batch ids, model options, latency, and failure reasons.", "operator controlled"),
        ("Report promotion", "Summarize selected raw runs into the derived report and promote repeated failures into fixtures or task proposals.", "human approval required"),
    ]
    workflow = "".join(
        '<article class="timeline-step">'
        f'<div class="gate">{esc(gate)}</div>'
        f'<h3>{esc(title)}</h3>'
        f'<p class="muted">{esc(text)}</p>'
        '</article>'
        for title, text, gate in steps
    )
    return page(
        "Issue workflow",
        f"""
    <section class="hero">
      <div class="eyebrow">Review workflow</div>
      <h1>GitHub Issues as benchmark backlog.</h1>
      <p class="subtitle">Issues are the intake surface for task proposals, failure reports, contamination review, verifier design, validation, baseline runs, and report promotion.</p>
    </section>
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Process timeline</div><h2>Review gates before report promotion.</h2></div><p class="lede">Human review belongs at task definition, contamination, verifier design, and report promotion. Automation guards repeatable validation.</p></div>
      <div class="timeline">{workflow}</div>
    </section>
    <section class="section">
      <h2>Failure report evidence</h2>
      <p>Failure reports should include model, observed answer, expected behavior, raw run path when available, and why the failure improves the benchmark.</p>
      <p><a href="{GITHUB_URL}/issues">Open the GitHub issue tracker</a>.</p>
    </section>
""",
    )


def main() -> int:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    (DIST_DIR / "assets").mkdir(parents=True)
    (DIST_DIR / "assets" / "style.css").write_text(STYLE.strip() + "\n", encoding="utf-8")

    report = load_report()
    tasks = load_tasks()
    pages = {
        "index.html": index_page(report, tasks),
        "hiscores.html": hiscores_page(report, tasks),
        "methodology.html": methodology_page(),
        "tasks.html": tasks_page(),
        "workflow.html": workflow_page(),
    }
    for filename, content in pages.items():
        (DIST_DIR / filename).write_text(content, encoding="utf-8")
    print(f"wrote {DIST_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
