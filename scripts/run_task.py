#!/usr/bin/env python3
"""Run one benchmark task against an Ollama model."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TASK_DIR = REPO_ROOT / "tasks" / "music-theory" / "basic" / "c-major-fifth"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
SCHEMA_VERSION = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a benchmark task against an Ollama model and save JSON results."
    )
    parser.add_argument("--model", required=True, help="Ollama model name, such as llama3.2:1b.")
    parser.add_argument(
        "--task-dir",
        type=Path,
        default=DEFAULT_TASK_DIR,
        help="Task directory containing instruction.md and verifier.py.",
    )
    parser.add_argument(
        "--ollama-url",
        default=os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL),
        help="Ollama base URL. Defaults to OLLAMA_URL or http://localhost:11434.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON path. Only valid when --repeat is 1.",
    )
    parser.add_argument("--repeat", type=int, default=1, help="Number of samples to run.")
    parser.add_argument("--batch-id", help="Batch id to record and use in output filenames.")
    parser.add_argument("--seed", type=int, help="Base Ollama seed. Each repeat increments it by one.")
    parser.add_argument("--temperature", type=float, default=0.2, help="Ollama temperature.")
    parser.add_argument("--top-p", type=float, help="Ollama top_p option.")
    parser.add_argument(
        "--num-predict",
        type=int,
        default=32,
        help="Maximum tokens to predict.",
    )
    return parser.parse_args()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_run_at(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "value"


def validate_task_dir(task_dir: Path) -> None:
    required = ["instruction.md", "verifier.py", "metadata.json"]
    missing = [name for name in required if not (task_dir / name).is_file()]
    if missing:
        raise RuntimeError(f"task directory {task_dir} missing: {', '.join(missing)}")


def load_metadata(task_dir: Path) -> dict[str, Any]:
    metadata_path = task_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise RuntimeError(f"{metadata_path} must contain a JSON object")
    for key in ("id", "capability", "complexity"):
        if not isinstance(metadata.get(key), str) or not metadata[key]:
            raise RuntimeError(f"{metadata_path} must define non-empty string field {key!r}")
    return metadata


def load_verifier(task_dir: Path) -> ModuleType:
    verifier_path = task_dir / "verifier.py"
    module_hash = hashlib.sha256(str(verifier_path).encode("utf-8")).hexdigest()[:12]
    spec = importlib.util.spec_from_file_location(f"task_verifier_{module_hash}", verifier_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load verifier from {verifier_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "verify"):
        raise RuntimeError(f"{verifier_path} must define verify(answer)")
    return module


def call_ollama(base_url: str, model: str, prompt: str, options: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps(
        {"model": model, "prompt": prompt, "stream": False, "options": options}
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc

    if not isinstance(body, dict) or "response" not in body:
        raise RuntimeError(f"Ollama response missing 'response': {body}")
    return body


def default_output_path(task_id: str, model: str, batch_id: str, sample_index: int) -> Path:
    safe_model = safe_name(model)
    safe_task = safe_name(task_id)
    safe_batch = safe_name(batch_id)
    return REPO_ROOT / "data" / "runs" / f"{safe_batch}_{safe_task}_{safe_model}_{sample_index:03d}.json"


def write_result(output_path: Path, result: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    except FileExistsError as exc:
        raise RuntimeError(f"refusing to overwrite existing result: {output_path}") from exc


def verify_answer(verifier: ModuleType, raw_answer: str) -> tuple[bool, str | None]:
    outcome = verifier.verify(raw_answer)
    if (
        not isinstance(outcome, tuple)
        or len(outcome) != 2
        or not isinstance(outcome[0], bool)
        or (outcome[1] is not None and not isinstance(outcome[1], str))
    ):
        raise RuntimeError("verifier.verify(answer) must return tuple[bool, str | None]")
    return outcome


def main() -> int:
    args = parse_args()
    if args.repeat < 1:
        raise RuntimeError("--repeat must be at least 1")
    if args.output is not None and args.repeat != 1:
        raise RuntimeError("--output can only be used when --repeat is 1")

    task_dir = args.task_dir.resolve()
    validate_task_dir(task_dir)
    instruction_path = task_dir / "instruction.md"

    metadata = load_metadata(task_dir)
    prompt = instruction_path.read_text(encoding="utf-8").strip()
    verifier = load_verifier(task_dir)
    batch_id = args.batch_id or f"batch-{utc_now().strftime('%Y%m%dT%H%M%S.%fZ')}-{uuid.uuid4().hex[:8]}"
    any_failed = False

    for sample_index in range(1, args.repeat + 1):
        options: dict[str, Any] = {
            "temperature": args.temperature,
            "num_predict": args.num_predict,
        }
        if args.top_p is not None:
            options["top_p"] = args.top_p
        if args.seed is not None:
            options["seed"] = args.seed + sample_index - 1

        run_started = utc_now()
        started_perf = time.perf_counter()
        response_body = call_ollama(args.ollama_url, args.model, prompt, options)
        latency_ms = round((time.perf_counter() - started_perf) * 1000, 3)

        raw_answer = str(response_body["response"])
        passed, failure_reason = verify_answer(verifier, raw_answer)
        any_failed = any_failed or not passed

        result = {
            "schema_version": SCHEMA_VERSION,
            "run_at": format_run_at(run_started),
            "batch_id": batch_id,
            "sample_index": sample_index,
            "task_id": metadata["id"],
            "task_path": str(task_dir.relative_to(REPO_ROOT)),
            "task_metadata": metadata,
            "model": args.model,
            "harness": "ollama-generate",
            "ollama_url": args.ollama_url,
            "ollama_options": options,
            "prompt": prompt,
            "raw_answer": raw_answer,
            "passed": passed,
            "failure_reason": failure_reason,
            "latency_ms": latency_ms,
            "ollama_metrics": {
                key: response_body[key]
                for key in (
                    "total_duration",
                    "load_duration",
                    "prompt_eval_count",
                    "prompt_eval_duration",
                    "eval_count",
                    "eval_duration",
                )
                if key in response_body
            },
        }
        output_path = args.output or default_output_path(metadata["id"], args.model, batch_id, sample_index)
        write_result(output_path.resolve(), result)
        print(f"wrote {output_path}")

    return 1 if any_failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
