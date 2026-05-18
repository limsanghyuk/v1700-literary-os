from __future__ import annotations

from pathlib import Path

from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest


def run_symbol_to_branchpoint_trace_gate(root: Path | None = None) -> dict:
    manifest = build_symbol_to_branchpoint_trace_manifest(root)
    issues = list(manifest.get("issues", []))
    return {
        "stage": "85",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "symbol_to_branchpoint_trace_manifest": manifest,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }

