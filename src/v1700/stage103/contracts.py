from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


Status = Literal["pass", "warn", "blocked"]


@dataclass(frozen=True)
class InstallReplayResult:
    status: Status
    fresh_clone_ready: bool
    editable_install_ready: bool
    cli_smoke_ready: bool
    release_gate_replay_ready: bool
    documented_commands: tuple[str, ...]
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuntimeProfileContract:
    profile_id: Literal["dev", "release", "sandbox"]
    provider_mode: str
    allow_live_provider_calls: bool
    raw_manuscript_allowed: bool
    credential_source: str
    evidence_policy: str
    default_timeout_seconds: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuntimeProfileValidation:
    status: Status
    profiles: tuple[RuntimeProfileContract, ...]
    release_profile_safe: bool
    sandbox_opt_in_required: bool
    dev_profile_local_first: bool
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["profiles"] = [profile.to_dict() for profile in self.profiles]
        return payload


@dataclass(frozen=True)
class VaultProbeResult:
    status: Status
    vault_mode: Literal["LOCAL_ONLY"]
    raw_text_exported: bool
    provider_export_allowed: bool
    feature_fingerprint: str
    stored_feature_keys: tuple[str, ...]
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BackupRestoreResult:
    status: Status
    backup_format: str
    source_checksum: str
    restored_checksum: str
    metadata_only: bool
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ErrorReportContract:
    status: Status
    error_id: str
    severity: Literal["INFO", "WARN", "ERROR"]
    safe_message: str
    raw_prompt_included: bool
    credential_included: bool
    redaction_policy: str
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseNoteContract:
    status: Status
    stage: str
    package_name: str
    highlights: tuple[str, ...]
    verification_commands: tuple[str, ...]
    known_limits: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
