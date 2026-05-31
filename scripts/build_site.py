#!/usr/bin/env python3
"""Generate the GitHub Pages site."""

from __future__ import annotations

import html
import json
import statistics
import shutil
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "docs" / "site"
DIST_DIR = SITE_DIR / "dist"
REPORT_PATH = REPO_ROOT / "data" / "reports" / "latest.json"


GITHUB_URL = "https://github.com/shahzebqazi/benchmark-euterpea"


BENCHMARK_SECTIONS = [
    {
        "id": "music-theory-recognition",
        "title": "Music Theory Recognition",
        "summary": "Core recognition tasks such as relative keys, key signatures, and scale degrees.",
        "icon": "🎼",
    },
    {
        "id": "tonal-spelling-enharmonics",
        "title": "Tonal Spelling & Enharmonics",
        "summary": "Exact note spelling, chord spelling, accidentals, and enharmonic traps.",
        "icon": "♯",
    },
    {
        "id": "rhythm-duration-reasoning",
        "title": "Rhythm & Duration Reasoning",
        "summary": "Beat, duration, and symbolic time arithmetic.",
        "icon": "⏱",
    },
    {
        "id": "symbolic-transformation",
        "title": "Symbolic Transformation",
        "summary": "Operations that rewrite symbolic music while preserving spelling and structure.",
        "icon": "↔",
    },
    {
        "id": "symbolic-music-euterpea",
        "title": "Symbolic Music / Euterpea",
        "summary": "Haskell/Euterpea-shaped tasks that can grow into solver-backed evaluation.",
        "icon": "λ",
    },
    {
        "id": "instruction-output-compliance",
        "title": "Instruction / Output Compliance",
        "summary": "Exact-response tasks where the contract is obeying the output boundary.",
        "icon": "⌘",
    },
    {
        "id": "structured-output-fidelity",
        "title": "Structured Output Fidelity",
        "summary": "Machine-readable response formats such as strict JSON.",
        "icon": "{}",
    },
    {
        "id": "multi-step-constraint-following",
        "title": "Multi-Step Constraint Following",
        "summary": "Tasks where intermediate reasoning must not leak into the final answer.",
        "icon": "⛓",
    },
    {
        "id": "representation-translation",
        "title": "Representation Translation",
        "summary": "Translation between notation, symbolic forms, and plain-language descriptions.",
        "icon": "⇄",
    },
    {
        "id": "verifier-robustness-ambiguity",
        "title": "Verifier Robustness / Ambiguity Cases",
        "summary": "Near-miss and ambiguity cases used to harden deterministic grading.",
        "icon": "✓",
    },
]


SECTION_BY_ID = {section["id"]: section for section in BENCHMARK_SECTIONS}


TASK_SECTION_OVERRIDES = {
    "a-minor-relative-major": "music-theory-recognition",
    "b-flat-major-key-signature": "music-theory-recognition",
    "c-major-fifth": "music-theory-recognition",
    "d-major-third": "music-theory-recognition",
    "f-major-key-signature": "music-theory-recognition",
    "c-major-triad-spelling": "tonal-spelling-enharmonics",
    "e-sharp-enharmonic": "tonal-spelling-enharmonics",
    "g-sharp-minor-leading-tone": "tonal-spelling-enharmonics",
    "haskell-duration-sum": "rhythm-duration-reasoning",
    "transpose-line": "symbolic-transformation",
    "output-only-token": "instruction-output-compliance",
    "json-only-status": "structured-output-fidelity",
    "multi-step-output": "multi-step-constraint-following",
    "e-major-sixth": "music-theory-recognition",
    "g-major-key-signature-count": "music-theory-recognition",
    "e-minor-relative-major": "music-theory-recognition",
    "minor-second-semitones": "music-theory-recognition",
    "dorian-sixth-degree": "music-theory-recognition",
    "f-sharp-major-leading-tone": "tonal-spelling-enharmonics",
    "d-flat-major-triad-spelling": "tonal-spelling-enharmonics",
    "b-diminished-triad-spelling": "tonal-spelling-enharmonics",
    "c-sharp-harmonic-minor-leading-tone": "tonal-spelling-enharmonics",
    "a-flat-major-seventh-chord": "tonal-spelling-enharmonics",
    "half-plus-quarter-duration": "rhythm-duration-reasoning",
    "dotted-half-duration": "rhythm-duration-reasoning",
    "three-four-bar-fit": "rhythm-duration-reasoning",
    "four-four-remaining-beats": "rhythm-duration-reasoning",
    "transpose-down-line": "symbolic-transformation",
    "retrograde-line": "symbolic-transformation",
    "double-duration-list": "symbolic-transformation",
    "euterpea-trans-pitch": "symbolic-music-euterpea",
    "euterpea-scale-durations": "symbolic-music-euterpea",
    "no-markdown-token": "instruction-output-compliance",
    "lowercase-only-token": "instruction-output-compliance",
    "branch-policy-decision": "instruction-output-compliance",
    "secret-redaction-decision": "instruction-output-compliance",
    "expected-answer-leakage": "instruction-output-compliance",
    "json-array-enum": "structured-output-fidelity",
    "music-note-json": "structured-output-fidelity",
    "patch-summary-json": "structured-output-fidelity",
    "pitch-list-to-json": "representation-translation",
    "json-to-compact-chord": "representation-translation",
    "two-step-final-token": "multi-step-constraint-following",
    "music-final-only": "multi-step-constraint-following",
    "ordered-transform-final": "multi-step-constraint-following",
    "verifier-false-positive-label": "verifier-robustness-ambiguity",
    "verifier-false-negative-label": "verifier-robustness-ambiguity",
    "punctuation-strictness-label": "verifier-robustness-ambiguity",
}


TASK_BACKLOG = {
    "music-theory-recognition": {
        "source": "Open Music Theory: scale degrees, key signatures, intervals, modes, and chord qualities.",
        "families": [
            "Scale-degree variants across sharp and flat keys",
            "Key-signature counts and accidental lists",
            "Relative and parallel major/minor identification",
            "Interval size and quality recognition",
            "Mode and chord-quality recognition with compact answers",
        ],
    },
    "tonal-spelling-enharmonics": {
        "source": "Music-theory manuals: enharmonic equivalence, altered degrees, double accidentals, triads, and seventh chords.",
        "families": [
            "Double-sharp and double-flat spelling traps",
            "Harmonic-minor leading-tone spelling",
            "Altered scale-degree note naming",
            "Triad and seventh-chord spelling with exact delimiters",
            "Enharmonic-near-miss rejection cases",
        ],
    },
    "rhythm-duration-reasoning": {
        "source": "Open music-theory rhythm units: note values, rests, beat counts, simple meter, and bar completion.",
        "families": [
            "Duration sums in quarter-note units",
            "Rest-value arithmetic",
            "Simple meter fit checks",
            "Dotted value arithmetic",
            "Bar-completion and remaining-beat tasks",
        ],
    },
    "symbolic-transformation": {
        "source": "Parser-backed symbolic music structures: pitch lists, durations, melodies, and transforms.",
        "families": [
            "Pitch-list transposition with octave preservation",
            "Interval shifts with accidentals",
            "Retrograde over short melodies",
            "Inversion around an anchor pitch",
            "Duration scaling and transform composition",
        ],
    },
    "symbolic-music-euterpea": {
        "source": "Euterpea/Haskell concepts: Pitch, PitchClass, Octave, Dur, Music, note, transpose, absPitch, pitch, trans, scaleDurations.",
        "families": [
            "Euterpea expression evaluation to compact pitch output",
            "Dur arithmetic over note and rest constructors",
            "Music value normalization",
            "Transposition and scaleDurations reasoning",
            "Future solver-backed Haskell tasks with executable checks",
        ],
    },
    "instruction-output-compliance": {
        "source": "IFEval and Datacurve/DeepSWE: objectively verifiable constraints, short natural prompts, and behavioral grading.",
        "families": [
            "Exact-token and no-prose outputs",
            "No markdown or quote wrapping",
            "Branch-policy and no-main-commit decisions",
            "Secret-redaction and safe-output decisions",
            "Expected-answer leakage and prompt-boundary compliance",
        ],
    },
    "structured-output-fidelity": {
        "source": "IFEval, SchemaBench, and BigCodeBench: strict schema-like output and practical structured artifacts.",
        "families": [
            "JSON objects with required keys and no extras",
            "Allowed enum values and exact arrays",
            "Nested JSON for music structures",
            "Patch-summary JSON for coding-agent workflows",
            "CSV/TSV delimiter tasks after fixtures mature",
        ],
    },
    "multi-step-constraint-following": {
        "source": "FollowBench/IFEval-style layered constraints plus Datacurve-style underspecified developer prompts.",
        "families": [
            "Hidden-intermediate reasoning with final-only output",
            "Ordered symbolic transforms",
            "Music reasoning plus exact output constraints",
            "Agent procedure compliance with a single artifact",
            "Short natural prompts requiring constraint discovery",
        ],
    },
    "representation-translation": {
        "source": "Music notation, Euterpea syntax, and coding-agent artifacts translated into verifier-friendly forms.",
        "families": [
            "Pitch strings to strict JSON",
            "JSON back to compact notation",
            "Plain language to symbolic forms",
            "Euterpea expressions to compact outputs",
            "Patch or diff summaries to constrained labels",
        ],
    },
    "verifier-robustness-ambiguity": {
        "source": "Datacurve verifier QA: prompt-verifier bijection, acceptance breadth, false-positive traps, and false-negative traps.",
        "families": [
            "Near-miss rejection fixtures",
            "Punctuation and whitespace strictness boundaries",
            "Accepted-variant boundary checks",
            "False-positive and false-negative classification tasks",
            "Ambiguity review queue before scored promotion",
        ],
    },
}


TASK_INTAKE_GATES = [
    ("Original prompt", "The prompt is written for this benchmark, not copied from a public exercise or merged fix."),
    ("Hidden answer", "Expected answers live in metadata and verifier code, never in the model-facing instruction."),
    ("Prompt-verifier bijection", "The verifier tests exactly the requested behavior: no more, no less."),
    ("Acceptance breadth", "The verifier accepts all intended correct observable forms, not one private implementation shape."),
    ("Contamination review", "The task records exposure risk and avoids benchmark claims that outrun that risk."),
    ("Fixture promotion", "Repeated failures become negative fixtures or ambiguity review cases before public claims grow."),
]


TASK_SOURCE_REFERENCES = [
    ("DeepSWE", "https://deepswe.datacurve.ai/blog"),
    ("Datacurve Research", "https://datacurve.ai/research"),
    ("IFEval", "https://arxiv.org/abs/2311.07911"),
    ("HumanEval", "https://arxiv.org/abs/2107.03374"),
    ("BigCodeBench", "https://arxiv.org/html/2406.15877v3"),
    ("Open Music Theory", "https://viva.pressbooks.pub/openmusictheory/"),
    ("Euterpea", "https://www.euterpea.com/"),
]


PIE_COLORS = [
    "#4f46e5",
    "#148044",
    "#b42318",
    "#9a5b0a",
    "#7c3aed",
    "#0f766e",
    "#be185d",
    "#2563eb",
    "#a16207",
    "#475569",
]


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
pre { background: #181818; color: #f6efe4; border: 1px solid #303030; padding: 16px; overflow-x: auto; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .9rem; line-height: 1.5; }
pre code { background: transparent; border: 0; padding: 0; color: inherit; font-size: inherit; font-family: inherit; }
.eyebrow { color: var(--accent); font-size: .72rem; font-weight: 800; letter-spacing: .15em; text-transform: uppercase; }
.subtitle { max-width: 830px; color: #38332c; font-size: clamp(1.15rem, 2.2vw, 1.55rem); }
.muted { color: var(--muted); }
.small { font-size: .88rem; }
.section { margin-top: 50px; padding-top: 28px; border-top: 1px solid var(--line); }
.section:first-child, .hero + .section { border-top: 0; }
.section-head { display: grid; grid-template-columns: minmax(0, 1fr) minmax(280px, 470px); gap: 32px; align-items: end; margin-bottom: 18px; }
.center-section { max-width: 820px; margin-left: auto; margin-right: auto; text-align: center; }
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
.matrix-grid { display: grid; gap: 6px; width: max-content; min-width: 100%; }
.matrix-row { display: grid; grid-template-columns: 260px repeat(var(--cols), 180px); gap: 6px; align-items: stretch; }
.matrix-head, .matrix-task { color: var(--muted); font-size: .86rem; }
.matrix-section-title { grid-column: 1 / -1; background: #181818; color: #f6efe4; padding: 14px 16px; border: 1px solid #181818; }
.matrix-section-title strong { display: block; font-size: 1rem; color: #fffaf0; }
.matrix-task { position: sticky; left: 0; z-index: 2; background: var(--paper); border: 1px solid var(--line); padding: 8px 10px; }
.matrix-cell { display: grid; place-items: center; min-height: 34px; border: 1px solid var(--line); font-weight: 750; font-size: .82rem; }
.matrix-cell.pass { background: #dff0e5; color: #0f6a38; }
.matrix-cell.fail { background: #f7dedb; color: #9f1f17; }
.matrix-cell.partial { background: #f6e8c8; color: #81500a; }
.matrix-cell.empty { background: #ece6dc; color: var(--muted); }
.matrix-cell.summary { align-content: center; gap: 2px; }
.matrix-cell.summary span { display: block; font-weight: 500; font-size: .72rem; color: inherit; opacity: .82; }
.section-card-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.section-card { background: var(--paper); border: 1px solid var(--line); padding: 14px; }
.section-card strong { display: block; }
.section-card span { display: block; color: var(--muted); font-size: .88rem; }
.backlog-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.backlog-card { background: var(--paper); border: 1px solid var(--line); padding: 16px; }
.backlog-card h3 { margin-bottom: 8px; }
.backlog-card ul { margin: 10px 0 0; padding-left: 20px; }
.backlog-card li { margin: 3px 0; }
.evidence-list { display: grid; gap: 10px; }
.evidence-item { background: var(--paper); border: 1px solid var(--line); padding: 0; }
.evidence-item summary { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; gap: 12px; align-items: center; padding: 14px 16px; }
.section-icon { display: grid; place-items: center; min-width: 34px; height: 34px; border: 1px solid var(--line-strong); background: #eee8dc; font-weight: 800; }
.evidence-body { padding: 0 16px 16px; }
.gate-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border: 1px solid var(--line-strong); background: var(--paper); }
.gate-card { padding: 15px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.gate-card:nth-child(3n) { border-right: 0; }
.gate-card:nth-last-child(-n+3) { border-bottom: 0; }
.source-list { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.pie-wrap { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 22px; align-items: center; background: var(--paper); border: 1px solid var(--line); padding: 18px; }
.pie-chart { width: 240px; height: 240px; display: block; }
.pie-legend { display: grid; gap: 7px; }
.pie-legend-row { display: grid; grid-template-columns: 14px minmax(0, 1fr) auto; gap: 8px; align-items: center; font-size: .9rem; }
.pie-swatch { width: 12px; height: 12px; border: 1px solid var(--line-strong); }
.bar-list { display: grid; gap: 10px; }
.bar-row { display: grid; grid-template-columns: minmax(160px, 1fr) minmax(160px, 360px) 50px; gap: 12px; align-items: center; }
.thin-bar { height: 12px; background: #e6dfd3; border: 1px solid var(--line); }
.thin-bar span { display: block; width: var(--w); height: 100%; background: var(--pass); }
.thin-bar.fail span { background: var(--fail); }
.tag { display: inline-block; border: 1px solid var(--line); background: #f1eadf; padding: 1px 6px; margin: 1px 3px 1px 0; font-size: .78rem; white-space: nowrap; }
.schema-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }
.schema { background: #181818; color: #f6efe4; padding: 18px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .88rem; overflow-x: auto; }
.schema .comment { color: #a8a095; }
.reference-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 14px; }
.reference-list li { background: var(--paper); border: 1px solid var(--line); padding: 16px; }
.site-footer { background: #181818; color: #f6efe4; border-top: 0; padding-top: 34px; padding-bottom: 38px; }
.footer-inner { max-width: 1180px; margin: 0 auto; padding: 0 24px; display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 24px; align-items: start; }
.footer-links { display: flex; flex-wrap: wrap; gap: 14px; }
.site-footer a { color: #f6efe4; }
.site-footer .muted { color: #c8bdaa; }
.timeline { border-left: 2px solid var(--ink); margin-left: 12px; }
.timeline-step { position: relative; padding: 0 0 24px 28px; }
.timeline-step::before { content: ""; position: absolute; left: -7px; top: 3px; width: 12px; height: 12px; border-radius: 50%; background: var(--ink); }
.gate { color: var(--warn); font-weight: 750; font-size: .82rem; text-transform: uppercase; letter-spacing: .08em; }
details { border-top: 1px solid var(--line); padding: 10px 0; }
summary { cursor: pointer; font-weight: 700; }
@media (max-width: 860px) {
  .header-inner, .hero-top, .section-head, .split, .schema-grid, .footer-inner { display: block; }
  nav { gap: 10px; padding-bottom: 14px; }
  .stat-strip, .integrity, .pipeline, .backlog-grid, .gate-grid, .pie-wrap { grid-template-columns: 1fr; display: grid; }
  .stat, .integrity-step, .pipe-node, .gate-card { border-right: 0; border-bottom: 1px solid var(--line); }
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
      <a href="references.html">References</a>
      <a href="{GITHUB_URL}">GitHub</a>
    </nav>
    </div>
  </header>
  <main>
{body}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div>
        <strong>benchmark-euterpea</strong>
        <p class="muted small">A reproducible local benchmark slice: clone, run a model, preserve raw evidence, summarize results, and promote findings through reviewed issues.</p>
      </div>
      <div class="footer-links small">
        <a href="hiscores.html">Results</a>
        <a href="tasks.html">Tasks</a>
        <a href="workflow.html">Contribute Runs</a>
        <a href="references.html">References</a>
        <a href="{GITHUB_URL}">GitHub</a>
      </div>
    </div>
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


def section_for_task(task: dict[str, Any]) -> dict[str, str]:
    section_id = TASK_SECTION_OVERRIDES.get(str(task.get("id")))
    if not section_id:
        capability = str(task.get("capability", ""))
        if capability == "euterpea-stubs":
            section_id = "symbolic-music-euterpea"
        elif capability == "agent-compliance":
            section_id = "instruction-output-compliance"
        elif capability == "music-theory":
            section_id = "music-theory-recognition"
        else:
            section_id = "verifier-robustness-ambiguity"
    return SECTION_BY_ID[section_id]


def sectioned_tasks(tasks: list[dict[str, Any]], *, include_empty: bool = False) -> list[tuple[dict[str, str], list[dict[str, Any]]]]:
    by_section: dict[str, list[dict[str, Any]]] = {section["id"]: [] for section in BENCHMARK_SECTIONS}
    for task in tasks:
        by_section[section_for_task(task)["id"]].append(task)
    groups = []
    for section in BENCHMARK_SECTIONS:
        items = sorted(by_section[section["id"]], key=lambda item: (str(item.get("domain", "")), str(item.get("id", ""))))
        if items or include_empty:
            groups.append((section, items))
    return groups


def section_overview(tasks: list[dict[str, Any]]) -> str:
    cards = []
    counts = {section["id"]: len(items) for section, items in sectioned_tasks(tasks, include_empty=True)}
    for section in BENCHMARK_SECTIONS:
        count = counts.get(section["id"], 0)
        label = f"{count} current task{'s' if count != 1 else ''}" if count else "planned category"
        cards.append(
            '<div class="section-card">'
            f'<strong>{esc(section["title"])}</strong>'
            f'<span>{esc(label)} - {esc(section["summary"])}</span>'
            '</div>'
        )
    return '<div class="section-card-grid">' + "".join(cards) + "</div>"


def task_expansion_target(tasks: list[dict[str, Any]]) -> str:
    rows = []
    for section, items in sectioned_tasks(tasks, include_empty=True):
        current = len(items)
        needed = max(0, 10 - current)
        status = "ready for breadth work" if needed else "minimum met"
        rows.append(
            "<tr>"
            f"<td><strong>{esc(section['title'])}</strong></td>"
            f"<td>{esc(current)}</td>"
            f"<td>{esc(needed)}</td>"
            f"<td>{esc(status)}</td>"
            "</tr>"
        )
    return f"""
      <table>
        <thead><tr><th>Benchmark section</th><th>Current tasks</th><th>Needed for 10</th><th>Status</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    """


def coverage_table(tasks: list[dict[str, Any]]) -> str:
    rows = []
    for section, items in sectioned_tasks(tasks, include_empty=True):
        if items:
            domain_counts = Counter(str(task.get("domain", "unknown")) for task in items)
            domain_cell = "".join(
                f'<span class="tag">{esc(domain)} ({count})</span>'
                for domain, count in sorted(domain_counts.items())
            )
        else:
            domain_cell = '<span class="muted small">planned</span>'
        rows.append(
            "<tr>"
            f"<td><strong>{esc(section['title'])}</strong></td>"
            f"<td>{esc(len(items))}</td>"
            f"<td>{domain_cell}</td>"
            "</tr>"
        )
    return f"""
      <table>
        <thead><tr><th>Benchmark section</th><th>Tasks</th><th>Verifier domains</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
      <p class="muted small">Domain labels describe grading contracts. The same domain may appear in multiple sections when tasks share verifier families.</p>
    """


def pie_point(cx: float, cy: float, radius: float, fraction: float) -> tuple[float, float]:
    import math

    angle = 2 * math.pi * fraction - math.pi / 2
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def task_section_pie_chart(tasks: list[dict[str, Any]]) -> str:
    groups = sectioned_tasks(tasks, include_empty=True)
    total = max(sum(len(items) for _, items in groups), 1)
    start = 0.0
    slices = []
    legend = []
    cx = cy = radius = 50.0
    for index, (section, items) in enumerate(groups):
        count = len(items)
        if not count:
            continue
        end = start + count / total
        x1, y1 = pie_point(cx, cy, radius, start)
        x2, y2 = pie_point(cx, cy, radius, end)
        large_arc = 1 if end - start > 0.5 else 0
        color = PIE_COLORS[index % len(PIE_COLORS)]
        slices.append(
            f'<path d="M {cx:.3f} {cy:.3f} L {x1:.3f} {y1:.3f} '
            f'A {radius:.3f} {radius:.3f} 0 {large_arc} 1 {x2:.3f} {y2:.3f} Z" '
            f'fill="{esc(color)}"><title>{esc(section["title"])}: {esc(count)} tasks</title></path>'
        )
        legend.append(
            '<div class="pie-legend-row">'
            f'<span class="pie-swatch" style="background:{esc(color)}"></span>'
            f'<span>{esc(section["title"])}</span>'
            f'<strong>{esc(count)}</strong>'
            '</div>'
        )
        start = end
    return (
        '<div class="pie-wrap">'
        f'<svg class="pie-chart" viewBox="0 0 100 100" role="img" aria-label="Task coverage by benchmark section">{"".join(slices)}</svg>'
        f'<div class="pie-legend">{"".join(legend)}</div>'
        '</div>'
    )


def task_gate_grid() -> str:
    cards = []
    for title, text in TASK_INTAKE_GATES:
        cards.append(
            '<div class="gate-card">'
            f'<h3>{esc(title)}</h3>'
            f'<p class="muted small">{esc(text)}</p>'
            '</div>'
        )
    return '<div class="gate-grid">' + "".join(cards) + "</div>"


def source_reference_links() -> str:
    links = [
        f'<a class="tag" href="{esc(url)}">{esc(label)}</a>'
        for label, url in TASK_SOURCE_REFERENCES
    ]
    return '<div class="source-list">' + "".join(links) + "</div>"


def task_backlog_cards(tasks: list[dict[str, Any]]) -> str:
    counts = {section["id"]: len(items) for section, items in sectioned_tasks(tasks, include_empty=True)}
    cards = []
    for section in BENCHMARK_SECTIONS:
        backlog = TASK_BACKLOG[section["id"]]
        current = counts.get(section["id"], 0)
        needed = max(0, 10 - current)
        families = "".join(f"<li>{esc(item)}</li>" for item in backlog["families"])
        cards.append(
            '<article class="backlog-card">'
            f'<div class="eyebrow">{esc(current)} current / {esc(needed)} needed for 10</div>'
            f'<h3>{esc(section["title"])}</h3>'
            f'<p class="muted small">{esc(backlog["source"])}</p>'
            f'<ul>{families}</ul>'
            '</article>'
        )
    return '<div class="backlog-grid">' + "".join(cards) + "</div>"


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
    for section, items in sectioned_tasks(tasks):
        rows.append(
            '<div class="matrix-row" style="--cols:{0}">'.format(max(len(models), 1))
            + '<div class="matrix-section-title">'
            + f'<strong>{esc(section["title"])}</strong>'
            + f'<span>{esc(section["summary"])}</span>'
            + '</div></div>'
        )
        for task in items:
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


def section_result_summary(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    result_by_task = {str(result.get("task_id")): result for result in report.get("results", [])}
    cards = []
    for section, items in sectioned_tasks(tasks, include_empty=True):
        task_results = [result_by_task[str(task.get("id"))] for task in items if str(task.get("id")) in result_by_task]
        runs = sum(int(result.get("runs", 0)) for result in task_results)
        passed = sum(int(result.get("passed", 0)) for result in task_results)
        failed = sum(int(result.get("failed", 0)) for result in task_results)
        covered = len(task_results)
        pass_rate = passed / runs if runs else 0
        coverage = covered / len(items) if items else 0
        failure_counts: dict[str, int] = {}
        for result in task_results:
            for item in result.get("failure_distribution", []):
                klass = failure_class(item.get("failure_reason", ""))
                failure_counts[klass] = failure_counts.get(klass, 0) + int(item.get("count", 0))
        failure_note = (
            ", ".join(f"{label}: {count}" for label, count in sorted(failure_counts.items(), key=lambda item: (-item[1], item[0]))[:2])
            if failure_counts
            else "no failures recorded"
        )
        cards.append(
            '<details class="evidence-item">'
            '<summary>'
            f'<span class="section-icon">{esc(section.get("icon", ""))}</span>'
            f'<span><strong>{esc(section["title"])}</strong><br><span class="muted small">{esc(section["summary"])}</span></span>'
            f'<span class="muted small">{esc(covered)}/{esc(len(items))} tasks</span>'
            '</summary>'
            '<div class="evidence-body">'
            '<div class="backlog-card">'
            f'<div class="eyebrow">technical summary</div>'
            '<div class="bar-list">'
            f'<div class="bar-row"><span>pass rate</span>{percent_bar(pass_rate)}<strong>{esc(pct(pass_rate))}</strong></div>'
            f'<div class="bar-row"><span>report coverage</span>{percent_bar(coverage)}<strong>{esc(pct(coverage))}</strong></div>'
            '</div>'
            f'<p class="muted small">Runs: {esc(runs)}; passed: {esc(passed)}; failed: {esc(failed)}. Failure classes: {esc(failure_note)}.</p>'
            '</div>'
            '</div>'
            '</details>'
        )
    return '<div class="evidence-list">' + "".join(cards) + "</div>"


def report_provenance_summary(report: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    batches = sorted({batch for entry in model_summaries(report, tasks) for batch in entry["batches"]})
    option_sets = sum(len(entry["options"]) for entry in model_summaries(report, tasks))
    return f"""
      <div class="integrity">
        <div class="integrity-step"><h3>Generated report</h3><em>{esc(report.get("generated_at"))}</em></div>
        <div class="integrity-step"><h3>Raw source count</h3><em>{esc(report.get("source_run_count", 0))} run records summarized into this derived artifact.</em></div>
        <div class="integrity-step"><h3>Batch coverage</h3><em>{esc(len(batches))} batch id(s) represented; exact paths stay in <code>latest.json</code>.</em></div>
        <div class="integrity-step"><h3>Option samples</h3><em>{esc(option_sets)} model-option sample set(s) recorded for reproducibility.</em></div>
      </div>
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
          <li><strong>Recognition sections:</strong> relative keys, key signatures, scale degrees, tonal spelling, rhythm, and symbolic transformations.</li>
          <li><strong>Compliance sections:</strong> exact output, JSON-only output, and multi-step instruction following.</li>
          <li><strong>Euterpea path:</strong> symbolic pitch and duration contracts that can grow toward Haskell solver tasks.</li>
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
          <div class="eyebrow">Benchmark integrity</div>
          <h2>Four boundaries keep the report reproducible.</h2>
        </div>
        <p class="lede">The project separates what the model sees, what the verifier knows, what raw evidence records, and what public pages summarize.</p>
      </div>
      {integrity_block()}
    </section>

    <section class="section center-section">
      <div class="eyebrow">Coverage and scope</div>
      <h2>Section coverage is the roadmap, not a leaderboard claim.</h2>
      <p class="muted">The matrix is grouped by benchmark section so task rows act as evidence samples rather than standalone benchmark categories. The current suite is still intentionally compact; each approved section should grow to at least 10 deterministic tasks before the site makes stronger section-level claims.</p>
      <p><a href="tasks.html">Review task coverage</a> · <a href="hiscores.html">Open results snapshot</a> · <a href="references.html">View references</a></p>
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
      <p class="subtitle">A results-first view of every model benchmarked so far. Section summaries compare broader capabilities without turning raw answers or run paths into the public UI.</p>
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
          <div class="eyebrow">Current evidence</div>
          <h2>What the latest report supports.</h2>
        </div>
        <p class="lede">Model totals, section summaries, and failure classes are shown here. Raw observed answers, source paths, and full provenance stay in the derived JSON report for audit workflows.</p>
      </div>
      <p><a href="workflow.html">Run a model and submit reproducible findings</a>.</p>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Technical evidence</div>
          <h2>Evidence by benchmark.</h2>
        </div>
        <p class="lede">Each list item expands into a compact technical card with coverage, pass rate, and dominant failure classes. Raw evidence remains in <code>data/reports/latest.json</code>.</p>
      </div>
      {section_result_summary(report, tasks)}
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Sectioned score matrix</div>
          <h2>Capability sections with task evidence.</h2>
        </div>
        <p class="lede">The matrix scrolls horizontally as models are added and is sized to show about four model columns at a time. Section-level summaries live on the Tasks page; this view stays focused on task/model outcomes.</p>
      </div>
      {score_matrix(report, tasks)}
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <div class="eyebrow">Provenance</div>
          <h2>Audit summary, not raw-path dump.</h2>
        </div>
        <p class="lede">The page reports enough provenance to understand the derived artifact. Detailed source files, answer distributions, model options, and batch ids remain available in <code>data/reports/latest.json</code>.</p>
      </div>
      {report_provenance_summary(report, tasks)}
    </section>
""",
    )


def methodology_page() -> str:
    return page(
        "Methodology",
        f"""
    <section class="hero">
      <div class="eyebrow">Methodology</div>
      <h1>Methodology.</h1>
      <p class="subtitle">A formal description of task construction, verifier design, run collection, report derivation, and validity limits for a deterministic benchmark slice.</p>
    </section>

    <section class="section">
      <div class="section-head"><div><div class="eyebrow">3.1 Overview</div><h2>Evaluation unit and lifecycle.</h2></div><p class="lede">The unit of evaluation is a task contract: a model-facing instruction, hidden verifier metadata, deterministic grading code, and a raw run artifact. The same lifecycle can stay local or move into queue-backed execution because every transition has a concrete artifact.</p></div>
      {pipeline_diagram()}
    </section>

    <section class="section">
      <h2>3.2 Task Construction</h2>
      <p>Tasks are authored for this benchmark rather than copied from quiz banks, issue threads, or merged patches. Each task records capability, complexity, domain, expected behavior, expected failure modes, and contamination risk. Common music-theory concepts are allowed when wording and variants are original and the risk is documented.</p>
      <h2>3.3 Prompt/Verifier Boundary</h2>
      <p>The model sees only <code>instruction.md</code>. Expected answers live in <code>metadata.json</code> and <code>verifier.py</code>. Verifiers grade observable behavior, not intent, prose quality, or implementation style. Validation confirms each verifier imports correctly, returns the expected tuple contract, and accepts its metadata expected answer.</p>
      <h2>3.4 Datacurve-Aligned Review Standard</h2>
      <p>Task promotion follows four review criteria adapted from Datacurve/DeepSWE methodology: prompt-verifier bijection, acceptance breadth, task realism, and environment cleanliness. A verifier should test exactly the requested behavior, accept every intended correct observable form, reject partial or overbroad answers, and avoid grading noise from flaky infrastructure or hidden assumptions.</p>
      <h2>3.5 Run Collection and Provenance</h2>
      <p>Every raw run preserves the model-facing prompt, model name, options, raw answer, verifier decision, failure reason, latency, batch id, sample index, task path, and metadata snapshot. These fields make a score inspectable without requiring the public site to display raw answer tables or source-path dumps.</p>
      <h2>3.6 Derived Reports</h2>
      <p>Raw run JSON files are source data. <code>data/reports/latest.json</code> and the static site are derived artifacts generated from selected raw runs. Public pages summarize section-level evidence, failure classes, model totals, and provenance summaries; detailed answer distributions and file paths remain in the JSON report for audit workflows.</p>
      <h2>3.7 Failure Taxonomy</h2>
      <p>Verifier failures are grouped for readability into output contract violations, symbolic spelling errors, symbolic reasoning errors, and exact-answer mismatches. The taxonomy is a derived summary layer, not the source of truth; the underlying report preserves verifier reasons and answer distributions for reproducibility.</p>
      <h2>3.8 Threats to Validity</h2>
      <p>The current suite is intentionally small and local. It demonstrates a benchmark platform slice, not a comprehensive model ranking. The main validity risks are task breadth, public exposure of common music concepts, verifier false positives or false negatives, and incomplete model coverage after task expansion. Future work is repeated baselines, broader verifier fixtures, queue-backed workers, durable run storage, dashboards, and reviewer workflows.</p>
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
    tasks = load_tasks()
    groups = []
    for section, items in sectioned_tasks(tasks):
        rows = []
        for metadata in sorted(items, key=lambda item: (item.get("complexity", ""), item.get("id", ""))):
            failures = ", ".join(metadata.get("expected_failure_modes", []))
            rows.append(
                "<tr>"
                f"<td><strong>{esc(metadata.get('id'))}</strong><br><span class=\"muted small\"><code>{esc(metadata.get('_path'))}</code></span></td>"
                f"<td>{esc(section['title'])}</td>"
                f"<td>{esc(metadata.get('domain'))}</td>"
                f"<td>{esc(metadata.get('complexity'))}</td>"
                f"<td>{esc(metadata.get('contamination_risk'))}</td>"
                f"<td>{esc(failures)}</td>"
                "</tr>"
            )
        groups.append(
            f"""
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Benchmark section</div><h2>{esc(section['title'])}</h2></div><p class="lede">{esc(section['summary'])} {esc(len(items))} current task contract(s).</p></div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Task id</th><th>Section</th><th>Domain</th><th>Complexity</th><th>Contamination risk</th><th>Expected failure modes</th></tr></thead>
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
      <h1>Task roadmap and verifier contracts.</h1>
      <p class="subtitle">The catalog now shows both executable tasks and the researched backlog needed to turn this small benchmark slice into a broader evaluation platform. Current task rows are evidence; backlog families describe what should be authored next.</p>
    </section>
    <section class="section split">
      <div>
        <div class="eyebrow">Coverage</div>
        <h2>Section and domain coverage.</h2>
        {coverage_table(tasks)}
      </div>
      <div>
        <div class="eyebrow">Research inputs</div>
        <h2>Sources guide the backlog.</h2>
        <p class="muted">Task families inherit evaluation discipline from DeepSWE-style behavioral verification, IFEval-style output constraints, and music-domain references. The point is not to copy tasks; it is to inherit durable evaluation principles.</p>
        <p><a href="references.html">View full references and links</a></p>
      </div>
    </section>
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Coverage chart</div><h2>Task distribution by section.</h2></div><p class="lede">The pie chart shows where executable task coverage is currently concentrated. It should become more balanced as each section moves toward the minimum 10-task target.</p></div>
      {task_section_pie_chart(tasks)}
    </section>
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Meta-tasking gates</div><h2>Every task must earn promotion.</h2></div><p class="lede">Datacurve-style task quality depends on original prompts, prompt-verifier alignment, acceptance breadth, and clean grading. These gates apply before a proposal becomes benchmark data.</p></div>
      {task_gate_grid()}
    </section>
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Backlog map</div><h2>More than ten candidates per section where useful.</h2></div><p class="lede">The current goal is breadth with deterministic grading, weighted toward compliance, structured output, multi-step constraints, representation translation, and verifier robustness for coding-agent alignment.</p></div>
      {task_backlog_cards(tasks)}
    </section>
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Task expansion target</div><h2>Minimum 10 executable tasks per section.</h2></div><p class="lede">Backlog families can exceed the minimum, but public claims should stay modest until each section has enough deterministic verifier contracts and baseline runs.</p></div>
      {task_expansion_target(tasks)}
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
    <section class="section">
      <div class="section-head"><div><div class="eyebrow">Community runs</div><h2>Clone, run one model, open an issue.</h2></div><p class="lede">External users and agents can reproduce a model run locally without publishing raw traces. The issue should include enough command context for a maintainer or repo agent to recreate the result.</p></div>
      <pre><code>git clone {GITHUB_URL}.git
cd benchmark-euterpea
git rev-parse HEAD
ollama pull &lt;model&gt;
python3 scripts/run_batch.py --model &lt;model&gt; --repeat 10 --batch-id external-&lt;model&gt;-&lt;date&gt; --temperature 0.2 --num-predict 32
python3 scripts/summarize_runs.py --batch-id external-&lt;model&gt;-&lt;date&gt;
python3 scripts/build_site.py</code></pre>
      <p class="muted small">Open an <a href="{GITHUB_URL}/issues/new?template=model-failure.yml">Observed model failure</a> issue with commit SHA, model name, batch id, repeat count, generation options, Ollama version, pass-rate summary, and notable task failures. Paste the command block above unchanged for reproduction.</p>
    </section>
""",
    )


def references_page() -> str:
    references = [
        (
            "DeepSWE README",
            "https://github.com/datacurve-ai/deep-swe/blob/main/README.md",
            "Reference point for original tasks, isolated environments, programmatic verifiers, held-out solutions, and trajectory metadata.",
        ),
        (
            "Datacurve Research",
            "https://datacurve.ai/research",
            "Research framing for long-horizon software engineering benchmarks and verifier reliability.",
        ),
        (
            "Harbor task format",
            "https://www.harborframework.com/docs/tasks",
            "Task packaging reference for metadata, prompt, environment, verifier, and solution boundaries.",
        ),
        (
            "Pier",
            "https://github.com/datacurve-ai/pier",
            "Sandboxed agent evaluation runner referenced by DeepSWE for reproducible coding-agent evaluations.",
        ),
        (
            "Euterpea",
            "https://www.euterpea.com/",
            "Haskell-based computer music reference point for future symbolic music tasks.",
        ),
    ]
    items = "".join(
        "<li>"
        f'<strong><a href="{esc(url)}">{esc(title)}</a></strong>'
        f'<p class="muted">{esc(note)}</p>'
        "</li>"
        for title, url, note in references
    )
    return page(
        "References",
        f"""
    <section class="hero">
      <div class="eyebrow">References</div>
      <h1>Sources and methodological anchors.</h1>
      <p class="subtitle">The benchmark borrows evaluation discipline from coding-agent benchmarks while keeping this repo small, local, and deterministic.</p>
    </section>
    <section class="section">
      <ul class="reference-list">{items}</ul>
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
        "references.html": references_page(),
    }
    for filename, content in pages.items():
        (DIST_DIR / filename).write_text(content, encoding="utf-8")
    print(f"wrote {DIST_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
