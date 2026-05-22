from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_project_sources(root: Path) -> dict[str, Any]:
    sample_root = root / "samples" / "korean_drama_family_secret"
    project = _read_json(sample_root / "project.json")
    characters = _read_json(sample_root / "characters.json")
    world = _read_json(sample_root / "world.json")
    scene = _read_json(sample_root / "scene_requests" / "scene_001.json")
    plot_outline = (sample_root / "plot_outline.md").read_text(encoding="utf-8")
    return {
        "sample_root": sample_root.as_posix(),
        "project": project,
        "characters": characters,
        "world": world,
        "scene": scene,
        "plot_outline": plot_outline,
    }


def build_project_manifest_bundle(root: Path) -> dict[str, Any]:
    sources = load_project_sources(root)
    project = sources["project"]
    characters = sources["characters"]
    world = sources["world"]
    scene = sources["scene"]
    project_id = str(project["project_id"])
    scene_id = str(scene["scene_id"])
    episode_id = "episode_001"

    series_state = {
        "series_id": project_id,
        "title": project["title"],
        "format": project.get("genre", "longform_drama"),
        "theme_brief": project.get("purpose", "Synthetic local-only longform sample."),
        "episode_order": [episode_id],
        "timeline_anchor": "synthetic_modern_seoul_present_day",
    }
    episode_state = {
        "episode_id": episode_id,
        "series_id": project_id,
        "order_index": 1,
        "premise": scene["objective"],
        "scene_order": [scene_id],
        "continuity_anchor": "family_inheritance_question_open",
    }
    scene_state = {
        "scene_id": scene_id,
        "episode_id": episode_id,
        "location_id": world["world_id"],
        "participants": list(scene["characters"]),
        "objective": scene["objective"],
        "surface_constraints": [
            "synthetic_only",
            "public_safe_placeholder",
            "provider_calls_allowed_false",
            "raw_manuscript_included_false",
            "final_secret_not_revealed",
        ],
    }
    character_state = {
        "characters": [
            {
                "character_id": item["character_id"],
                "display_name": item["name"],
                "role": item["role"],
                "goal_vector": _goal_vector(item["role"]),
                "relationship_edges": _relationship_edges(item["character_id"]),
                "knowledge_boundary": "surface_only_until_reveal_contract",
            }
            for item in characters.get("characters", [])
        ]
    }
    world_state = {
        "world_id": world["world_id"],
        "era": "modern_day",
        "locations": [
            {"location_id": "family_estate", "label": "Family Estate", "public_safe": True},
            {"location_id": "legal_office", "label": "Small Legal Office", "public_safe": True},
        ],
        "institutions": [
            {"institution_id": "han_family", "type": "family", "public_safe": True},
            {"institution_id": "inheritance_law_office", "type": "legal", "public_safe": True},
        ],
        "rule_constraints": [
            "synthetic_only",
            "sample_local_only",
            "provider_calls_allowed_false",
            "raw_manuscript_included_false",
        ],
        "public_facts": [
            world["setting"],
            "A family inheritance dispute drives the opening tension.",
            "The final secret remains hidden from reader-facing output.",
        ],
    }
    reveal_state = {
        "reveal_id": "inheritance_secret_core",
        "owner_scope": episode_id,
        "visibility_level": "hidden",
        "knowledge_holders": ["critic_lane_only", "human_approval_lane_only"],
        "unlock_condition": "manual approval after future gate progression",
        "node2_surface_projection": "A mystery exists, but the final secret is withheld.",
    }
    continuity_state = {
        "continuity_id": "continuity_episode_001",
        "timeline_position": "episode_001_scene_001_opening",
        "open_threads": [
            "Who inherits the estate?",
            "Why did the estranged aunt return now?",
        ],
        "resolved_threads": [],
        "contradiction_watchlist": [
            "Do not reveal the final secret in Stage147 manifest packets.",
            "Keep all scene packets synthetic and provider-zero.",
        ],
        "repair_policy": "manual_only_human_approval_required",
    }
    return {
        "series_state": series_state,
        "episode_state": episode_state,
        "scene_state": scene_state,
        "character_state": character_state,
        "world_state": world_state,
        "reveal_state": reveal_state,
        "continuity_state": continuity_state,
        "source_summary": {
            "sample_root": sources["sample_root"],
            "project_id": project_id,
            "character_count": len(character_state["characters"]),
            "scene_count": 1,
            "episode_count": 1,
            "plot_outline_excerpt": _plot_outline_excerpt(sources["plot_outline"]),
        },
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _plot_outline_excerpt(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _goal_vector(role: str) -> list[str]:
    lookup = {
        "eldest_daughter": ["protect_family", "learn_truth", "keep_surface_composure"],
        "family_lawyer": ["manage_inheritance_process", "contain_public_risk"],
        "estranged_aunt": ["reenter_family", "pressure_hidden_history"],
    }
    return lookup.get(role, ["maintain_surface_stability"])


def _relationship_edges(character_id: str) -> list[dict[str, str]]:
    mapping = {
        "han_sera": [
            {"target": "kim_doyun", "relation": "trusts_as_legal_ally"},
            {"target": "yoon_mira", "relation": "uncertain_family_tension"},
        ],
        "kim_doyun": [
            {"target": "han_sera", "relation": "professional_confidant"},
            {"target": "yoon_mira", "relation": "legal_caution"},
        ],
        "yoon_mira": [
            {"target": "han_sera", "relation": "estranged_aunt_niece"},
            {"target": "kim_doyun", "relation": "wary_observer"},
        ],
    }
    return mapping.get(character_id, [])
