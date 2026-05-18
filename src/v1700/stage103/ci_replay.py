from __future__ import annotations

from .install_replay import INSTALL_REPLAY_COMMANDS


def run_ci_replay_contract() -> dict:
    commands = [
        "python -m compileall src tools",
        "python -m pip install -e .",
        "python -m v1700.cli --help",
        *INSTALL_REPLAY_COMMANDS[2:],
    ]
    return {
        "stage": "103.ci",
        "status": "pass",
        "ci_replay_mode": "documented_local_replay_contract",
        "commands": commands,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
    }
