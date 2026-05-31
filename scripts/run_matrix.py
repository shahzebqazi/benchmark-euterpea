#!/usr/bin/env python3
"""Run a benchmark task matrix across multiple Ollama models."""

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
    parser = argparse.ArgumentParser(description="Run discovered benchmark tasks across multiple Ollama models.")
    parser.add_argument(
        "--model",
        action="append",
        required=True,
        help="Ollama model name. Pass multiple times to run a matrix.",
    )
    parser.add_argument("--task-root", type=Path, default=DEFAULT_TASK_ROOT)
    parser.add_argument("--repeat", type=int, default=DEFAULT_REPEAT, help="Samples per task. Defaults to 10.")
    parser.add_argument("--batch-id", help="Batch id shared by all model batches.")
    parser.add_argument("--capability", help="Only run tasks under this capability directory.")
    parser.add_argument("--ollama-url", help="Ollama base URL to pass to run_batch.py.")
    parser.add_argument(
        "--ollama-api-key-env",
        default="OLLAMA_API_KEY",
        help="Environment variable containing an Ollama API key for authenticated hosts.",
    )
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--num-predict", type=int, default=32)
    parser.add_argument("--seed", type=int)
    return parser.parse_args()


def default_batch_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"matrix-{stamp}-{uuid.uuid4().hex[:8]}"


def build_batch_command(args: argparse.Namespace, model: str, batch_id: str) -> list[str]:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "run_batch.py"),
        "--model",
        model,
        "--task-root",
        str(args.task_root),
        "--repeat",
        str(args.repeat),
        "--batch-id",
        batch_id,
        "--temperature",
        str(args.temperature),
        "--num-predict",
        str(args.num_predict),
        "--ollama-api-key-env",
        args.ollama_api_key_env,
    ]
    if args.capability is not None:
        command.extend(["--capability", args.capability])
    if args.ollama_url is not None:
        command.extend(["--ollama-url", args.ollama_url])
    if args.seed is not None:
        command.extend(["--seed", str(args.seed)])
    return command


def main() -> int:
    args = parse_args()
    if args.repeat < 1:
        print("error: --repeat must be at least 1", file=sys.stderr)
        return 2

    batch_id = args.batch_id or default_batch_id()
    benchmark_failed_models: list[str] = []
    harness_error_models: list[str] = []

    for model in args.model:
        print(f"running model={model} batch_id={batch_id}", flush=True)
        completed = subprocess.run(
            build_batch_command(args, model, batch_id),
            cwd=REPO_ROOT,
            check=False,
        )
        if completed.returncode == 1:
            benchmark_failed_models.append(model)
        elif completed.returncode != 0:
            harness_error_models.append(model)

    print(f"batch_id={batch_id}")
    print(f"models={len(args.model)}")
    print(f"benchmark_failed_models={','.join(benchmark_failed_models)}")
    print(f"harness_error_models={','.join(harness_error_models)}")

    if harness_error_models:
        return 2
    return 1 if benchmark_failed_models else 0


if __name__ == "__main__":
    raise SystemExit(main())
