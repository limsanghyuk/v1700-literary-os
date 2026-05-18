from __future__ import annotations

from typing import Any


def shared_character_allowed(*, same_owner: bool, explicit_license_edge: bool, public_domain_flag: bool) -> bool:
    return bool(same_owner or explicit_license_edge or public_domain_flag)


def run_shared_character_audit() -> dict[str, Any]:
    fixtures = [
        {"character_id": "char_alpha_mentor", "same_owner": True, "explicit_license_edge": False, "public_domain_flag": False},
        {"character_id": "char_beta_guest", "same_owner": False, "explicit_license_edge": True, "public_domain_flag": False},
        {"character_id": "blocked_private_character", "same_owner": False, "explicit_license_edge": False, "public_domain_flag": False},
    ]
    allowed = []
    blocked = []
    for item in fixtures:
        ok = shared_character_allowed(
            same_owner=item["same_owner"],
            explicit_license_edge=item["explicit_license_edge"],
            public_domain_flag=item["public_domain_flag"],
        )
        payload = {**item, "shared_character_allowed": ok}
        (allowed if ok else blocked).append(payload)
    # Stage127 passes if blocked private character remains blocked and no unauthorized reuse is allowed.
    unauthorized_allowed = [x for x in allowed if x["character_id"].startswith("blocked_")]
    return {
        "status": "pass" if not unauthorized_allowed and blocked else "blocked",
        "allowed": allowed,
        "blocked": blocked,
        "shared_character_conflicts": len(unauthorized_allowed),
        "license_edge_required_for_cross_owner_private_character": True,
    }
