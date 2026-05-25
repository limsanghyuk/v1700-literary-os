from __future__ import annotations

from pathlib import Path
import shutil

from v1700.page03_release_seal import run_stage160_page03_release_seal
from v1700.gates.stage160_release_gate import run_stage160_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage160_report_passes() -> None:
    result = run_stage160_page03_release_seal(ROOT)
    assert result["status"] == "pass"
    assert result["page03_sealed"] is True
    assert result["page03_total_stage_count"] == 6
    assert result["page03_upstream_stage_count"] == 5
    assert len(result["page03_release_checksum"]) == 64
    assert result["stage161_rendering_contract_ready"] is True
    assert result["runtime_execution_count"] == 0
    assert result["write_operation_count"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage160_release_gate_passes() -> None:
    result = run_stage160_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["page03_sealed"] is True
    assert result["stage161_rendering_contract_ready"] is True
    assert result["provider_default_calls"] == 0
    assert result["runtime_execution_count"] == 0
    assert result["write_operation_count"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["boundary_violation_count"] == 0


def test_stage160_artifact_index_checks_existence() -> None:
    result = run_stage160_page03_release_seal(ROOT)
    index = result["parts"]["page03_artifact_index"]
    assert index["status"] == "pass"
    assert index["missing_count"] == 0
    assert all(asset["exists"] or asset.get("generated_by_stage160") for asset in index["assets"] if asset["required"])


def test_stage160_invariant_freeze_is_strict() -> None:
    result = run_stage160_page03_release_seal(ROOT)
    freeze = result["parts"]["page03_invariant_freeze"]
    assert freeze["status"] == "pass"
    frozen = {item["name"]: item["frozen_value"] for item in freeze["frozen"]}
    assert frozen["provider_default_calls"] == 0
    assert frozen["runtime_execution_count"] == 0
    assert frozen["write_operation_count"] == 0
    assert frozen["runtime_execution_enabled"] is False
    assert frozen["provider_execution_enabled"] is False
    assert frozen["memory_write_enabled"] is False
    assert frozen["runtime_training_enabled"] is False


def test_stage160_transition_criteria_points_to_stage161() -> None:
    result = run_stage160_page03_release_seal(ROOT)
    transition = result["parts"]["page03_transition_criteria"]
    assert transition["status"] == "pass"
    assert transition["next_stage"] == "stage161"
    assert transition["next_stage_title"] == "Rendering Contract"
    assert transition["next_page"] == "Page04 Rendering Body"


def test_stage160_blocks_missing_historical_artifact(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "*.pyc")
    shutil.copytree(ROOT, sandbox, ignore=ignore)
    missing = sandbox / "release/current/stage159_release_gate_report.json"
    missing.unlink()
    report = run_stage160_page03_release_seal(sandbox)
    assert report["status"] == "blocked"
    assert any("stage159_not_sealed" in issue or "missing:release/current/stage159_release_gate_report.json" in issue for issue in report["issues"])


def test_stage160_blocks_missing_stage159_invariant_evidence(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "*.pyc")
    shutil.copytree(ROOT, sandbox, ignore=ignore)

    import json
    report_path = sandbox / "release/current/stage159_execution_dry_run_trace_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report.pop("vector_db_runtime_dependency", None)
    gate_path = sandbox / "release/current/stage159_release_gate_report.json"
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    gate.pop("vector_db_runtime_dependency", None)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = run_stage160_page03_release_seal(sandbox)
    assert result["status"] == "blocked"
    assert any("stage159_invariant_missing:vector_db_runtime_dependency" in issue for issue in result["issues"])


def test_stage160_blocks_stage159_invariant_drift(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "*.pyc")
    shutil.copytree(ROOT, sandbox, ignore=ignore)

    import json
    report_path = sandbox / "release/current/stage159_execution_dry_run_trace_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["provider_execution_enabled"] = True
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = run_stage160_page03_release_seal(sandbox)
    assert result["status"] == "blocked"
    assert any("stage159_invariant_drift:provider_execution_enabled" in issue for issue in result["issues"])
