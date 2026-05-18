from __future__ import annotations

from collections.abc import Mapping

from v1700.nie.asd.contracts import DebtItem, NarrativeDebtReport


class NarrativeDebtDetector:
    """V545 ASD narrative debt concept absorbed as deterministic analysis.

    This adapter deliberately uses simple serializable graph snapshots instead
    of importing the V545 runtime graph store. It never calls providers and does
    not mutate narrative state.
    """

    SECRET_SEVERITY = 0.45
    FORESHADOW_SEVERITY = 0.50
    THREAD_SEVERITY = 0.35

    def detect(self, graph: Mapping) -> NarrativeDebtReport:
        items: list[DebtItem] = []
        secrets = graph.get("secrets", [])
        reveals = set(graph.get("reveals", []))
        foreshadows = graph.get("foreshadows", [])
        threads = graph.get("threads", [])
        for secret in secrets:
            secret_id = str(secret.get("id"))
            if secret_id not in reveals:
                items.append(DebtItem(
                    debt_id=f"D-{len(items)+1:03d}",
                    debt_type="unresolved_secret",
                    node_id=secret_id,
                    label=str(secret.get("label", secret_id)),
                    severity=float(secret.get("severity", self.SECRET_SEVERITY)),
                    blast_ratio=float(secret.get("blast_ratio", 0.0)),
                ))
        for f in foreshadows:
            if not f.get("resolved", False):
                items.append(DebtItem(
                    debt_id=f"D-{len(items)+1:03d}",
                    debt_type="broken_foreshadow",
                    node_id=str(f.get("id")),
                    label=str(f.get("label", f.get("id"))),
                    severity=float(f.get("severity", self.FORESHADOW_SEVERITY)),
                    blast_ratio=float(f.get("blast_ratio", 0.0)),
                    related_ids=tuple(map(str, f.get("related_ids", ()))),
                ))
        for t in threads:
            if t.get("abandoned", False):
                items.append(DebtItem(
                    debt_id=f"D-{len(items)+1:03d}",
                    debt_type="abandoned_thread",
                    node_id=str(t.get("id")),
                    label=str(t.get("label", t.get("id"))),
                    severity=float(t.get("severity", self.THREAD_SEVERITY)),
                    blast_ratio=float(t.get("blast_ratio", 0.0)),
                    related_ids=tuple(map(str, t.get("related_ids", ()))),
                ))
        score = sum(item.severity for item in items) / max(1, len(items))
        status = "pass" if score <= 0.50 else "warn"
        return NarrativeDebtReport(status=status, items=tuple(items), overall_debt_score=score)
