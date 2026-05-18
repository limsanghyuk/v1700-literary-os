from __future__ import annotations
import hashlib

def seed_aware_fixture(seed: str, mode: str = "DRAMA") -> dict:
    digest = hashlib.sha256(f"{mode}:{seed}".encode("utf-8")).hexdigest()
    return {
        "fixture_id": f"stage111_{digest[:12]}",
        "mode": mode,
        "response_sha256": digest,
        "response_excerpt": f"[{mode}] fixture scene candidate {digest[:8]}",
        "raw_response_stored": False,
    }
