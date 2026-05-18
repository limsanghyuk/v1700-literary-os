from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class GitNexusProbeResult:
    installed: bool
    command: str | None
    optional_runtime_dependency: bool = False
    fallback_available: bool = True
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "installed": self.installed,
            "command": self.command,
            "optional_runtime_dependency": self.optional_runtime_dependency,
            "fallback_available": self.fallback_available,
            "error": self.error,
        }


@dataclass(frozen=True)
class GitNexusCommandResult:
    capability: str
    command: tuple[str, ...]
    returncode: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out

    def to_dict(self) -> dict:
        return {
            "capability": self.capability,
            "command": list(self.command),
            "returncode": self.returncode,
            "ok": self.ok,
            "timed_out": self.timed_out,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


@dataclass(frozen=True)
class GitNexusIndexStatus:
    alias: str
    registered: bool
    path: str = ""
    storage_path: str = ""
    indexed_at: str = ""
    stats: dict = field(default_factory=dict)
    registry_path: str = ""
    stale: bool = False
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "alias": self.alias,
            "registered": self.registered,
            "path": self.path,
            "storage_path": self.storage_path,
            "indexed_at": self.indexed_at,
            "stats": dict(self.stats),
            "registry_path": self.registry_path,
            "stale": self.stale,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class GitNexusAdapterConfig:
    repo_alias: str = "v1700_stage72_3_ascii"
    timeout_seconds: float = 8.0
    registry_path: Path | None = None

    def resolved_registry_path(self) -> Path:
        return self.registry_path or Path.home() / ".gitnexus" / "registry.json"
