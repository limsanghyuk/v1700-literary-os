from __future__ import annotations

from statistics import mean

from v1700.provider_adapters.contracts import NormalizedProviderResponse
from v1700.provider_evaluation.contracts import (
    ProviderEvaluationProfile,
    ProviderEvaluationPrompt,
    ProviderEvaluationScore,
)


_LATENCY_BY_KIND = {
    "ollama": 180,
    "gpt": 420,
    "claude": 460,
    "gemini": 390,
}

_COST_PER_OUTPUT_TOKEN = {
    "ollama": 0.0,
    "gpt": 0.004,
    "claude": 0.005,
    "gemini": 0.003,
}

_STRENGTHS = {
    "ollama": ("local_privacy", "zero_cloud_cost", "offline_dry_run"),
    "gpt": ("rule_following", "structured_reasoning", "schema_discipline"),
    "claude": ("literary_surface", "subtext_sensitivity", "long_context_editorial_tone"),
    "gemini": ("fast_broad_context", "multimodal_extension_path", "low_latency_cloud_route"),
}

_WEAKNESSES = {
    "ollama": ("quality_varies_by_local_model",),
    "gpt": ("cloud_cost_requires_policy",),
    "claude": ("cloud_cost_requires_policy",),
    "gemini": ("style_consistency_needs_guardrails",),
}


def score_normalized_response(
    response: NormalizedProviderResponse,
    prompt: ProviderEvaluationPrompt,
) -> ProviderEvaluationScore:
    issues: list[str] = list(response.issues)
    normalized_schema_pass = response.normalized_status == "pass" and bool(response.text_sha256)
    if not normalized_schema_pass:
        issues.append("normalized_schema_failed")
    if response.live_call_performed:
        issues.append("live_call_performed_during_release_evaluation")

    latency_ms = _LATENCY_BY_KIND.get(response.provider_kind, 600)
    estimated_cost_units = round(response.output_tokens * _COST_PER_OUTPUT_TOKEN.get(response.provider_kind, 0.006), 3)
    safety_score = 10.0 if not response.safety_labels and not response.live_call_performed else 7.0
    literary_quality_score = _literary_quality_score(response, prompt)
    branchpoint_compliance_score = 10.0 if not response.live_call_performed and normalized_schema_pass else 6.0

    return ProviderEvaluationScore(
        provider_id=response.provider_id,
        provider_kind=response.provider_kind,
        prompt_id=prompt.prompt_id,
        request_id=response.request_id,
        normalized_schema_pass=normalized_schema_pass,
        latency_ms=latency_ms,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        estimated_cost_units=estimated_cost_units,
        safety_score=safety_score,
        literary_quality_score=literary_quality_score,
        branchpoint_compliance_score=branchpoint_compliance_score,
        live_call_performed=response.live_call_performed,
        issues=tuple(sorted(set(issues))),
    )


def build_provider_profiles(scores: tuple[ProviderEvaluationScore, ...]) -> tuple[ProviderEvaluationProfile, ...]:
    provider_ids = sorted({score.provider_id for score in scores})
    profiles: list[ProviderEvaluationProfile] = []
    for provider_id in provider_ids:
        subset = [score for score in scores if score.provider_id == provider_id]
        provider_kind = subset[0].provider_kind
        profiles.append(
            ProviderEvaluationProfile(
                provider_id=provider_id,
                provider_kind=provider_kind,
                average_score=round(mean(score.total_score for score in subset), 2),
                average_latency_ms=round(mean(score.latency_ms for score in subset)),
                estimated_cost_units=round(sum(score.estimated_cost_units for score in subset), 3),
                strengths=_STRENGTHS.get(provider_kind, ("unknown_strength_profile",)),
                weaknesses=_WEAKNESSES.get(provider_kind, ("unknown_weakness_profile",)),
            )
        )
    return tuple(sorted(profiles, key=lambda item: (-item.average_score, item.provider_id)))


def _literary_quality_score(response: NormalizedProviderResponse, prompt: ProviderEvaluationPrompt) -> float:
    base = 8.0
    if "scene" in prompt.task or "render" in prompt.task:
        base += 0.25
    if response.provider_kind == "claude":
        base += 0.35
    elif response.provider_kind == "gpt":
        base += 0.25
    elif response.provider_kind == "gemini":
        base += 0.15
    elif response.provider_kind == "ollama":
        base += 0.05
    if response.output_tokens >= 20:
        base += 0.15
    return round(min(base, 9.2), 2)
