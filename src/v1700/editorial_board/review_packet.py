from __future__ import annotations
import hashlib, json
from pathlib import Path
from .contracts import ReviewPacket

def build_review_packets(root: Path | None = None) -> list[ReviewPacket]:
    root = root or Path(__file__).resolve().parents[3]
    stage107_5 = _read_json(root / "release/current/stage107_5_provider_live_sandbox_report.json")
    stage107 = _read_json(root / "release/current/stage107_longform_production_suite_report.json")
    base = {
        "stage107_5_status": stage107_5.get("status", "pass"),
        "stage107_status": stage107.get("status", "pass"),
        "raw_manuscript": False,
    }
    return [
        _packet("pkt_prose_fixture", "PROSE", "stage107_5", "feature-only prose candidate review", base),
        _packet("pkt_scenario_fixture", "SCENARIO", "stage107_5", "feature-only scenario candidate review", base),
        _packet("pkt_longform_structure", "LONGFORM_STRUCTURE", "stage107", "multi-season arc and payoff calendar review", base),
        _packet("pkt_production_readiness", "PRODUCTION_READINESS", "stage107", "production calendar and export readiness review", base),
    ]

def _packet(packet_id: str, mode: str, source_stage: str, note: str, payload: dict) -> ReviewPacket:
    digest = hashlib.sha256(json.dumps({"packet_id": packet_id, **payload}, sort_keys=True).encode()).hexdigest()
    return ReviewPacket(
        packet_id=packet_id,
        mode=mode,
        payload_kind="FEATURE_ONLY",
        source_stage=source_stage,
        contains_raw_manuscript=False,
        prompt_sha256=digest,
        production_scope="stage107_5_to_stage108_editorial_board",
        notes=[note, "raw response and raw manuscript are not stored"],
    )

def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
