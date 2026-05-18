from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Stage111Contract:
    stage: str = "111"
    baseline_stage: str = "110"
    title: str = "V485 Absorption Candidate Bridge"
    absorption_mode: str = "wrap_only"
    direct_v485_code_import_allowed: bool = False
    direct_v485_metadata_import_allowed: bool = False
    release_gate_replacement_allowed: bool = False
    live_provider_call_count_in_release_gate: int = 0
    raw_manuscript_provider_leakage: int = 0
    credential_leakage: int = 0
    raw_response_stored: bool = False
    writer_decision_required: bool = True
    python_fallback_required: bool = True
    gitnexus_runtime_dependency_required: bool = False
    def to_dict(self) -> dict:
        return asdict(self)
