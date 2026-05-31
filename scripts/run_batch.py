#!/usr/bin/env python3
"""Run a batch of benchmark tasks against one Ollama model."""

from __future__ import annotations

import argparse
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TASK_ROOT = REPO_ROOT / "tasks"
DEFAULT_REPEAT = 10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run every discovered benchmark task, or a filtered subset.")
    parser.add_argument("--model", required=True, help="Ollama model name, such as llama3.2:3b.")
    parser.add_argument("--task-root", type=Path, default=DEFAULT_TASK_ROOT)
    parser.add_argument("--repeat", type=int, default=DEFAULT_REPEAT, help="Samples per task. Defaults to 10 for accuracy estimates.")
    parser.add_argument("--batch-id", help="Batch id shared by all task runs.")
    parser.add_argument("--capability", help="Only run tasks under this capability directory.")
    parser.add_argument("--ollama-url", help="Ollama base URL to pass to run_task.py.")
    parser.add_argument(
        "--ollama-api-key-env",
        default="OLLAMA_API_KEY",
        help="Environment variable containing an Ollama API key for authenticated hosts.",
    )
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--num-predict", type=int, default=32)
    parser.add_argument("--seed", type=int)
    return parser.parse_args()


def discover_tasks(task_root: Path, capability: str | None) -> list[Path]:
    root = task_root / capability if capability else task_root
    tasks = sorted(path.parent for path in root.glob("**/metadata.json"))
    return [path for path in tasks if (path / "instruction.md").is_file() and (path / "verifier.py").is_file()]


def default_batch_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"batch-{stamp}-{uuid.uuid4().hex[:8]}"


def main() -> int:
    args = parse_args()
    tasks = discover_tasks(args.task_root.resolve(), args.capability)
    if not tasks:
        print("error: no tasks discovered", file=sys.stderr)
        return 2

    batch_id = args.batch_id or default_batch_id()
    benchmark_failures = 0
    harness_errors = 0
    for index, task_dir in enumerate(tasks):
        cmd = [
            sys.executable,
            str(REPO_ROOT / "scripts" / "run_task.py"),
            "--model", args.model,
            "--task-dir", str(task_dir),
            "--repeat", str(args.repeat),
            "--batch-id", batch_id,
            "--temperature", str(args.temperature),
            "--num-predict", str(args.num_predict),
            "--ollama-api-key-env", args.ollama_api_key_env,
        ]
        if args.ollama_url is not None:
            cmd.extend(["--ollama-url", args.ollama_url])
        if args.seed is not None:
            cmd.extend(["--seed", str(args.seed + index * args.repeat)])
        completed = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
        if completed.returncode == 1:
            benchmark_failures += 1
        elif completed.returncode != 0:
            harness_errors += 1

    print(f"batch_id={batch_id}")
    print(f"benchmark_failures={benchmark_failures}")
    print(f"harness_errors={harness_errors}")
    if harness_errors:
        return 2
    return 1 if benchmark_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
