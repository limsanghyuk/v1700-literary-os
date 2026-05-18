from __future__ import annotations

import hashlib

from .contracts import VaultProbeResult


def run_local_manuscript_vault_probe(sample_text: str | None = None) -> dict:
    text = sample_text or "local manuscript sample kept inside the vault"
    features = {
        "length_bucket": str(min(len(text) // 50, 10)),
        "sentence_count_bucket": str(max(1, text.count(".") + text.count("!") + text.count("?"))),
        "language_hint": "ko_or_mixed",
        "style_feature_mode": "feature_only",
    }
    fingerprint = hashlib.sha256("|".join(f"{key}:{value}" for key, value in sorted(features.items())).encode("utf-8")).hexdigest()
    result = VaultProbeResult(
        status="pass",
        vault_mode="LOCAL_ONLY",
        raw_text_exported=False,
        provider_export_allowed=False,
        feature_fingerprint=fingerprint,
        stored_feature_keys=tuple(sorted(features)),
        issues=(),
    )
    return result.to_dict()
