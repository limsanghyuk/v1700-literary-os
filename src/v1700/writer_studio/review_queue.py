from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ReviewQueueItem:
    item_id: str
    source_event_id: str
    panel_id: str
    severity: str
    category: str
    status: str
    summary: str
    branchpoint_refs: tuple[str, ...]
    resolution_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "source_event_id": self.source_event_id,
            "panel_id": self.panel_id,
            "severity": self.severity,
            "category": self.category,
            "status": self.status,
            "summary": self.summary,
            "branchpoint_refs": list(self.branchpoint_refs),
            "resolution_note": self.resolution_note,
        }


@dataclass(frozen=True)
class ReviewQueueReport:
    stage: str
    status: str
    total_items: int
    pending_count: int
    approved_count: int
    needs_changes_count: int
    resolved_count: int
    blocking_count: int
    items: tuple[ReviewQueueItem, ...]
    provider_default_calls: int = 0
    node2_raw_reveal_access_count: int = 0
    issues: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "total_items": self.total_items,
            "pending_count": self.pending_count,
            "approved_count": self.approved_count,
            "needs_changes_count": self.needs_changes_count,
            "resolved_count": self.resolved_count,
            "blocking_count": self.blocking_count,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
            "items": [item.to_dict() for item in self.items],
        }


class StudioReviewQueue:
    """Deterministic review queue for Studio UI changes.

    The queue treats UI edits as auditable branchpoint-impact events. It is not a
    collaboration backend; it is a local gateable state machine that can later be
    wired into a real Studio front end.
    """

    def __init__(self) -> None:
        self._items: list[ReviewQueueItem] = []

    @property
    def items(self) -> tuple[ReviewQueueItem, ...]:
        return tuple(self._items)

    def add_item(
        self,
        *,
        source_event_id: str,
        panel_id: str,
        severity: str,
        category: str,
        summary: str,
        branchpoint_refs: tuple[str, ...],
    ) -> ReviewQueueItem:
        item = ReviewQueueItem(
            item_id=f"RQ{len(self._items) + 1:03d}",
            source_event_id=source_event_id,
            panel_id=panel_id,
            severity=severity,
            category=category,
            status="pending",
            summary=summary,
            branchpoint_refs=branchpoint_refs,
        )
        self._items.append(item)
        return item

    def transition(self, item_id: str, *, status: str, note: str) -> ReviewQueueItem:
        allowed = {"pending", "approved", "needs_changes", "resolved"}
        if status not in allowed:
            raise ValueError(f"unsupported_review_status:{status}")
        for index, item in enumerate(self._items):
            if item.item_id == item_id:
                updated = ReviewQueueItem(
                    item_id=item.item_id,
                    source_event_id=item.source_event_id,
                    panel_id=item.panel_id,
                    severity=item.severity,
                    category=item.category,
                    status=status,
                    summary=item.summary,
                    branchpoint_refs=item.branchpoint_refs,
                    resolution_note=note,
                )
                self._items[index] = updated
                return updated
        raise KeyError(item_id)

    def report(self) -> ReviewQueueReport:
        pending = sum(1 for item in self._items if item.status == "pending")
        approved = sum(1 for item in self._items if item.status == "approved")
        needs_changes = sum(1 for item in self._items if item.status == "needs_changes")
        resolved = sum(1 for item in self._items if item.status == "resolved")
        blocking = sum(1 for item in self._items if item.severity == "blocking" and item.status not in {"approved", "resolved"})
        issues: list[str] = []
        if len(self._items) < 6:
            issues.append("stage91_review_queue_minimum_6_items_not_met")
        if blocking:
            issues.append("stage91_blocking_review_items_unresolved")
        if not any(item.category == "branchpoint_impact" for item in self._items):
            issues.append("stage91_branchpoint_review_item_missing")
        return ReviewQueueReport(
            stage="91",
            status="pass" if not issues else "blocked",
            total_items=len(self._items),
            pending_count=pending,
            approved_count=approved,
            needs_changes_count=needs_changes,
            resolved_count=resolved,
            blocking_count=blocking,
            items=tuple(self._items),
            issues=tuple(issues),
        )
