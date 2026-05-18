from __future__ import annotations

import subprocess
from pathlib import Path

from v1700.sidecars.gitnexus.contracts import GitNexusAdapterConfig, GitNexusCommandResult
from v1700.sidecars.gitnexus.probe import probe_gitnexus
from v1700.sidecars.gitnexus.result_normalizer import normalize_gitnexus_result


class GitNexusCliAdapter:
    def __init__(self, config: GitNexusAdapterConfig | None = None) -> None:
        self.config = config or GitNexusAdapterConfig()

    def available(self) -> bool:
        return probe_gitnexus().installed

    def list_repositories(self, cwd: Path) -> dict:
        return self._normalized("list", cwd, ["list"])

    def query(self, cwd: Path, query: str, *, context: str = "", goal: str = "", limit: int = 5) -> dict:
        args = ["query", "-r", self.config.repo_alias, query, "-l", str(limit)]
        if context:
            args.extend(["-c", context])
        if goal:
            args.extend(["-g", goal])
        return self._normalized("query", cwd, args)

    def context(self, cwd: Path, name: str) -> dict:
        return self._normalized("context", cwd, ["context", "-r", self.config.repo_alias, name])

    def impact(self, cwd: Path, target: str, *, include_tests: bool = True) -> dict:
        args = ["impact", "-r", self.config.repo_alias, target]
        if include_tests:
            args.append("--include-tests")
        return self._normalized("impact", cwd, args)

    def detect_changes(self, cwd: Path, *, scope: str = "all") -> dict:
        return self._normalized(
            "detect_changes",
            cwd,
            ["detect-changes", "-r", self.config.repo_alias, "-s", scope],
        )

    def _normalized(self, capability: str, cwd: Path, args: list[str]) -> dict:
        return normalize_gitnexus_result(self._run(capability, cwd, args))

    def _run(self, capability: str, cwd: Path, args: list[str]) -> GitNexusCommandResult:
        probe = probe_gitnexus()
        if not probe.installed or not probe.command:
            return GitNexusCommandResult(
                capability=capability,
                command=tuple(args),
                returncode=127,
                stderr=probe.error,
            )

        command = [probe.command, *args]
        try:
            completed = subprocess.run(
                command,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.config.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return GitNexusCommandResult(
                capability=capability,
                command=tuple(command),
                returncode=124,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "gitnexus command timed out",
                timed_out=True,
            )

        return GitNexusCommandResult(
            capability=capability,
            command=tuple(command),
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
