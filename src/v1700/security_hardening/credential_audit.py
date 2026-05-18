from __future__ import annotations

import re
from pathlib import Path

SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def audit_credentials(root: Path) -> dict:
    hits: list[str] = []
    for base in ("src", "tools", "manifests"):
        base_path = root / base
        if not base_path.exists():
            continue
        for path in base_path.rglob("*"):
            if not path.is_file() or _ignored(path):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern.search(text) for pattern in SECRET_PATTERNS):
                hits.append(path.relative_to(root).as_posix())
    return {"status": "pass" if not hits else "blocked", "credential_leakage": len(hits), "hits": hits}


def _ignored(path: Path) -> bool:
    return any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts) or path.suffix in {".pyc", ".zip"}
