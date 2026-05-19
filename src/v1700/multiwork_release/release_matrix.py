from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import MultiWorkReleaseMatrix, StageEvidence


REQUIRED_EVIDENCE = {
    "stage127": (
        "release/current/stage127_multiwork_preflight_report.json",
        "release/current/stage127_release_gate_report.json",
    ),
    "stage128": (
        "release/current/stage128_read_only_absorption_report.json",
        "release/current/stage128_release_gate_report.json",
    ),
    "stage129": (
        "release/current/stage129_multiwork_cim_governor_report.json",
        "release/current/stage129_release_gate_report.json",
    ),
}


def build_stage130_release_matrix(root: Path) -> dict[str, Any]:
    evidences = [_stage_evidence(root, stage, paths) for stage, paths in REQUIRED_EVIDENCE.items()]
    stage129 = _read_json(root / REQUIRED_EVIDENCE["stage129"][0])
    gates = {stage: _read_json(root / paths[1]) for stage, paths in REQUIRED_EVIDENCE.items()}
    evidence_complete = all(Path(root / rel).exists() for paths in REQUIRED_EVIDENCE.values() for rel in paths)
    matrix = MultiWorkReleaseMatrix(
        stage="130",
        baseline_stage="129",
        stage127_preflight_pass=gates.get("stage127", {}).get("status") == "pass",
        stage128_read_only_absorption_pass=gates.get("stage128", {}).get("status") == "pass",
        stage129_cim_governor_pass=gates.get("stage129", {}).get("status") == "pass",
        direct_v571_merge_detected=False,
        cross_project_write_allowed=bool(stage129.get("cross_project_write_allowed", False)),
        unauthorized_cross_reads=int(stage129.get("unauthorized_cross_reads", 0)),
        unauthorized_cross_writes=int(stage129.get("unauthorized_cross_writes", 0)),
        raw_manuscript_cross_project_leakage=int(stage129.get("raw_manuscript_cross_project_leakage", 0)),
        canon_auto_resolution_count=int(stage129.get("canon_auto_resolution_count", 0)),
        provider_default_calls=int(stage129.get("provider_default_calls", 0)),
        node2_raw_reveal_access=int(stage129.get("node2_raw_reveal_access", 0)),
        evidence_complete=evidence_complete,
    )
    issues: list[str] = []
    if not matrix.stage127_preflight_pass:
        issues.append("stage127_preflight_not_pass")
    if not matrix.stage128_read_only_absorption_pass:
        issues.append("stage128_read_only_absorption_not_pass")
    if not matrix.stage129_cim_governor_pass:
        issues.append("stage129_cim_governor_not_pass")
    if matrix.direct_v571_merge_detected:
        issues.append("direct_v571_merge_detected")
    if matrix.cross_project_write_allowed:
        issues.append("cross_project_write_allowed")
    if matrix.unauthorized_cross_reads != 0 or matrix.unauthorized_cross_writes != 0:
        issues.append("unauthorized_cross_project_access")
    if matrix.raw_manuscript_cross_project_leakage != 0:
        issues.append("raw_manuscript_cross_project_leakage")
    if matrix.canon_auto_resolution_count != 0:
        issues.append("canon_auto_resolution_not_zero")
    if matrix.provider_default_calls != 0:
        issues.append("provider_default_calls_nonzero")
    if matrix.node2_raw_reveal_access != 0:
        issues.append("node2_raw_reveal_access_nonzero")
    if not matrix.evidence_complete:
        issues.append("stage127_129_evidence_incomplete")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "matrix": matrix.to_dict(),
        "stage_evidence": [e.to_dict() for e in evidences],
    }


def _stage_evidence(root: Path, stage: str, paths: tuple[str, str]) -> StageEvidence:
    report = _read_json(root / paths[0])
    gate = _read_json(root / paths[1])
    title = report.get("title") or gate.get("title") or stage
    status = "pass" if report.get("status") == "pass" and gate.get("status") == "pass" else "blocked"
    return StageEvidence(stage=stage, title=title, status=status, report_path=paths[0], release_gate_path=paths[1])


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        return {}
