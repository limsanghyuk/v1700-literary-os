from __future__ import annotations

from v1700.provider_adapters.config import build_default_multi_provider_configs
from v1700.provider_adapters.contracts import ProviderRequest, ProviderResponse
from v1700.provider_adapters.credential_audit import audit_provider_credentials
from v1700.provider_adapters.normalization import normalize_provider_response
from v1700.provider_adapters.router import MultiProviderAdapterRouter
from v1700.provider_evaluation.contracts import ProviderEvaluationReport
from v1700.provider_evaluation.prompt_suite import build_stage94_prompt_suite
from v1700.provider_evaluation.scoring import build_provider_profiles, score_normalized_response


class ProviderEvaluationHarness:
    """Dry-run evaluation harness for provider comparison.

    Stage94 deliberately evaluates the provider contracts without making live
    calls. The same prompt suite is routed to Ollama/GPT/Claude/Gemini adapters,
    normalized into the Stage93 response contract, and scored with deterministic
    release-safe metrics.
    """

    def __init__(self, *, allow_live_call: bool = False) -> None:
        self.configs = build_default_multi_provider_configs(allow_live_call=allow_live_call)
        self.router = MultiProviderAdapterRouter(self.configs)

    def evaluate(self) -> ProviderEvaluationReport:
        prompts = build_stage94_prompt_suite()
        all_scores = []
        live_call_count = 0
        for prompt in prompts:
            request = ProviderRequest(
                request_id=f"stage94-{prompt.prompt_id}",
                task=prompt.task,
                system=prompt.system,
                prompt=prompt.prompt,
                metadata={"stage": "94", "branchpoint_requirements": prompt.branchpoint_requirements},
            )
            for response in self.router.dry_run_all(request):
                normalized = normalize_provider_response(
                    provider_id=response.provider_id,
                    provider_kind=response.provider_kind,
                    request_id=response.request_id,
                    raw=_raw_from_provider_response(response),
                    live_call_performed=response.live_call_performed,
                )
                live_call_count += 1 if normalized.live_call_performed else 0
                all_scores.append(score_normalized_response(normalized, prompt))

        scores = tuple(all_scores)
        profiles = build_provider_profiles(scores)
        credential_audit = audit_provider_credentials(self.configs)
        normalized_schema_fail_count = sum(1 for score in scores if not score.normalized_schema_pass)
        issues: list[str] = []
        if len(self.configs) != 4:
            issues.append("configured_provider_count_not_4")
        if len(prompts) < 2:
            issues.append("prompt_suite_too_small")
        if live_call_count != 0:
            issues.append("live_call_count_not_zero")
        if normalized_schema_fail_count != 0:
            issues.append("normalized_schema_fail_count_not_zero")
        if credential_audit.secret_value_leaked:
            issues.append("credential_secret_value_leaked")
        if any(score.branchpoint_compliance_score < 9.0 for score in scores):
            issues.append("branchpoint_compliance_score_below_floor")
        best_provider_id = profiles[0].provider_id if profiles else ""
        return ProviderEvaluationReport(
            stage="94",
            status="pass" if not issues else "blocked",
            mode="dry_run_fixture_evaluation",
            prompt_count=len(prompts),
            provider_count=len(self.configs),
            evaluation_count=len(scores),
            scores=scores,
            provider_profiles=profiles,
            best_provider_id=best_provider_id,
            live_call_count=live_call_count,
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
            credential_secret_value_leaked=credential_audit.secret_value_leaked,
            normalized_schema_fail_count=normalized_schema_fail_count,
            issues=tuple(issues),
        )


def run_stage94_provider_evaluation_smoke() -> dict:
    return ProviderEvaluationHarness(allow_live_call=False).evaluate().to_dict()


def _raw_from_provider_response(response: ProviderResponse) -> dict:
    text = _fixture_text(response)
    if response.provider_kind == "ollama":
        return {"message": {"content": text}, "done": True, "prompt_eval_count": 36, "eval_count": 54}
    if response.provider_kind == "gpt":
        return {"output_text": text, "status": "completed", "usage": {"input_tokens": 36, "output_tokens": 54}}
    if response.provider_kind == "claude":
        return {"content": [{"type": "text", "text": text}], "stop_reason": "end_turn", "usage": {"input_tokens": 36, "output_tokens": 54}}
    if response.provider_kind == "gemini":
        return {
            "candidates": [{"content": {"parts": [{"text": text}]}, "finishReason": "STOP"}],
            "usageMetadata": {"promptTokenCount": 36, "candidatesTokenCount": 54},
        }
    return {"text": text}


def _fixture_text(response: ProviderResponse) -> str:
    return (
        f"{response.provider_id} normalized dry-run evaluation: reader-facing prose is allowed, "
        "raw reveal access is blocked, and branchpoint compliance remains provider-zero."
    )
