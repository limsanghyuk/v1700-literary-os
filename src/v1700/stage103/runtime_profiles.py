from __future__ import annotations

from .contracts import RuntimeProfileContract, RuntimeProfileValidation


def build_runtime_profiles() -> tuple[RuntimeProfileContract, ...]:
    return (
        RuntimeProfileContract(
            profile_id="dev",
            provider_mode="fixture_local",
            allow_live_provider_calls=False,
            raw_manuscript_allowed=False,
            credential_source="none_by_default",
            evidence_policy="write_local_release_evidence",
            default_timeout_seconds=30,
        ),
        RuntimeProfileContract(
            profile_id="release",
            provider_mode="fixture_or_mock_only",
            allow_live_provider_calls=False,
            raw_manuscript_allowed=False,
            credential_source="forbidden",
            evidence_policy="provider_zero_clean_evidence",
            default_timeout_seconds=30,
        ),
        RuntimeProfileContract(
            profile_id="sandbox",
            provider_mode="opt_in_live_provider_guarded",
            allow_live_provider_calls=False,
            raw_manuscript_allowed=False,
            credential_source="explicit_env_only",
            evidence_policy="sandbox_evidence_never_release_gate",
            default_timeout_seconds=90,
        ),
    )


def validate_runtime_profiles() -> dict:
    profiles = build_runtime_profiles()
    issues: list[str] = []
    release = next(profile for profile in profiles if profile.profile_id == "release")
    sandbox = next(profile for profile in profiles if profile.profile_id == "sandbox")
    dev = next(profile for profile in profiles if profile.profile_id == "dev")
    if release.allow_live_provider_calls or release.raw_manuscript_allowed:
        issues.append("release_profile_allows_live_or_raw_manuscript")
    if sandbox.allow_live_provider_calls:
        issues.append("sandbox_profile_live_calls_enabled_by_default")
    if dev.provider_mode != "fixture_local":
        issues.append("dev_profile_not_local_first")
    result = RuntimeProfileValidation(
        status="pass" if not issues else "blocked",
        profiles=profiles,
        release_profile_safe=not release.allow_live_provider_calls and not release.raw_manuscript_allowed,
        sandbox_opt_in_required=not sandbox.allow_live_provider_calls and sandbox.credential_source == "explicit_env_only",
        dev_profile_local_first=dev.provider_mode == "fixture_local",
        issues=tuple(issues),
    )
    return result.to_dict()
