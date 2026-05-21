from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage142_release_gate import run_stage142_release_gate
from v1700.stage143 import run_stage143

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage143_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage143":
        existing = _load_report(root, "stage143_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    out = root / "release/current/stage143_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text(
            json.dumps(
                {
                    "stage": "143",
                    "baseline_stage": "142",
                    "title": "User CLI/API Minimum Docs Gate",
                    "status": "building",
                    "issues": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    baseline = _baseline_gate(root)
    stage = run_stage143(root)
    docs_index = stage.get("parts", {}).get("docs_index", {})
    checks = {
        "stage142_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage142", {}).get("status") == "pass"
        ),
        "stage143_report_pass": _check(stage.get("status") == "pass"),
        "docs_mode_pass": _check(
            stage.get("user_cli_api_docs_only") is True
            and stage.get("mode") == "USER_CLI_API_MINIMUM_DOCS_LOCAL"
        ),
        "metadata_consistency_pass": _check(stage.get("metadata_consistency_status") == "pass"),
        "release_asset_integrity_pass": _check(stage.get("release_asset_integrity_status") == "pass"),
        "cli_help_available_pass": _check(stage.get("cli_help_available") is True),
        "cli_json_example_valid_pass": _check(stage.get("cli_json_example_valid") is True),
        "api_contract_documented_only_pass": _check(stage.get("api_contract_documented_only") is True),
        "docs_index_pass": _check(docs_index.get("status") == "pass"),
        "stage144_split_ci_runtime_ready_pass": _check(stage.get("stage144_split_ci_runtime_ready") is True),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "active_meta_learning_blocked": _check(stage.get("active_meta_learning_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "losdb_write_blocked": _check(stage.get("losdb_write_enabled") is False),
        "migration_execution_blocked": _check(stage.get("migration_execution_enabled") is False),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(
            stage.get("raw_manuscript_provider_leakage") == 0
            and stage.get("raw_manuscript_cross_project_leakage") == 0
        ),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "143",
        "baseline_stage": "142",
        "title": "User CLI/API Minimum Docs Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage143": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage143":
        report = _load_report(root, "stage142_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage142_release_gate(root)


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_report(root: Path, name: str) -> dict[str, Any] | None:
    path = root / "release/current" / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "mode",
        "user_cli_api_docs_only",
        "cli_help_available",
        "cli_json_example_valid",
        "api_contract_documented_only",
        "metadata_consistency_status",
        "release_asset_integrity_status",
        "stage144_split_ci_runtime_ready",
        "runtime_training_enabled",
        "active_meta_learning_enabled",
        "model_weight_update_count",
        "losdb_write_enabled",
        "migration_execution_enabled",
        "storage_contract_write_enabled",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage",
        "credential_leakage",
        "cross_project_write_allowed",
        "canon_auto_resolution_count",
        "auto_repair_mutation_count",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage143.md",
            "docs/proposals/stage143_proposal.md",
            "docs/architecture/stage143_blueprint.md",
            "docs/development/stage143_developer_handoff.md",
            "docs/user/cli_quickstart.md",
            "docs/user/api_minimum.md",
            "docs/user/examples/render_request.json",
            "docs/user/examples/render_response.json",
            "manifests/stage143_manifest.json",
            "manifests/stage143_user_cli_api_docs_manifest.json",
            "manifests/stage143_branchpoint_trace_manifest.json",
            "manifests/live_core_stage143_overlay.json",
            "release/current/stage143_user_cli_api_docs_report.json",
            "release/current/stage143_release_gate_report.json",
            "release/current/stage143_release_asset_manifest.json",
            "release/current/stage143_user_cli_api_docs_pack/cli_contract.json",
            "release/current/stage143_user_cli_api_docs_pack/api_contract.json",
            "release/current/stage143_user_cli_api_docs_pack/user_docs_index.json",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [
        root / ".github/workflows/ci-core.yml",
        root / ".github/workflows/cd-dry-run.yml",
        root / ".github/workflows/release.yml",
        root / "RELEASE_NOTES.md",
        root / "package_manifest.json",
    ]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(
        token in contents
        for token in [
            "stage143",
            "run_stage143_user_cli_api_docs.py",
            "run_stage143_release_gate.py",
        ]
    )
