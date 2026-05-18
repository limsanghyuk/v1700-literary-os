from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def normalize_result(value: Any) -> dict[str, Any]:
    """Normalize CLI/MCP/fallback/cypher-like results into a stable dict shape.

    GitNexus is optional in this repository. Stage112 therefore treats every
    external tool response as untrusted until it is normalized into the same
    status/issues/data envelope used by release gates.
    """
    if isinstance(value, Mapping):
        data = dict(value)
        status = str(data.get("status", "pass")).lower()
        issues = data.get("issues", [])
        if isinstance(issues, str):
            issues = [issues]
        return {"status": "pass" if status in {"pass", "ok", "ready"} and not issues else status, "issues": list(issues), "data": data}
    if isinstance(value, (str, Path)):
        return {"status": "pass", "issues": [], "data": {"value": str(value)}}
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return {"status": "pass", "issues": [], "data": {"items": list(value)}}
    return {"status": "pass", "issues": [], "data": {"value": value}}


def normalize_tool_map(raw: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {name: normalize_result(result) for name, result in raw.items()}

