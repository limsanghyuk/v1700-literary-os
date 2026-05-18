from __future__ import annotations
from .contracts import Node2AuthorProfileBridge
from .style_genome import build_style_genome


def build_node2_author_profile_bridge(genome_payload: dict | None = None) -> dict:
    genome_payload = genome_payload or build_style_genome()
    bridge = Node2AuthorProfileBridge(
        status="pass",
        genome_id=genome_payload.get("genome_id", "style_genome_stage106_feature_only"),
        node2_profile_id="node2_surface_profile_stage106",
        allowed_surface_controls=("rhythm_hint", "sensory_density_hint", "dialogue_ratio_hint", "introspection_hint", "motion_hint"),
        forbidden_controls=("raw_reveal", "raw_manuscript_prompt", "provider_export", "verbatim_style_copy"),
        raw_reveal_access=0,
        provider_call_count=0,
    )
    payload = bridge.to_dict()
    payload.update({
        "stage": "106.3",
        "title": "Node2 Feature-only Author Profile Bridge",
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
    })
    return payload
