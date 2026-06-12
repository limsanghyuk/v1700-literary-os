#!/usr/bin/env python3
"""Writer IDE advisory panel renderer scaffold.

Builds a UI-facing render packet from the Option B Writer IDE static flow and
manual static review result. This produces only a render packet; it does not
open Page18 runtime, call providers, generate prose, write memory, mutate canon,
or update weights.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

RENDERER_VERSION = "0.1.0"
STATIC_FLOW_PATH = "fixtures/option_b_validation/writer_ide_static_flow_result.json"
MANUAL_REVIEW_PATH = "fixtures/option_b_validation/manual_static_review_result.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


class WriterIDEAdvisoryPanelRenderer:
    def __init__(self, repo_root: Path, static_flow_path: str = STATIC_FLOW_PATH, review_path: str = MANUAL_REVIEW_PATH) -> None:
        self.repo_root = repo_root
        self.static_flow_path = static_flow_path
        self.review_path = review_path
        self.blocking: List[Dict[str, str]] = []

    def build_packet(self) -> Dict[str, Any]:
        started = utc_now()
        static_flow = self._load_json(self.static_flow_path)
        review = self._load_json(self.review_path)
        if static_flow and review:
            self._validate_inputs(static_flow, review)
        cards = self._build_cards(static_flow, review) if not self.blocking else []
        return self._result(started, static_flow, review, cards)

    def _load_json(self, rel_path: str) -> Mapping[str, Any]:
        path = self.repo_root / rel_path
        if not path.exists():
            self._block(rel_path, "input file is missing")
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._block(rel_path, f"invalid JSON: {exc}")
            return {}
        if not isinstance(data, Mapping):
            self._block(rel_path, "input must be an object")
            return {}
        return data

    def _validate_inputs(self, static_flow: Mapping[str, Any], review: Mapping[str, Any]) -> None:
        expected = {
            STATIC_FLOW_PATH: {
                "overall_status": "PASS",
                "acceptance_status": "ACCEPTED_FOR_MANUAL_STATIC_REVIEW",
                "page18_status": "NOT_OPENED",
                "stage243_status": "NOT_CREATED",
            },
            MANUAL_REVIEW_PATH: {
                "overall_status": "PASS",
                "acceptance_status": "READY_FOR_HUMAN_REVIEW",
                "page18_status": "NOT_OPENED",
                "stage243_status": "NOT_CREATED",
            },
        }
        for path, checks in expected.items():
            payload = static_flow if path == STATIC_FLOW_PATH else review
            for key, value in checks.items():
                if payload.get(key) != value:
                    self._block(path, f"{key} must be {value}")
        if static_flow.get("panel_count") != review.get("review_object_count"):
            self._block(self.review_path, "panel_count and review_object_count mismatch")

    def _build_cards(self, static_flow: Mapping[str, Any], review: Mapping[str, Any]) -> List[Dict[str, Any]]:
        panels = as_list(static_flow.get("writer_ide_panels"))
        reviews = as_list(review.get("manual_review_objects"))
        review_by_panel = {obj.get("source_panel_id"): obj for obj in reviews if isinstance(obj, Mapping)}
        cards: List[Dict[str, Any]] = []
        for index, panel in enumerate(panels):
            if not isinstance(panel, Mapping):
                self._block(f"writer_ide_panels[{index}]", "panel is not an object")
                continue
            panel_id = panel.get("panel_id")
            review_object = review_by_panel.get(panel_id, {})
            if not review_object:
                self._block(str(panel_id), "matching manual review object is missing")
                continue
            cards.append(
                {
                    "card_id": f"render_card_{panel_id}",
                    "panel_id": panel_id,
                    "formula_signal_id": panel.get("formula_signal_id"),
                    "formula_name": panel.get("formula_name"),
                    "formula_group": panel.get("formula_group"),
                    "surface_label": panel.get("surface_label"),
                    "source_record_ids": panel.get("source_record_ids", []),
                    "source_record_types": panel.get("source_record_types", []),
                    "review_object_id": review_object.get("review_object_id"),
                    "manual_review_status": review_object.get("default_decision", "PENDING_REVIEW"),
                    "required_reviewer_role": review_object.get("required_reviewer_role"),
                    "allowed_decisions": review_object.get("allowed_decisions", []),
                    "ide_region": "advisory_panel",
                    "display_mode": "read_only_advisory",
                    "evidence_refs": [self.static_flow_path, self.review_path],
                }
            )
        return cards

    def _result(self, started: str, static_flow: Mapping[str, Any], review: Mapping[str, Any], cards: List[Dict[str, Any]]) -> Dict[str, Any]:
        completed = utc_now()
        blocked = bool(self.blocking)
        return {
            "render_packet_id": f"writer_ide_advisory_panel_render_packet_{completed}",
            "renderer_version": RENDERER_VERSION,
            "source_result_refs": {
                "static_flow": self.static_flow_path,
                "manual_review": self.review_path,
            },
            "overall_status": "BLOCKED" if blocked else "PASS",
            "acceptance_status": "BLOCKED" if blocked else "READY_FOR_UI_RENDER_PACKET_REVIEW",
            "panel_card_count": len(cards),
            "review_object_count": review.get("review_object_count"),
            "blocking_failure_count": len(self.blocking),
            "blocking_failures": self.blocking,
            "panel_cards": cards,
            "review_state_summary": {
                "manual_review_acceptance_status": review.get("acceptance_status"),
                "default_review_status": "PENDING_REVIEW",
            },
            "blocked_action_summary": ["provider_generation", "memory_write", "canon_mutation", "weight_update", "page18_runtime"],
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
    parser = argparse.ArgumentParser(description="Build Writer IDE advisory panel render packet.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--static-flow", default=STATIC_FLOW_PATH)
    parser.add_argument("--manual-review", default=MANUAL_REVIEW_PATH)
    parser.add_argument("--output", default="")
    args = parser.parse_args(argv)
    renderer = WriterIDEAdvisoryPanelRenderer(Path(args.repo_root).resolve(), args.static_flow, args.manual_review)
    result = renderer.build_packet()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
