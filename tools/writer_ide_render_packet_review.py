#!/usr/bin/env python3
"""Writer IDE render packet review scaffold.

Reviews the UI-facing advisory panel render packet for structural consistency and
boundary preservation. This does not open Page18 runtime.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

REVIEW_VERSION = "0.1.0"
DEFAULT_PACKET = "fixtures/option_b_validation/writer_ide_advisory_panel_render_packet.json"
REQUIRED_BLOCKED_ACTIONS = {
    "provider_generation",
    "memory_write",
    "canon_mutation",
    "weight_update",
    "page18_runtime",
}
REQUIRED_CARD_FIELDS = {
    "card_id",
    "panel_id",
    "formula_signal_id",
    "formula_name",
    "formula_group",
    "surface_label",
    "review_object_id",
    "manual_review_status",
    "ide_region",
    "display_mode",
    "evidence_refs",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


class WriterIDERenderPacketReview:
    def __init__(self, repo_root: Path, packet_path: str = DEFAULT_PACKET) -> None:
        self.repo_root = repo_root
        self.packet_path = packet_path
        self.blocking: List[Dict[str, str]] = []
        self.warnings: List[Dict[str, str]] = []

    def review(self) -> Dict[str, Any]:
        started = utc_now()
        packet = self._load_packet()
        if packet:
            self._review_packet(packet)
        return self._result(started, packet)

    def _load_packet(self) -> Mapping[str, Any]:
        path = self.repo_root / self.packet_path
        if not path.exists():
            self._block(self.packet_path, "render packet is missing")
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._block(self.packet_path, f"invalid JSON: {exc}")
            return {}
        if not isinstance(data, Mapping):
            self._block(self.packet_path, "render packet must be an object")
            return {}
        return data

    def _review_packet(self, packet: Mapping[str, Any]) -> None:
        expected = {
            "overall_status": "PASS",
            "acceptance_status": "READY_FOR_UI_RENDER_PACKET_REVIEW",
            "page18_status": "NOT_OPENED",
            "stage243_status": "NOT_CREATED",
            "provider_status": "DISABLED",
            "generation_status": "DISABLED",
            "memory_write_status": "DISABLED",
            "canonical_mutation_status": "NO_CANONICAL_MUTATION",
        }
        for key, value in expected.items():
            if packet.get(key) != value:
                self._block(self.packet_path, f"{key} must be {value}")

        blocked_actions = set(as_list(packet.get("blocked_action_summary")))
        missing_actions = REQUIRED_BLOCKED_ACTIONS - blocked_actions
        if missing_actions:
            self._block(self.packet_path, f"blocked_action_summary missing: {sorted(missing_actions)}")

        cards = as_list(packet.get("panel_cards"))
        if not cards:
            self._block(self.packet_path, "panel_cards is empty")
            return
        if packet.get("panel_card_count") != len(cards):
            self._block(self.packet_path, "panel_card_count does not match panel_cards length")
        if packet.get("review_object_count") != len(cards):
            self._block(self.packet_path, "review_object_count does not match panel_cards length")

        seen_card_ids = set()
        for index, card in enumerate(cards):
            card_path = f"panel_cards[{index}]"
            if not isinstance(card, Mapping):
                self._block(card_path, "card must be an object")
                continue
            missing = [field for field in REQUIRED_CARD_FIELDS if field not in card]
            if missing:
                self._block(card_path, f"missing card fields: {missing}")
            card_id = card.get("card_id")
            if card_id in seen_card_ids:
                self._block(card_path, f"duplicate card_id: {card_id}")
            seen_card_ids.add(card_id)
            if card.get("manual_review_status") != "PENDING_REVIEW":
                self._block(card_path, "manual_review_status must remain PENDING_REVIEW")
            if card.get("display_mode") != "read_only_advisory":
                self._block(card_path, "display_mode must be read_only_advisory")
            if card.get("ide_region") != "advisory_panel":
                self._block(card_path, "ide_region must be advisory_panel")
            if len(as_list(card.get("evidence_refs"))) < 2:
                self._block(card_path, "card must include evidence refs")

    def _result(self, started: str, packet: Mapping[str, Any]) -> Dict[str, Any]:
        completed = utc_now()
        overall = "BLOCKED" if self.blocking else "PASS"
        return {
            "result_id": f"writer_ide_render_packet_review_result_{completed}",
            "review_version": REVIEW_VERSION,
            "packet_ref": self.packet_path,
            "packet_status": packet.get("overall_status"),
            "overall_status": overall,
            "acceptance_status": "BLOCKED" if self.blocking else "READY_FOR_FRONTEND_RENDERER_BLUEPRINT",
            "panel_card_count": packet.get("panel_card_count", 0),
            "blocking_failure_count": len(self.blocking),
            "warning_count": len(self.warnings),
            "blocking_failures": self.blocking,
            "warnings": self.warnings,
            "page18_status": "NOT_OPENED",
            "stage243_status": "NOT_CREATED",
            "provider_status": "DISABLED",
            "generation_status": "DISABLED",
            "memory_write_status": "DISABLED",
            "canonical_mutation_status": "NO_CANONICAL_MUTATION",
            "created_at": completed,
            "validation_started_at": started,
            "validation_completed_at": completed,
        }

    def _block(self, path: str, message: str) -> None:
        self.blocking.append({"severity": "BLOCKING", "path": path, "message": message})


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Review Writer IDE advisory panel render packet.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--packet", default=DEFAULT_PACKET)
    parser.add_argument("--output", default="")
    args = parser.parse_args(argv)
    review = WriterIDERenderPacketReview(Path(args.repo_root).resolve(), args.packet)
    result = review.review()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
