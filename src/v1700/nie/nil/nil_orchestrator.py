from __future__ import annotations

from typing import Any

from v1700.nie.arc.tension_curve_report import build_stage117_tension_curve_report
from v1700.nie.characters.cim_report import build_stage115_cim_report
from v1700.nie.emotion.amw_report import build_stage114_amw_report
from v1700.nie.nil.contracts import NILComponentStatus, NILLoopReport
from v1700.nie.rag.rag_fusion_report import build_stage116_rag_fusion_report
from v1700.nie.reward.reward_signal_report import build_stage113_reward_bridge_report

LOOP_ORDER = (
    "CharacterInfluenceMatrix",
    "StructuralBalance",
    "AdaptiveMomentumWeights",
    "MAERewardSignal",
    "PhysicsRewardBridge",
    "CoefficientUpdateProposal",
    "DomainSpecificRAGFusion",
    "NarrativeTensionCurve",
)


def run_nil_loop() -> dict[str, Any]:
    """Run the deterministic Stage118 Narrative Intelligence Loop fixture.

    Stage118 deliberately composes cached/fixture outputs from Stage113~117.
    It proves the wiring and evidence contract without live providers, raw
    manuscript export, or Node2 reveal access.
    """

    reward = build_stage113_reward_bridge_report()
    amw = build_stage114_amw_report()
    cim = build_stage115_cim_report()
    rag = build_stage116_rag_fusion_report()
    tension = build_stage117_tension_curve_report()

    components = (
        _component("reward_bridge", reward, _reward_summary(reward)),
        _component("adaptive_momentum_weights", amw, _amw_summary(amw)),
        _component("character_influence_matrix", cim, _cim_summary(cim)),
        _component("domain_rag_fusion", rag, _rag_summary(rag)),
        _component("narrative_tension_curve", tension, _tension_summary(tension)),
    )
    issues: list[str] = []
    issues.extend(_component_issues(components))
    invariant_counts = _invariant_counts(reward, amw, cim, rag, tension)
    if any(value != 0 for value in invariant_counts.values()):
        issues.append("nil_invariant_count_nonzero")
    convergence = _convergence(reward, amw, cim, rag, tension)
    if convergence["loop_closure_status"] != "pass":
        issues.append("nil_loop_closure_failed")

    report = NILLoopReport(
        stage="118",
        baseline_stage="117",
        title="NIL Orchestrator",
        status="pass" if not issues else "blocked",
        components=components,
        loop_order=LOOP_ORDER,
        convergence=convergence,
        invariant_counts=invariant_counts,
        issues=tuple(issues),
    )
    data = report.to_dict()
    data.update({
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "component_reports": {
            "stage113_reward_bridge": reward,
            "stage114_adaptive_momentum_weights": amw,
            "stage115_character_influence_matrix": cim,
            "stage116_domain_rag_fusion": rag,
            "stage117_narrative_tension_curve": tension,
        },
    })
    return data


def _component(name: str, report: dict[str, Any], summary: dict[str, Any]) -> NILComponentStatus:
    return NILComponentStatus(
        name=name,  # type: ignore[arg-type]
        status="pass" if report.get("status") == "pass" else "blocked",
        stage=str(report.get("stage", "")),
        issue_count=len(report.get("issues", [])),
        summary=summary,
    )


def _component_issues(components: tuple[NILComponentStatus, ...]) -> list[str]:
    return [f"{component.name}_blocked" for component in components if component.status != "pass"]


def _reward_summary(report: dict[str, Any]) -> dict[str, Any]:
    signal = report.get("reward_signal", {})
    return {
        "reward": signal.get("reward"),
        "advantage": signal.get("advantage"),
        "baseline_after": signal.get("baseline_after"),
        "coefficient_update_proposal_count": len(report.get("coefficient_update_proposals", [])),
    }


def _amw_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "alpha_before": report.get("alpha_before"),
        "alpha_after": report.get("alpha_after"),
        "drift_guard": report.get("drift_guard"),
    }


def _cim_summary(report: dict[str, Any]) -> dict[str, Any]:
    matrix = report.get("character_influence_matrix", {})
    centrality = matrix.get("centrality", {})
    return {
        "character_count": matrix.get("character_count"),
        "asymmetric_pair_count": matrix.get("asymmetric_pair_count"),
        "triangle_count": matrix.get("triangle_count"),
        "high_tension_triangle_count": matrix.get("high_tension_triangle_count"),
        "role_tiers": centrality.get("role_tiers", {}),
    }


def _rag_summary(report: dict[str, Any]) -> dict[str, Any]:
    classifier = report.get("query_intent_classifier", {})
    rows = classifier.get("classified_queries", [])
    return {
        "intent_coverage": sorted({row.get("intent") for row in rows}),
        "classified_query_count": len(rows),
        "llm_call_count": classifier.get("llm_call_count"),
        "domain_tuning_enabled": report.get("adaptive_hybrid_weights", {}).get("domain_tuning_enabled"),
    }


def _tension_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "scene_count": report.get("scene_count"),
        "loss": report.get("loss", {}),
        "act_counts": report.get("act_counts", {}),
    }


def _invariant_counts(*reports: dict[str, Any]) -> dict[str, int]:
    keys = {
        "provider_call_count": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
    }
    for report in reports:
        for key in list(keys):
            value = report.get(key)
            if value is None and key == "provider_call_count":
                value = report.get("provider_default_calls")
            try:
                keys[key] += int(value or 0)
            except Exception:
                keys[key] += 0
    return keys


def _convergence(reward: dict[str, Any], amw: dict[str, Any], cim: dict[str, Any], rag: dict[str, Any], tension: dict[str, Any]) -> dict[str, Any]:
    reward_signal = reward.get("reward_signal", {})
    drift_guard = amw.get("drift_guard", {})
    matrix = cim.get("character_influence_matrix", {})
    intents = {row.get("intent") for row in rag.get("query_intent_classifier", {}).get("classified_queries", [])}
    loss = tension.get("loss", {})
    checks = {
        "positive_reward_advantage": float(reward_signal.get("advantage", 0.0)) > 0.0,
        "amw_drift_guard_pass": drift_guard.get("status") == "pass",
        "cim_has_high_tension_triangles": int(matrix.get("high_tension_triangle_count", 0)) >= 1,
        "rag_covers_required_intents": intents == {"CHARACTER", "EMOTIONAL", "PLOT_EVENT"},
        "tension_final_loss_pass": float(loss.get("final_loss", 1.0)) < 0.10,
    }
    return {
        "loop_closure_status": "pass" if all(checks.values()) else "blocked",
        "checks": checks,
        "reward_advantage": reward_signal.get("advantage"),
        "amw_max_single_shift": drift_guard.get("observed_max_single_shift"),
        "high_tension_triangle_count": matrix.get("high_tension_triangle_count"),
        "rag_intents": sorted(intents),
        "final_tension_loss": loss.get("final_loss"),
    }
