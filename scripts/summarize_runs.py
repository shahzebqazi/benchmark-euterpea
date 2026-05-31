#!/usr/bin/env python3
"""Create public benchmark summaries from raw run JSON files."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS_DIR = REPO_ROOT / "data" / "runs"
DEFAULT_REPORTS_DIR = REPO_ROOT / "data" / "reports"
SUMMARY_SCHEMA_VERSION = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize benchmark run JSON files.")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    parser.add_argument(
        "--batch-id",
        action="append",
        help="Only include runs from this batch id. May be passed more than once.",
    )
    return parser.parse_args()


def read_runs(runs_dir: Path, batch_ids: set[str] | None) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for path in sorted(runs_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if batch_ids and data.get("batch_id") not in batch_ids:
            continue
        if "schema_version" not in data:
            continue
        data["_source_file"] = str(path.relative_to(REPO_ROOT))
        runs.append(data)
    return runs


def answer_distribution(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(str(run.get("raw_answer", "")) for run in runs)
    return [{"answer": answer, "count": count} for answer, count in counts.most_common()]


def failure_distribution(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(str(run.get("failure_reason")) for run in runs if not run.get("passed"))
    return [{"failure_reason": reason, "count": count} for reason, count in counts.most_common()]


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        groups[(str(run.get("task_id")), str(run.get("model")))].append(run)

    rows = []
    for (task_id, model), group in sorted(groups.items()):
        pass_count = sum(1 for run in group if run.get("passed"))
        latencies = [run["latency_ms"] for run in group if isinstance(run.get("latency_ms"), (int, float))]
        task_metadata = next((run.get("task_metadata") for run in group if run.get("task_metadata")), {})
        rows.append(
            {
                "task_id": task_id,
                "model": model,
                "task_metadata": task_metadata,
                "runs": len(group),
                "passed": pass_count,
                "failed": len(group) - pass_count,
                "pass_rate": round(pass_count / len(group), 4) if group else 0,
                "answer_distribution": answer_distribution(group),
                "failure_distribution": failure_distribution(group),
                "latency_ms_avg": round(sum(latencies) / len(latencies), 3) if latencies else None,
                "batch_ids": sorted({str(run.get("batch_id")) for run in group}),
                "source_files": sorted(str(run.get("_source_file")) for run in group if run.get("_source_file")),
                "model_options": sorted(
                    {
                        json.dumps(run.get("ollama_options", {}), sort_keys=True)
                        for run in group
                    }
                ),
            }
        )

    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source_run_count": len(runs),
        "results": rows,
    }


def main() -> int:
    args = parse_args()
    batch_ids = set(args.batch_id) if args.batch_id else None
    runs = read_runs(args.runs_dir.resolve(), batch_ids)
    report = summarize(runs)

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    latest_path = args.reports_dir / "latest.json"
    latest_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {latest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
