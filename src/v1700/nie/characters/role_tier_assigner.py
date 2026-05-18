from __future__ import annotations

from v1700.nie.characters.contracts import RoleTier


def assign_role_tiers(pagerank: dict[str, float], betweenness: dict[str, float]) -> dict[str, RoleTier]:
    """Assign Korean janggi-style narrative roles from observed centrality.

    PageRank is normalized against the strongest character for role assignment so
    multi-character casts can still expose a single 장(將) without requiring a raw
    probability greater than 0.80. This preserves the blueprint semantics while
    keeping scores comparable across cast sizes.
    """
    if not pagerank:
        return {}
    max_pr = max(pagerank.values()) or 1.0
    tiers: dict[str, RoleTier] = {}
    for char, pr in pagerank.items():
        rel_pr = pr / max_pr if max_pr else 0.0
        bc = betweenness.get(char, 0.0)
        if rel_pr >= 0.80:
            tier: RoleTier = "jang"
        elif rel_pr >= 0.60:
            tier = "cha"
        elif bc >= 0.70:
            tier = "po"
        elif rel_pr >= 0.30 or bc >= 0.40:
            tier = "ma_sang"
        else:
            tier = "jol"
        tiers[char] = tier
    return tiers
