from __future__ import annotations
from .contracts import DriftGuardReport
from .style_genome import build_style_genome


def run_style_drift_guard(genome_payload: dict | None = None, candidate_delta: float = 0.12, allowed_delta: float = 0.22) -> dict:
    genome_payload = genome_payload or build_style_genome()
    action = "ALLOW" if candidate_delta <= allowed_delta else "BLOCK"
    issues = () if action == "ALLOW" else ("style_drift_exceeds_allowed_delta",)
    report = DriftGuardReport(
        status="pass" if not issues else "blocked",
        genome_id=genome_payload.get("genome_id", "unknown"),
        voice_drift_score=round(candidate_delta, 3),
        allowed_delta=allowed_delta,
        action=action,
        issues=issues,
    )
    payload = report.to_dict()
    payload.update({
        "stage": "106.3",
        "title": "Authorial Drift Guard",
        "raw_manuscript_provider_leakage": 0,
        "provider_call_count": 0,
    })
    return payload
