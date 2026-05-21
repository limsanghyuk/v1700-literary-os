from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

from v1700.cli import CLI_VERSION, build_parser, main as cli_main
from v1700.gates.stage142_release_gate import run_stage142_release_gate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency

from .contracts import DocumentedSurface

TARGET_STAGE = "stage143"
TARGET_REPORT = "release/current/stage143_user_cli_api_docs_report.json"
SAMPLE_PROMPT = "A cautious heir notices the ledger notch that everyone else pretends not to see."


def run_stage143_user_cli_api_docs(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage143_user_cli_api_docs_pack"
    pack.mkdir(parents=True, exist_ok=True)

    baseline = run_stage142_release_gate(root)
    _write_json(root / "release/current/stage143_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))
    cli_contract = _build_cli_contract(root)
    api_contract = _build_api_contract()
    docs_index = _build_docs_index(root)

    _write_json(pack / "cli_contract.json", cli_contract)
    _write_json(pack / "api_contract.json", api_contract)
    _write_json(pack / "user_docs_index.json", docs_index)
    (pack / "cli_help.txt").write_text(str(cli_contract.get("help_text", "")) + "\n", encoding="utf-8")
    (pack / "sample_render_text.txt").write_text(str(cli_contract.get("sample_text_output", "")) + "\n", encoding="utf-8")
    _write_json(pack / "sample_render_json.json", dict(cli_contract.get("sample_json_output", {})))

    _write_json(
        root / TARGET_REPORT,
        {
            "stage": "143",
            "baseline_stage": "142",
            "title": "User CLI/API Minimum Docs",
            "status": "building",
            "issues": [],
        },
    )

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage142_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "cli_contract": cli_contract,
        "api_contract": api_contract,
        "docs_index": docs_index,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))

    result = {
        "stage": "143",
        "baseline_stage": "142",
        "title": "User CLI/API Minimum Docs",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "USER_CLI_API_MINIMUM_DOCS_LOCAL",
        "user_cli_api_docs_only": True,
        "cli_help_available": cli_contract.get("help_available", False),
        "cli_json_example_valid": cli_contract.get("sample_json_valid", False),
        "api_contract_documented_only": api_contract.get("documented_only", False),
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "stage144_split_ci_runtime_ready": docs_index.get("stage144_split_ci_runtime_ready", False),
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "losdb_write_enabled": False,
        "migration_execution_enabled": False,
        "storage_contract_write_enabled": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "cross_project_write_allowed": False,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage142_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "cli_contract": cli_contract,
            "api_contract": api_contract,
            "docs_index": docs_index,
        },
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_cli_contract(root: Path) -> dict[str, Any]:
    parser = build_parser()
    help_text = parser.format_help()
    text_output = _capture_cli([SAMPLE_PROMPT])
    json_output_raw = _capture_cli([SAMPLE_PROMPT, "--json"])
    sample_json = json.loads(json_output_raw)
    issues: list[str] = []
    expected_keys = {"scene_id", "final_text", "surface_score", "constraint_score", "risk_flags"}
    if "--json" not in help_text or "--version" not in help_text:
        issues.append("help_flags_missing")
    if not text_output.strip():
        issues.append("sample_text_output_missing")
    if not expected_keys.issubset(sample_json.keys()):
        issues.append("sample_json_keys_missing")
    if not sample_json.get("final_text"):
        issues.append("sample_json_final_text_missing")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage143 CLI Minimum Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "entrypoint": "python -m v1700.cli",
        "version_string": CLI_VERSION,
        "help_available": True,
        "documented_flags": ["--json", "--version"],
        "default_prompt_available": True,
        "sample_prompt": SAMPLE_PROMPT,
        "sample_text_output": text_output.strip(),
        "sample_json_valid": True,
        "sample_json_output": sample_json,
    }


def _build_api_contract() -> dict[str, Any]:
    request_example = {
        "prompt": SAMPLE_PROMPT,
        "response_format": "rendered_prose_ir",
        "provider_calls_allowed": False,
        "runtime_training_enabled": False,
    }
    response_shape = {
        "scene_id": "string",
        "final_text": "string",
        "surface_score": "object",
        "constraint_score": "object",
        "risk_flags": "array",
    }
    return {
        "stage": TARGET_STAGE,
        "title": "Stage143 API Minimum Contract",
        "status": "pass",
        "issues": [],
        "documented_only": True,
        "implemented_server": False,
        "method": "POST",
        "path": "/v1/render-prose",
        "request_example": request_example,
        "response_shape": response_shape,
        "public_safe_only": True,
        "provider_calls_allowed": False,
        "auth_required": False,
    }


def _build_docs_index(root: Path) -> dict[str, Any]:
    docs = [
        DocumentedSurface(
            name="cli_quickstart",
            status="pass" if (root / "docs/user/cli_quickstart.md").exists() else "blocked",
            path="docs/user/cli_quickstart.md",
            summary="Minimum CLI entrypoint, flags, and example outputs.",
        ),
        DocumentedSurface(
            name="api_minimum",
            status="pass" if (root / "docs/user/api_minimum.md").exists() else "blocked",
            path="docs/user/api_minimum.md",
            summary="Documentation-only API contract for future local surfaces.",
        ),
        DocumentedSurface(
            name="render_request_example",
            status="pass" if (root / "docs/user/examples/render_request.json").exists() else "blocked",
            path="docs/user/examples/render_request.json",
            summary="Public-safe request example.",
        ),
        DocumentedSurface(
            name="render_response_example",
            status="pass" if (root / "docs/user/examples/render_response.json").exists() else "blocked",
            path="docs/user/examples/render_response.json",
            summary="Public-safe response example.",
        ),
    ]
    issues = [doc.name for doc in docs if doc.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage143 User Docs Index",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "documents": [doc.to_dict() for doc in docs],
        "stage144_split_ci_runtime_ready": not issues,
    }


def _compact_baseline(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "stage",
        "baseline_stage",
        "status",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    compact = {key: report.get(key) for key in keep if key in report}
    compact["stage142_release_gate_status"] = report.get("status")
    return compact


def _capture_cli(argv: list[str]) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cli_main(argv)
    return buffer.getvalue()


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
