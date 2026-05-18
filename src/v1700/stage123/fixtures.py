from __future__ import annotations

ASD_FIXTURE_GRAPH = {
    "secrets": [
        {"id": "secret_birth_record", "label": "Birth Record Secret", "severity": 0.42, "blast_ratio": 0.10},
    ],
    "reveals": [],
    "foreshadows": [
        {"id": "motif_red_scarf", "label": "Red Scarf Payoff", "resolved": False, "severity": 0.38, "blast_ratio": 0.08},
    ],
    "threads": [
        {"id": "thread_detective_partner", "label": "Detective Partner Thread", "abandoned": False},
    ],
    "characters": [
        {"id": "minjun", "label": "Minjun", "tracked": True, "episode_first": 1, "episode_last": 16},
        {"id": "sujin", "label": "Sujin", "tracked": True, "episode_first": 1, "episode_last": 16},
        {"id": "haewon", "label": "Haewon", "tracked": True, "episode_first": 2, "episode_last": 14},
    ],
    "relationships": [
        {"id": "rel_minjun_haewon", "label": "Minjun-Haewon", "character_id": "haewon", "post_death_edge": False, "contradiction_count": 0},
    ],
}

BLOCKING_ASD_GRAPH = {
    "secrets": [
        {"id": "secret_a", "label": "Secret A", "severity": 0.95, "blast_ratio": 0.70},
        {"id": "secret_b", "label": "Secret B", "severity": 0.90, "blast_ratio": 0.70},
    ],
    "reveals": [],
    "foreshadows": [
        {"id": "motif_a", "label": "Motif A", "resolved": False, "severity": 0.88, "blast_ratio": 0.60},
    ],
    "threads": [
        {"id": "thread_a", "label": "Thread A", "abandoned": True, "severity": 0.80, "blast_ratio": 0.50},
    ],
    "characters": [
        {"id": "ghost", "label": "Ghost", "tracked": False, "episode_first": 8, "episode_last": 2, "severity": 0.90},
    ],
    "relationships": [
        {"id": "rel_bad", "label": "Bad Relation", "character_id": "ghost", "post_death_edge": True, "contradiction_count": 3, "severity": 0.85},
    ],
}
