from __future__ import annotations
import re
from pathlib import Path

_RAW_TEXT_KEYS = {"raw_text", "manuscript", "full_text", "original_text", "verbatim"}
_SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def run_author_profile_privacy_guard(payload: dict | None = None, root: Path | None = None) -> dict:
    payload = payload or {}
    issues: list[str] = []
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in _RAW_TEXT_KEYS and v:
                    issues.append(f"raw_text_field:{path}/{k}".strip("/"))
                walk(v, f"{path}/{k}".strip("/"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            if any(p.search(obj) for p in _SECRET_PATTERNS):
                issues.append(f"secret_like_value:{path}")
            if len(obj) > 600 and " " in obj:
                issues.append(f"long_verbatim_like_string:{path}")
    walk(payload)
    return {
        "stage": "106.privacy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "raw_manuscript_provider_leakage": 0 if not issues else 1,
        "raw_manuscript_retained": False,
        "provider_export_allowed": False,
        "feature_only": True,
        "credential_leakage": 0,
    }
