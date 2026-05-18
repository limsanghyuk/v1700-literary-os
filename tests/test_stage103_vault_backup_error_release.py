from pathlib import Path

from v1700.stage103.backup_restore import run_backup_restore_probe
from v1700.stage103.error_reporting import build_safe_error_report
from v1700.stage103.manuscript_vault import run_local_manuscript_vault_probe
from v1700.stage103.orchestrator import run_stage103_3_vault_backup_error_release
from v1700.stage103.release_notes import build_stage103_release_notes


def test_stage103_local_vault_is_feature_only():
    result = run_local_manuscript_vault_probe("private scene text that must stay local")
    assert result["status"] == "pass"
    assert result["vault_mode"] == "LOCAL_ONLY"
    assert result["raw_text_exported"] is False
    assert result["provider_export_allowed"] is False


def test_stage103_backup_restore_checksum_matches():
    result = run_backup_restore_probe()
    assert result["status"] == "pass"
    assert result["source_checksum"] == result["restored_checksum"]
    assert result["metadata_only"] is True


def test_stage103_error_report_and_release_notes_are_safe():
    error_report = build_safe_error_report()
    notes = build_stage103_release_notes()
    assert error_report["raw_prompt_included"] is False
    assert error_report["credential_included"] is False
    assert notes["status"] == "pass"
    assert "python tools/run_stage103_release_gate.py" in notes["verification_commands"]


def test_stage103_vault_backup_error_release_writes_pack():
    root = Path(__file__).resolve().parents[1]
    result = run_stage103_3_vault_backup_error_release(root)
    assert result["status"] == "pass"
    assert (root / "release/current/stage103_deployment_pack/local_manuscript_vault_report.json").exists()
