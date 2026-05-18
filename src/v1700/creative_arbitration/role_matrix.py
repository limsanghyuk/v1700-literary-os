from __future__ import annotations

from .contracts import ProviderRole


def build_provider_role_matrix() -> dict:
    roles = (
        ProviderRole(
            provider_id="gpt_reasoning_lane",
            provider_kind="gpt",
            assigned_tasks=("STRUCTURE", "PROSE_SURFACE"),
            release_mode="FIXTURE_ONLY",
            strengths=("outline reasoning", "revision synthesis", "constraint following"),
        ),
        ProviderRole(
            provider_id="claude_long_context_lane",
            provider_kind="claude",
            assigned_tasks=("DIALOGUE", "PROSE_SURFACE"),
            release_mode="FIXTURE_ONLY",
            strengths=("long context", "subtext dialogue", "tone consistency"),
        ),
        ProviderRole(
            provider_id="gemini_visual_lane",
            provider_kind="gemini",
            assigned_tasks=("VISUAL", "SCENARIO_BEAT"),
            release_mode="FIXTURE_ONLY",
            strengths=("visual beats", "spatial reasoning", "multimodal-ready scene planning"),
        ),
        ProviderRole(
            provider_id="ollama_local_privacy_lane",
            provider_kind="ollama",
            assigned_tasks=("LOCAL_PRIVACY", "STRUCTURE"),
            release_mode="FIXTURE_ONLY",
            strengths=("local-first drafting", "privacy-preserving fixtures", "offline continuity"),
        ),
        ProviderRole(
            provider_id="fixture_release_lane",
            provider_kind="fixture",
            assigned_tasks=("STRUCTURE", "DIALOGUE", "VISUAL", "SCENARIO_BEAT"),
            release_mode="FIXTURE_ONLY",
            strengths=("deterministic release evidence", "provider-zero gate execution"),
        ),
        ProviderRole(
            provider_id="mock_contract_lane",
            provider_kind="mock",
            assigned_tasks=("PROSE_SURFACE", "LOCAL_PRIVACY"),
            release_mode="FIXTURE_ONLY",
            strengths=("contract negative testing", "leakage simulation"),
        ),
    )
    issues = [role.provider_id for role in roles if role.live_call_allowed_in_release or role.raw_manuscript_allowed]
    return {
        "stage": "105.1",
        "title": "Provider Creative Role Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "provider_count": len(roles),
        "release_mode": "fixture_only",
        "live_provider_call_count_in_release": 0,
        "roles": [role.to_dict() for role in roles],
    }
