#!/usr/bin/env python3
"""Run positive and negative verifier fixtures."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
TASK_ROOT = REPO_ROOT / "tasks"
DEFAULT_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "verifiers"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate verifier fixture cases.")
    parser.add_argument("--fixture-dir", type=Path, default=DEFAULT_FIXTURE_DIR)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def task_dirs_by_id() -> dict[str, Path]:
    dirs: dict[str, Path] = {}
    for metadata_path in sorted(TASK_ROOT.glob("**/metadata.json")):
        metadata = load_json(metadata_path)
        task_id = metadata.get("id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError(f"{metadata_path}: missing string id")
        dirs[task_id] = metadata_path.parent
    return dirs


def load_verifier(task_dir: Path) -> ModuleType:
    verifier_path = task_dir / "verifier.py"
    spec = importlib.util.spec_from_file_location(f"fixture_verifier_{abs(hash(verifier_path))}", verifier_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"could not import verifier {verifier_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "verify"):
        raise ValueError(f"{verifier_path} must define verify(answer)")
    return module


def validate_case(path: Path, index: int, case: dict[str, Any], verifier: ModuleType) -> None:
    if "answer" not in case or "passed" not in case:
        raise ValueError(f"{path}: case {index} must define answer and passed")
    if not isinstance(case["passed"], bool):
        raise ValueError(f"{path}: case {index} passed must be a boolean")

    outcome = verifier.verify(str(case["answer"]))
    if (
        not isinstance(outcome, tuple)
        or len(outcome) != 2
        or not isinstance(outcome[0], bool)
        or (outcome[1] is not None and not isinstance(outcome[1], str))
    ):
        raise ValueError(f"{path}: case {index} verifier returned invalid contract: {outcome!r}")

    passed, reason = outcome
    if passed != case["passed"]:
        raise ValueError(f"{path}: case {index} expected passed={case['passed']} but got {outcome!r}")

    expected_reason = case.get("reason_contains")
    if not passed and expected_reason:
        reason_text = reason or ""
        if str(expected_reason).casefold() not in reason_text.casefold():
            raise ValueError(
                f"{path}: case {index} failure reason {reason_text!r} "
                f"does not contain {expected_reason!r}"
            )


def validate_fixture(path: Path, task_dirs: dict[str, Path]) -> int:
    fixture = load_json(path)
    task_id = fixture.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        raise ValueError(f"{path}: missing string task_id")
    if task_id not in task_dirs:
        raise ValueError(f"{path}: unknown task_id {task_id!r}")
    cases = fixture.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{path}: cases must be a non-empty list")

    verifier = load_verifier(task_dirs[task_id])
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"{path}: case {index} must be an object")
        validate_case(path, index, case, verifier)
    return len(cases)


def validate_fixtures(fixture_dir: Path = DEFAULT_FIXTURE_DIR) -> int:
    if not fixture_dir.is_dir():
        raise ValueError(f"missing verifier fixture directory: {fixture_dir}")
    fixture_paths = sorted(fixture_dir.glob("*.json"))
    if not fixture_paths:
        raise ValueError(f"no verifier fixtures found in {fixture_dir}")

    task_dirs = task_dirs_by_id()
    case_count = 0
    for path in fixture_paths:
        case_count += validate_fixture(path, task_dirs)
    return case_count


def main() -> int:
    args = parse_args()
    case_count = validate_fixtures(args.fixture_dir.resolve())
    print(f"validated {case_count} verifier fixture cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
