from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KNOWN_ACTIVE_VERSIONS = {
    "stage72", "stage72.1", "stage72.2", "stage72.3", "stage73", "stage73.1",
    "stage74", "stage75", "stage76", "stage77", "stage78", "stage79", "stage80",
    "stage81", "stage81.1", "stage82", "stage83", "stage83.1", "stage84", "stage85",
    "stage86", "stage87", "stage88", "stage89", "stage90", "stage91", "stage92",
    "stage93", "stage94", "stage95", "stage96", "stage97", "stage97.1", "stage97.2",
    "stage98", "stage99", "stage100", "stage101", "stage102", "stage103", "stage104",
    "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110",
    "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117",
    "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124",
    "stage125", "stage126", "stage127", "stage128", "stage129", "stage130", "stage131",
    "stage132", "stage133", "stage134",
}

STAGE_REQUIRED_GATES = {
    "stage112": ["stage112_gitnexus_nie_preflight", "stage112_release_gate"],
    "stage113": ["stage113_physics_reward_bridge", "stage113_release_gate"],
    "stage114": ["stage114_adaptive_momentum_weights", "stage114_release_gate"],
    "stage115": ["stage115_character_influence_matrix", "stage115_release_gate"],
    "stage116": ["stage116_domain_rag_fusion", "stage116_release_gate"],
    "stage117": ["stage117_narrative_tension_curve", "stage117_release_gate"],
    "stage118": ["stage118_nil_orchestrator", "stage118_release_gate"],
    "stage119": ["stage119_nie_adversarial_regression", "stage119_release_gate"],
    "stage120": ["stage120_gate25_nie_v1", "stage120_release_gate"],
    "stage121": ["stage121_cross_lineage_preflight", "stage121_release_gate"],
    "stage122": ["stage122_nie_v2_stability_absorption", "stage122_release_gate"],
    "stage123": ["stage123_asd_gate28_absorption", "stage123_release_gate"],
    "stage124": ["stage124_pne_gate29_absorption", "stage124_release_gate"],
    "stage125": ["stage125_gate25_28_29_governor", "stage125_release_gate"],
    "stage126": ["stage126_cross_lineage_release", "stage126_release_gate"],
    "stage127": ["stage127_multiwork_preflight", "stage127_release_gate"],
    "stage128": ["stage128_read_only_absorption", "stage128_release_gate"],
    "stage129": ["stage129_multiwork_cim_governor", "stage129_release_gate"],
    "stage130": ["stage130_multiwork_release", "stage130_release_gate"],
    "stage131": ["stage131_gig_advisory", "stage131_release_gate"],
    "stage132": ["stage132_contradiction_classifier", "stage132_release_gate"],
    "stage133": ["stage133_narrative_state_tensor", "stage133_release_gate"],
    "stage134": ["stage134_meta_learner_audit", "stage134_release_gate"],
}

STAGE_REQUIRED_FILES = {
    "stage127": [
        "manifests/stage127_manifest.json",
        "manifests/stage127_multiwork_preflight_manifest.json",
        "manifests/stage127_branchpoint_trace_manifest.json",
        "docs/stages/stage127.md",
        "release/current/stage127_multiwork_preflight_report.json",
        "release/current/stage127_release_gate_report.json",
    ],
    "stage128": [
        "manifests/stage128_manifest.json",
        "manifests/stage128_read_only_absorption_manifest.json",
        "manifests/stage128_branchpoint_trace_manifest.json",
        "docs/stages/stage128.md",
        "release/current/stage128_read_only_absorption_report.json",
        "release/current/stage128_release_gate_report.json",
    ],
    "stage129": [
        "manifests/stage129_manifest.json",
        "manifests/stage129_multiwork_cim_governor_manifest.json",
        "manifests/stage129_branchpoint_trace_manifest.json",
        "docs/stages/stage129.md",
        "docs/architecture/stage129_blueprint.md",
        "docs/proposals/stage129_proposal.md",
        "release/current/stage129_multiwork_cim_governor_report.json",
        "release/current/stage129_release_gate_report.json",
    ],
    "stage130": [
        "manifests/stage130_manifest.json",
        "manifests/stage130_multiwork_release_manifest.json",
        "manifests/stage130_branchpoint_trace_manifest.json",
        "docs/stages/stage130.md",
        "docs/architecture/stage130_blueprint.md",
        "docs/proposals/stage130_proposal.md",
        "release/current/stage130_multiwork_release_report.json",
        "release/current/stage130_release_gate_report.json",
    ],
    "stage131": [
        "manifests/stage131_manifest.json",
        "manifests/stage131_gig_advisory_manifest.json",
        "manifests/stage131_branchpoint_trace_manifest.json",
        "docs/stages/stage131.md",
        "docs/architecture/stage131_blueprint.md",
        "docs/proposals/stage131_proposal.md",
        "docs/roadmaps/stage131_roadmap.md",
        "release/current/stage131_gig_advisory_report.json",
        "release/current/stage131_release_gate_report.json",
    ],
    "stage132": [
        "manifests/stage132_manifest.json",
        "manifests/stage132_contradiction_classifier_manifest.json",
        "manifests/stage132_branchpoint_trace_manifest.json",
        "docs/stages/stage132.md",
        "docs/architecture/stage132_blueprint.md",
        "docs/proposals/stage132_proposal.md",
        "docs/roadmaps/stage132_roadmap.md",
        "release/current/stage132_contradiction_classifier_report.json",
        "release/current/stage132_release_gate_report.json",
    ],
    "stage133": [
        "manifests/stage133_manifest.json",
        "manifests/stage133_narrative_state_tensor_manifest.json",
        "manifests/stage133_branchpoint_trace_manifest.json",
        "docs/stages/stage133.md",
        "docs/architecture/stage133_blueprint.md",
        "docs/proposals/stage133_proposal.md",
        "docs/roadmaps/stage133_roadmap.md",
        "release/current/stage133_narrative_state_tensor_report.json",
        "release/current/stage133_release_gate_report.json",
    ],
    "stage134": [
        "manifests/stage134_manifest.json",
        "manifests/stage134_meta_learner_audit_manifest.json",
        "manifests/stage134_branchpoint_trace_manifest.json",
        "docs/stages/stage134.md",
        "docs/architecture/stage134_blueprint.md",
        "docs/proposals/stage134_proposal.md",
        "docs/roadmaps/stage134_roadmap.md",
        "release/current/stage134_meta_learner_audit_report.json",
        "release/current/stage134_release_gate_report.json",
    ],
}

PREDECESSOR_GATE = {
    "stage113": "stage112_release_gate",
    "stage114": "stage113_release_gate",
    "stage115": "stage114_release_gate",
    "stage116": "stage115_release_gate",
    "stage117": "stage116_release_gate",
    "stage118": "stage117_release_gate",
    "stage119": "stage118_release_gate",
    "stage120": "stage119_release_gate",
    "stage121": "stage120_release_gate",
    "stage122": "stage121_release_gate",
    "stage123": "stage122_release_gate",
    "stage124": "stage123_release_gate",
    "stage125": "stage124_release_gate",
    "stage126": "stage125_release_gate",
    "stage127": "stage126_release_gate",
    "stage128": "stage127_release_gate",
    "stage129": "stage128_release_gate",
    "stage130": "stage129_release_gate",
    "stage131": "stage130_release_gate",
    "stage132": "stage131_release_gate",
    "stage133": "stage132_release_gate",
    "stage134": "stage133_release_gate",
}


def main() -> int:
    issues: list[str] = []
    required = [
        "src/v1700/cli.py",
        "src/v1700/nodes/node2_prose_renderer/compiler.py",
        "manifests/live_core_manifest.json",
        "manifests/stage_lineage_manifest.json",
        "docs/stages/STAGE_INDEX.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            issues.append(f"missing:{rel}")
    root_py = [p.name for p in ROOT.glob("*.py")]
    if root_py:
        issues.append(f"root_python_files_present:{root_py}")

    manifest = json.loads((ROOT / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    active = manifest.get("active_version")
    gates = set(manifest.get("active_gates", []))
    if active not in KNOWN_ACTIVE_VERSIONS:
        issues.append("live_core_manifest_active_version_unknown")

    for gate in STAGE_REQUIRED_GATES.get(active, []):
        if gate not in gates:
            issues.append(f"{gate}_missing")

    predecessor_gate = PREDECESSOR_GATE.get(active)
    if predecessor_gate and predecessor_gate not in gates:
        issues.append(f"{predecessor_gate}_missing")

    for rel in STAGE_REQUIRED_FILES.get(active, []):
        if not (ROOT / rel).exists():
            issues.append(f"missing:{rel}")

    result = {"status": "pass" if not issues else "blocked", "active_version": active, "root_python_files": root_py, "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
