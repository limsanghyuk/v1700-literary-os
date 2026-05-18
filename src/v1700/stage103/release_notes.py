from __future__ import annotations

from .contracts import ReleaseNoteContract
from .install_replay import INSTALL_REPLAY_COMMANDS


PACKAGE_NAME = "V1700_stage103_production_hardening_deployment_readiness_FIXED.zip"


def build_stage103_release_notes() -> dict:
    notes = ReleaseNoteContract(
        status="pass",
        stage="103",
        package_name=PACKAGE_NAME,
        highlights=(
            "Production hardening and deployment readiness layer over Stage102.",
            "Fresh-clone install replay commands and CI replay contract.",
            "Dev/release/sandbox runtime profile separation.",
            "Local-only manuscript vault, feature-only backup/restore, and safe error reporting.",
            "Provider-zero and Node2 boundary remain intact.",
        ),
        verification_commands=INSTALL_REPLAY_COMMANDS,
        known_limits=(
            "Stage103 is deployment readiness, not a full commercial SaaS/desktop installer.",
            "Live provider benchmarking remains opt-in sandbox work outside release gates.",
        ),
    )
    return notes.to_dict()
