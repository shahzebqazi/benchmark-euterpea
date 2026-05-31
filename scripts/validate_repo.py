#!/usr/bin/env python3
"""Validate task contracts, verifier contracts, reports, and prompt leakage."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from validate_verifier_fixtures import validate_fixtures

REPO_ROOT = Path(__file__).resolve().parents[1]
TASK_ROOT = REPO_ROOT / "tasks"
SITE_DIST = REPO_ROOT / "docs" / "site" / "dist"
REPORT_SCHEMA_VERSION = 1
REQUIRED_METADATA_FIELDS = {
    "id",
    "capability",
    "complexity",
    "domain",
    "expected_answer",
    "expected_behavior",
    "expected_failure_modes",
    "contamination_risk",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate benchmark repository contracts.")
    parser.add_argument("--skip-report", action="store_true", help="Do not require data/reports/latest.json.")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def load_verifier(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"verifier_{abs(hash(path))}", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"could not import verifier {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "verify"):
        raise ValueError(f"{path} must define verify(answer)")
    return module


def assert_verify_contract(task_dir: Path, expected_answer: str) -> None:
    module = load_verifier(task_dir / "verifier.py")
    outcome = module.verify(expected_answer)
    if not (
        isinstance(outcome, tuple)
        and len(outcome) == 2
        and isinstance(outcome[0], bool)
        and (outcome[1] is None or isinstance(outcome[1], str))
    ):
        raise ValueError(f"{task_dir}: verify(answer) must return tuple[bool, str | None]")
    if outcome != (True, None):
        raise ValueError(f"{task_dir}: verifier rejects metadata expected_answer {expected_answer!r}: {outcome}")


def validate_prompt_no_leak(task_dir: Path, metadata: dict[str, Any]) -> None:
    instruction = (task_dir / "instruction.md").read_text(encoding="utf-8")
    expected = str(metadata.get("expected_answer", "")).strip()
    if not expected:
        raise ValueError(f"{task_dir}: expected_answer must be non-empty")

    normalized_instruction = instruction.casefold()
    normalized_expected = expected.casefold()

    # Exact-copy compliance tasks intentionally place the token in the prompt.
    domain = str(metadata.get("domain", ""))
    if domain in {"output-constraint", "structured-output"}:
        return

    if len(normalized_expected) >= 3 and normalized_expected in normalized_instruction:
        raise ValueError(
            f"{task_dir}: instruction appears to contain expected_answer {expected!r}; "
            "move answers into metadata/verifier or mark as an explicit copy task"
        )


def validate_tasks() -> list[dict[str, Any]]:
    metadata_paths = sorted(TASK_ROOT.glob("**/metadata.json"))
    if not metadata_paths:
        raise ValueError("no tasks found")

    tasks = []
    seen_ids: set[str] = set()
    for metadata_path in metadata_paths:
        task_dir = metadata_path.parent
        for filename in ("instruction.md", "verifier.py"):
            if not (task_dir / filename).is_file():
                raise ValueError(f"{task_dir}: missing {filename}")

        metadata = load_json(metadata_path)
        missing = sorted(REQUIRED_METADATA_FIELDS - set(metadata))
        if missing:
            raise ValueError(f"{metadata_path}: missing metadata fields: {', '.join(missing)}")
        if metadata["id"] in seen_ids:
            raise ValueError(f"duplicate task id: {metadata['id']}")
        seen_ids.add(str(metadata["id"]))

        if not isinstance(metadata.get("expected_failure_modes"), list) or not metadata["expected_failure_modes"]:
            raise ValueError(f"{metadata_path}: expected_failure_modes must be a non-empty list")

        validate_prompt_no_leak(task_dir, metadata)
        assert_verify_contract(task_dir, str(metadata["expected_answer"]))
        tasks.append(metadata)
    return tasks


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def validate_report(tasks: list[dict[str, Any]]) -> None:
    report_path = REPO_ROOT / "data" / "reports" / "latest.json"
    if not report_path.is_file():
        raise ValueError("missing data/reports/latest.json; run scripts/summarize_runs.py")
    report = load_json(report_path)
    for key in ("schema_version", "generated_at", "source_run_count", "results"):
        if key not in report:
            raise ValueError(f"{report_path}: missing {key}")
    if report["schema_version"] != REPORT_SCHEMA_VERSION:
        raise ValueError(
            f"{report_path}: schema_version must be {REPORT_SCHEMA_VERSION}, got {report['schema_version']!r}"
        )
    if not isinstance(report["source_run_count"], int) or report["source_run_count"] < 0:
        raise ValueError(f"{report_path}: source_run_count must be a non-negative integer")
    if not isinstance(report["results"], list):
        raise ValueError(f"{report_path}: results must be a list")
    for result in report["results"]:
        for key in (
            "task_id",
            "model",
            "task_metadata",
            "runs",
            "passed",
            "failed",
            "pass_rate",
            "answer_distribution",
            "failure_distribution",
            "latency_ms_avg",
            "batch_ids",
            "source_files",
            "model_options",
        ):
            if key not in result:
                raise ValueError(f"{report_path}: result missing {key}")
        if not isinstance(result["runs"], int) or result["runs"] < 1:
            raise ValueError(f"{report_path}: result runs must be a positive integer")
        if result["passed"] + result["failed"] != result["runs"]:
            raise ValueError(f"{report_path}: passed + failed must equal runs for {result.get('task_id')}")
        if not 0 <= float(result["pass_rate"]) <= 1:
            raise ValueError(f"{report_path}: pass_rate must be between 0 and 1")
        for list_key in ("answer_distribution", "failure_distribution", "batch_ids", "source_files", "model_options"):
            if not isinstance(result[list_key], list):
                raise ValueError(f"{report_path}: {list_key} must be a list")

    task_ids = {str(task["id"]) for task in tasks}
    models = sorted({str(result.get("model")) for result in report["results"]})
    coverage_by_model: dict[str, set[str]] = {model: set() for model in models}
    for result in report["results"]:
        coverage_by_model[str(result.get("model"))].add(str(result.get("task_id")))
    if len(models) < 4:
        warn(f"latest report contains {len(models)} model(s); target public baseline is four")
    incomplete = {
        model: len(task_ids - covered)
        for model, covered in coverage_by_model.items()
        if task_ids - covered
    }
    if incomplete:
        details = ", ".join(f"{model}: {missing} missing task(s)" for model, missing in sorted(incomplete.items()))
        warn(f"latest report is not full-suite for every model ({details})")
    if not SITE_DIST.is_dir():
        warn("docs/site/dist is not present yet; run scripts/build_site.py before local preview or Pages artifact upload")


def main() -> int:
    args = parse_args()
    try:
        tasks = validate_tasks()
        fixture_count = validate_fixtures()
        if not args.skip_report:
            validate_report(tasks)
    except Exception as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"validated {len(tasks)} tasks and {fixture_count} verifier fixture cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
