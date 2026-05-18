from __future__ import annotations

MAE_AGENT_WEIGHTS = {
    "reader": 0.35,
    "writer": 0.25,
    "editor": 0.25,
    "cultural": 0.15,
}

AGENT_RELIABILITY = {
    "reader": 0.72,
    "writer": 0.64,
    "editor": 0.68,
    "cultural": 0.58,
}

# A deterministic 8-scene actual tension curve close to Stage117 ideal evidence.
ACTUAL_TENSION_VALUES = [0.42, 0.47, 0.61, 0.70, 0.79, 0.82, 0.61, 0.54]

TEMPORAL_ROLE_TIERS = [
    {"minjun": "jang", "sujin": "jang", "haewon": "po", "chairman": "jol", "detective": "jol"},
    {"minjun": "jang", "sujin": "jang", "haewon": "po", "chairman": "jol", "detective": "ma_sang"},
    {"minjun": "jang", "sujin": "jang", "haewon": "po", "chairman": "jol", "detective": "ma_sang"},
]

TEMPORAL_CIM_VOLATILITY = [0.08, 0.11, 0.12]

META_LEARNER_PROPOSALS = [
    {"proposal_id": "ML-001", "target": "t_ideal.base", "mode": "proposal_only"},
    {"proposal_id": "ML-002", "target": "agent_weights.reader", "mode": "proposal_only"},
    {"proposal_id": "ML-003", "target": "temporal_cim.volatility_guard", "mode": "proposal_only"},
]
