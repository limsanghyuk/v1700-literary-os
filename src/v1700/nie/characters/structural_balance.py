from __future__ import annotations

from v1700.nie.characters.contracts import TriangleTension, sign


def compute_triangle_tension(a: str, b: str, c: str, w_ab: float, w_bc: float, w_ca: float) -> TriangleTension:
    """Compute directed structural balance for an ordered character triangle.

    Stage115 keeps the NIE character model deterministic and auditable. Zero
    edges are treated as unresolved imbalance, because a missing relation cannot
    support a stable dramatic triangle.
    """
    signs = (sign(w_ab), sign(w_bc), sign(w_ca))
    balance = 0 if 0 in signs else signs[0] * signs[1] * signs[2]
    tension = 2 if balance <= 0 else 0
    return TriangleTension(a=a, b=b, c=c, w_ab=round(w_ab, 6), w_bc=round(w_bc, 6), w_ca=round(w_ca, 6), balance=balance, tension=tension)
