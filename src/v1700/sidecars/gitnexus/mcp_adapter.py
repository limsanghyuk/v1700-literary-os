from __future__ import annotations


class GitNexusMcpAdapter:
    """Placeholder boundary for future MCP integration.

    Stage72.2 keeps release gates deterministic by using the CLI/Python fallback.
    MCP reads can be attached here later without changing GraphNexus contracts.
    """

    enabled = False

    def to_dict(self) -> dict:
        return {
            "provider": "gitnexus_mcp",
            "enabled": self.enabled,
            "reason": "deferred_to_preserve_provider_free_release_gates",
        }
