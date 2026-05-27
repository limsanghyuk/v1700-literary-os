from __future__ import annotations

import json
import shutil
from pathlib import Path

from v1700.governance_contract import run_stage173_governance_contract
from v1700.gates.stage173_release_gate import run_stage173_release_gate


def test_stage173_governance_contract_passes() -> None:
    result = run_stage173_governance_contract(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["governance_contract_only"] is True
    assert result["stage172_page05_seal_inherited"] is True
    assert result["default_authority_decision"] == "DENY"
    assert result["deny_by_default"] is True
    assert result["stage174_release_policy_registry_ready"] is True
    assert result["provider_default_calls"] == 0
    assert result["governance_write_enabled"] is False
    assert result["node2_raw_reveal_access"] == 0


def test_stage173_release_gate_preserves_governance_boundaries() -> None:
    result = run_stage173_release_gate(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["default_authority_decision"] == "DENY"
    assert result["automatic_promotion_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["write_operation_count"] == 0
    assert result["runtime_training_enabled"] is False
    assert result["canon_mutation_enabled"] is False


def test_stage173_policy_precedence_is_deterministic() -> None:
    result = run_stage173_governance_contract(Path(__file__).resolve().parents[1])
    matrix = result["parts"]["policy_precedence_matrix"]
    policies = matrix["policies"]
    assert policies == sorted(policies, key=lambda item: (item["precedence"], item["policy_id"]))
    assert matrix["deny_overrides_allow"] is True
    assert matrix["unknown_request_decision"] == "DENY"


def test_stage173_requires_preflight_and_package_comparison(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    sandbox = tmp_path / "repo"
    _copy_minimal_repo(root, sandbox)
    target = sandbox / "release/current/stage173_preflight_execution_report.json"
    data = json.loads(target.read_text(encoding="utf-8"))
    data["status"] = "blocked"
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = run_stage173_release_gate(sandbox)
    assert result["status"] == "blocked"
    assert "preflight_execution_report_pass" in result["issues"]


def test_stage173_active_version_mismatch_blocks(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    sandbox = tmp_path / "repo"
    _copy_minimal_repo(root, sandbox)
    manifest_path = sandbox / "manifests/live_core_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["active_version"] = "stage172"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = run_stage173_governance_contract(sandbox)
    assert result["status"] == "blocked"
    assert any(issue.startswith("active_version_mismatch") for issue in result["issues"])


def _copy_minimal_repo(src: Path, dst: Path) -> None:
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".git")
    for name in ["src", "tools", "tests", "docs", "manifests", "release", "samples", "benchmarks"]:
        source = src / name
        if source.exists():
            shutil.copytree(source, dst / name, ignore=ignore)
    for name in ["README.md", "RELEASE_NOTES.md", "package_manifest.json", "pyproject.toml"]:
        source = src / name
        if source.exists():
            (dst / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def test_stage173_requires_gitnexus_7x12_preflight_analysis(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    sandbox = tmp_path / "repo"
    _copy_minimal_repo(root, sandbox)
    target = sandbox / "release/current/stage173_gitnexus_preflight_analysis_report.json"
    data = json.loads(target.read_text(encoding="utf-8"))
    data["seven_key_perspectives_count"] = 6
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = run_stage173_release_gate(sandbox)
    assert result["status"] == "blocked"
    assert "gitnexus_preflight_analysis_pass" in result["issues"]
