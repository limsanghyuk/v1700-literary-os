from __future__ import annotations

import hashlib
import os
import re
from collections.abc import Iterable

from v1700.provider_adapters.config import build_default_multi_provider_configs
from v1700.provider_adapters.contracts import (
    CredentialAuditReport,
    ProviderAdapterConfig,
    ProviderCredentialStatus,
)

_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),
    re.compile(r"anthropic-[A-Za-z0-9_\-]{16,}"),
)


def _fingerprint(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest().upper()
    return f"sha256:{digest[:12]}...{digest[-8:]}"


def _status_for(config: ProviderAdapterConfig) -> ProviderCredentialStatus:
    if not config.requires_secret:
        return ProviderCredentialStatus(
            provider_id=config.provider_id,
            provider_kind=config.provider_kind,
            requires_secret=False,
            api_key_env=None,
            env_present=True,
            redacted_fingerprint=None,
            status="secret_not_required",
            issues=(),
        )
    env_name = config.api_key_env or ""
    value = os.getenv(env_name, "")
    if not value:
        return ProviderCredentialStatus(
            provider_id=config.provider_id,
            provider_kind=config.provider_kind,
            requires_secret=True,
            api_key_env=env_name,
            env_present=False,
            redacted_fingerprint=None,
            status="missing_optional_for_dry_run",
            issues=("secret_env_not_present",),
        )
    issues: list[str] = []
    if len(value.strip()) < 8:
        issues.append("secret_value_too_short_for_live_use")
    return ProviderCredentialStatus(
        provider_id=config.provider_id,
        provider_kind=config.provider_kind,
        requires_secret=True,
        api_key_env=env_name,
        env_present=True,
        redacted_fingerprint=_fingerprint(value),
        status="present_redacted",
        issues=tuple(issues),
    )


def audit_provider_credentials(configs: Iterable[ProviderAdapterConfig] | None = None) -> CredentialAuditReport:
    configs = tuple(configs or build_default_multi_provider_configs(allow_live_call=False))
    statuses = tuple(_status_for(config) for config in configs)
    serialized = " ".join(str(item.to_dict()) for item in statuses)
    leaked = any(pattern.search(serialized) for pattern in _SECRET_PATTERNS)
    issues: list[str] = []
    if leaked:
        issues.append("secret_value_leaked_in_audit_report")
    if len(statuses) != 4:
        issues.append("credential_provider_count_not_4")
    plain_secret_preview_count = 1 if leaked else 0
    return CredentialAuditReport(
        stage="93",
        status="pass" if not issues else "blocked",
        credential_statuses=statuses,
        secret_value_leaked=leaked,
        plain_secret_preview_count=plain_secret_preview_count,
        provider_default_calls=0,
        node2_raw_reveal_access_count=0,
        issues=tuple(issues),
    )
