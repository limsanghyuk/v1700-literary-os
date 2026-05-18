from __future__ import annotations

from v1700.provider_ensemble.contracts import ProviderCandidate


def build_fixture_candidate_pool(provider_profiles: tuple[dict, ...] = ()) -> tuple[ProviderCandidate, ...]:
    profile_by_id = {profile["provider_id"]: profile for profile in provider_profiles}
    fixtures = (
        ("ollama-local", "ollama", "structure and privacy-first offline continuity", ()),
        ("gpt-frontier", "gpt", "schema discipline and branchpoint-safe refinement", ()),
        ("claude-editorial", "claude", "subtext-sensitive surface prose without raw reveal leakage", ()),
        ("gemini-fast", "gemini", "fast broad-context outline with READER_ONLY leakage", ("READER_ONLY_leakage",)),
    )
    candidates = []
    for index, (provider_id, provider_kind, response, flags) in enumerate(fixtures, start=1):
        profile = profile_by_id.get(provider_id, {})
        candidates.append(
            ProviderCandidate(
                candidate_id=f"stage96-candidate-{index}",
                provider_id=provider_id,
                provider_kind=provider_kind,
                prompt_id="stage96-ensemble-fixture",
                normalized_response=response,
                estimated_cost=float(profile.get("estimated_cost_units", 0.1)),
                latency_ms=int(profile.get("average_latency_ms", 300)),
                safety_flags=flags,
                metadata={
                    "stage": "96C",
                    "source": "dry_run_fixture_candidate",
                    "provider_average_score": profile.get("average_score", 8.0),
                },
            )
        )
    return tuple(candidates)
