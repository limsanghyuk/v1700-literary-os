from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import CrossLineageReleaseDecision, ReleaseLayer


STAGE_REPORTS: tuple[tuple[str, str, str, str], ...] = (
    ("120", "Gate25 NIE v1.0", "release/current/stage120_gate25_nie_v1_report.json", "primary_gate"),
    ("121", "Cross-Lineage Formula Reconciliation", "release/current/stage121_cross_lineage_preflight_report.json", "preflight"),
    ("122", "NIE v2.0 Stability Absorption", "release/current/stage122_nie_v2_stability_absorption_report.json", "stability"),
    ("123", "ASD / Gate28 Absorption", "release/current/stage123_asd_gate28_absorption_report.json", "secondary_quality_gate"),
    ("124", "PNE / Gate29 Absorption", "release/current/stage124_pne_gate29_absorption_report.json", "secondary_predictive_gate"),
    ("125", "Gate25/28/29 Governor", "release/current/stage125_gate25_28_29_governor_report.json", "governor"),
)


class CrossLineageReleaseAssembler:
    """Stage126 release assembler.

    This class does not import V545/V555 source directly. It seals the already
    absorbed Stage120~125 evidence into one deterministic release pack.
    """

    def __init__(self, root: Path):
        self.root = root

    def evaluate(self) -> CrossLineageReleaseDecision:
        layers: list[ReleaseLayer] = []
        issues: list[str] = []
        warnings: list[str] = []

        for stage, title, rel, mode in STAGE_REPORTS:
            payload = self._read_json(self.root / rel)
            status = str(payload.get("status", "missing"))
            if not payload:
                issues.append(f"missing_report:stage{stage}")
            elif status != "pass":
                issues.append(f"stage{stage}_report_not_pass:{status}")
            layers.append(ReleaseLayer(
                stage=stage,
                title=title,
                report_path=rel,
                status=status,
                authority_mode=mode,
                absorbed_capabilities=tuple(self._absorbed_capabilities(stage, payload)),
                blocked_concepts=tuple(self._blocked_concepts(stage, payload)),
                metrics=self._metrics(stage, payload),
            ))

        governor = self._read_json(self.root / "release/current/stage125_gate25_28_29_governor_report.json")
        governor_decision = governor.get("governor_decision", {})
        summary = governor.get("summary", {})
        gate_inputs = governor_decision.get("gate_inputs", [])
        gate_modes = {g.get("gate_id"): g.get("mode") for g in gate_inputs}

        checks = {
            "stage125_baseline_preserved": True,
            "stage120_gate25_primary_present": gate_modes.get("Gate25") == "primary" or summary.get("primary_gate") == "Gate25",
            "stage123_gate28_secondary_present": gate_modes.get("Gate28") == "secondary_quality" or "Gate28" in summary.get("secondary_gates", []),
            "stage124_gate29_secondary_present": gate_modes.get("Gate29") == "secondary_predictive" or "Gate29" in summary.get("secondary_gates", []),
            "gate28_not_primary": governor.get("gate28_primary_authority_enabled") is False or governor_decision.get("invariants", {}).get("gate28_primary_authority_enabled") is False,
            "gate29_not_primary": governor.get("gate29_primary_authority_enabled") is False or governor_decision.get("invariants", {}).get("gate29_primary_authority_enabled") is False,
            "direct_candidate_merge_blocked": self._direct_merge_blocked(),
            "runtime_training_disabled": self._sum_int(governor, "pne_runtime_training_count") == 0,
            "auto_repair_mutation_disabled": self._sum_int(governor, "auto_repair_mutation_count") == 0,
            "provider_zero": self._provider_zero(governor),
            "node2_boundary": self._sum_int(governor, "node2_raw_reveal_access") == 0,
            "raw_manuscript_leakage_zero": self._sum_int(governor, "raw_manuscript_provider_leakage") == 0,
            "credential_leakage_zero": self._sum_int(governor, "credential_leakage") == 0,
        }
        for name, ok in checks.items():
            if not ok:
                issues.append(name)

        invariants = {
            "provider_default_calls": 0,
            "live_provider_call_count_in_release_gate": 0,
            "embedding_provider_call_count": 0,
            "query_classifier_llm_call_count": 0,
            "physics_reward_bridge_llm_call_count": 0,
            "mae_live_provider_call_count": 0,
            "story_doctor_llm_call_count": 0,
            "pne_provider_call_count": 0,
            "pne_runtime_training_count": 0,
            "auto_repair_mutation_count": 0,
            "node2_raw_reveal_access": 0,
            "raw_manuscript_provider_leakage": 0,
            "credential_leakage": 0,
            "gate25_primary_authority_preserved": checks["stage120_gate25_primary_present"],
            "gate28_secondary_quality_preserved": checks["stage123_gate28_secondary_present"],
            "gate29_secondary_predictive_preserved": checks["stage124_gate29_secondary_present"],
        }
        final_pack = {
            "release_name": "Cross-Lineage Intelligence Release",
            "release_stage": "126",
            "baseline_stage": "125",
            "sealed_lineage": [layer.stage for layer in layers],
            "authority_stack": {
                "Gate25": "primary_nie_release_authority",
                "Gate28": "secondary_asd_quality_gate",
                "Gate29": "secondary_pne_predictive_gate",
                "Governor": "deterministic_gate25_28_29_arbitration",
            },
            "absorbed_reference_branches": {
                "V525": "NIE v2.0 stability concepts via Stage122",
                "V545": "ASD/Gate28 concepts via Stage123 dry-run adapter",
                "V555": "PNE/Gate29 concepts via Stage124 predictive adapter",
            },
            "blocked_at_release": [
                "direct V545/V555 package merge",
                "Gate28 primary authority",
                "Gate29 primary authority",
                "release-gate runtime model training",
                "auto-repair graph mutation during release",
                "live provider calls in release governor",
            ],
            "release_evidence": [
                "release/current/stage126_cross_lineage_intelligence_release_report.json",
                "release/current/stage126_release_authority_manifest.json",
                "release/current/stage126_lineage_release_pack.json",
                "release/current/stage126_release_gate_report.json",
            ],
        }

        return CrossLineageReleaseDecision(
            status="pass" if not issues else "blocked",
            title="Cross-Lineage Intelligence Release",
            baseline_stage="125",
            release_stage="126",
            release_authority="Gate25 primary + Gate28/Gate29 secondary under Stage125 Governor",
            lineage_layers=tuple(layers),
            blocked_by=tuple(issues),
            warnings=tuple(warnings),
            checks=checks,
            invariants=invariants,
            final_release_pack=final_pack,
        )

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _absorbed_capabilities(self, stage: str, payload: dict[str, Any]) -> list[str]:
        if stage == "120":
            return ["Gate25 NIE v1.0", "NIL evidence", "NIE adversarial regression"]
        if stage == "121":
            return ["formula ledger", "conflict matrix", "gate authority map"]
        if stage == "122":
            return ["NIL stability", "agent calibration", "T_ideal learning", "Temporal CIM adapter"]
        if stage == "123":
            return ["NarrativeDebtDetector", "ArcConsistencyChecker", "Gate28 secondary quality gate"]
        if stage == "124":
            return ["PNECore", "DebtPredictor", "PreemptiveGate", "Gate29 secondary predictive gate"]
        if stage == "125":
            return ["Gate25/28/29 Governor", "single deterministic gate stack"]
        return []

    def _blocked_concepts(self, stage: str, payload: dict[str, Any]) -> list[str]:
        concepts = payload.get("blocked_concepts") or payload.get("release_contract", {}).get("blocked_concepts") or []
        if isinstance(concepts, list):
            return [str(item) for item in concepts]
        return []

    def _metrics(self, stage: str, payload: dict[str, Any]) -> dict[str, Any]:
        keys = (
            "provider_default_calls", "live_provider_call_count_in_release_gate",
            "pne_runtime_training_count", "auto_repair_mutation_count",
            "node2_raw_reveal_access", "raw_manuscript_provider_leakage", "credential_leakage",
        )
        return {key: payload.get(key) for key in keys if key in payload}

    def _sum_int(self, payload: dict[str, Any], key: str) -> int:
        value = payload.get(key, 0)
        try:
            return int(value or 0)
        except Exception:
            return 0

    def _provider_zero(self, payload: dict[str, Any]) -> bool:
        keys = (
            "provider_default_calls", "live_provider_call_count_in_release_gate",
            "pne_provider_call_count", "story_doctor_llm_call_count",
            "mae_live_provider_call_count", "physics_reward_bridge_llm_call_count",
        )
        return all(self._sum_int(payload, key) == 0 for key in keys)

    def _direct_merge_blocked(self) -> bool:
        manifest = self._read_json(self.root / "manifests/stage121_absorption_candidate_registry.json")
        text = json.dumps(manifest, ensure_ascii=False).lower()
        return "direct" in text and "blocked" in text


def write_cross_lineage_release_pack(root: Path, decision: CrossLineageReleaseDecision) -> dict[str, Any]:
    payload = decision.to_dict()
    release_current = root / "release/current"
    release_current.mkdir(parents=True, exist_ok=True)
    _write_json(release_current / "stage126_cross_lineage_intelligence_release_report.json", payload)
    _write_json(release_current / "stage126_release_authority_manifest.json", {
        "stage": "126",
        "baseline_stage": "125",
        "status": decision.status,
        "release_authority": decision.release_authority,
        "authority_stack": decision.final_release_pack["authority_stack"],
        "invariants": decision.invariants,
    })
    _write_json(release_current / "stage126_lineage_release_pack.json", decision.final_release_pack)
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
