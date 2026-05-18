from __future__ import annotations

from pathlib import Path

from .contracts import InstallReplayResult


INSTALL_REPLAY_COMMANDS = (
    "python -m pip install -e .",
    "python -m v1700.cli --help",
    "python tools/run_mandatory_predevelopment_check.py",
    "python tools/run_stage102_release_gate.py",
    "python tools/run_stage103_release_gate.py",
    "python tools/run_release_gate.py",
    "python tools/run_stage72_repo_doctor.py",
    "python -m pytest -q tests",
)


def run_install_replay_probe(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    required_paths = [
        root / "pyproject.toml",
        root / "README.md",
        root / "src" / "v1700" / "cli.py",
        root / "tools" / "run_release_gate.py",
        root / "tools" / "run_stage72_repo_doctor.py",
        root / "tools" / "run_mandatory_predevelopment_check.py",
    ]
    missing = [path.relative_to(root).as_posix() for path in required_paths if not path.exists()]
    result = InstallReplayResult(
        status="pass" if not missing else "blocked",
        fresh_clone_ready=not missing,
        editable_install_ready=(root / "pyproject.toml").exists(),
        cli_smoke_ready=(root / "src" / "v1700" / "cli.py").exists(),
        release_gate_replay_ready=(root / "tools" / "run_release_gate.py").exists(),
        documented_commands=INSTALL_REPLAY_COMMANDS,
        issues=tuple(f"missing:{rel}" for rel in missing),
    )
    return result.to_dict()
