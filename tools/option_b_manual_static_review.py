#!/usr/bin/env python3
"""Option B manual static review scaffold.

Consumes writer_ide_static_flow_result.json and emits a review packet. This is
not Page18 implementation and does not approve generation, memory write, canon
mutation, Value Proof, or coefficient updates.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

REVIEW_VERSION = "0.1.0"
DEFAULT_INPUT = "fixtures/option_b_validation/writer_ide_static_flow_result.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


class OptionBManualStaticReview:
    def __init__(self, repo_root: Path, input_path: str = DEFAULT_INPUT) -> None:
        self.repo_root = repo_root
        self.input_path = input_path
        self.blocking: List[Dict[str, str]] = []

    def build_review(self) -> Dict[str, Any]:
        started = utc_now()
        payload = self._load()
        if payload:
            self._validate_gate(payload)
        objects = self._build_review_objects(payload) if not self.blocking else []
        return self._result(started, payload, objects)

    def _load(self) -> Mapping[str, Any]:
        path = self.repo_root / self.input_path
        if not path.exists():
            self._block(self.input_path, "static flow result is missing")
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._block(self.input_path, f"invalid JSON: {exc}")
            return {}
        if not isinstance(data, Mapping):
            self._block(self.input_path, "expected JSON object")
            return {}
        return data

    def _validate_gate(self, payload: Mapping[str, Any]) -> None:
        checks = {
            "overall_status": "PASS",
            "acceptance_status": "ACCEPTED_FOR_MANUAL_STATIC_REVIEW",
            "provider_status": "DISABLED",
            "generation_status": "DISABLED",
            "memory_write_status": "DISABLED",
            "canonical_mutation_status": "NO_CANONICAL_MUTATION",
            "page18_status": "NOT_OPENED",
            "stage243_status": "NOT_CREATED",
        }
        for key, expected in checks.items():
            if payload.get(key) != expected:
                self._block(self.input_path, f"{key} must be {expected}")
        if payload.get("blocking_failure_count") != 0:
            self._block(self.input_path, "static flow has blocking failures")

    def _build_review_objects(self, payload: Mapping[str, Any]) -> List[Dict[str, Any]]:
        panels = as_list(payload.get("writer_ide_panels"))
        if not panels:
            self._block(self.input_path, "writer_ide_panels is empty")
            return []
        review_objects: List[Dict[str, Any]] = []
        for index, panel in enumerate(panels):
            if not isinstance(panel, Mapping):
                self._block(f"writer_ide_panels[{index}]", "panel is not an object")
                continue
            if panel.get("advisory_only") is not True:
                self._block(str(panel.get("panel_id", index)), "panel must remain advisory only")
                continue
            review_objects.append(
                {
                    "review_object_id": f"manual_review_{panel.get('panel_id', index)}",
                    "source_panel_id": panel.get("panel_id"),
                    "formula_signal_id": panel.get("formula_signal_id"),
                    "surface_label": panel.get("surface_label"),
                    "review_type": "HUMAN_STATIC_ADVISORY_REVIEW",
                    "required_reviewer_role": "writer_or_editor",
                    "default_decision": "PENDING_REVIEW",
                    "allowed_decisions": ["ACCEPT_AS_ADVISORY", "REQUEST_REVISION", "REJECT_ADVISORY"],
                    "forbidden_outcomes": ["AUTO_GENERATE", "AUTO_MUTATE_CANON", "AUTO_UPDATE_WEIGHTS"],
                    "manual_review_required": True,
                    "advisory_only": True,
                }
            )
        return review_objects

    def _result(self, started: str, payload: Mapping[str, Any], objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        completed = utc_now()
        status = "BLOCKED" if self.blocking else "PASS"
        return {
            "result_id": f"option_b_manual_static_review_result_{completed}",
            "review_version": REVIEW_VERSION,
            "input_ref": self.input_path,
            "input_status": payload.get("overall_status"),
            "overall_status": status,
            "acceptance_status": "BLOCKED" if self.blocking else "READY_FOR_HUMAN_REVIEW",
            "review_object_count": len(objects),
            "blocking_failure_count": len(self.blocking),
            "blocking_failures": self.blocking,
            "manual_review_objects": objects,
            "page18_status": "NOT_OPENED",
            "stage243_status": "NOT_CREATED",
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
    parser = argparse.ArgumentParser(description="Build Option B manual static review packet.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default="")
    args = parser.parse_args(argv)
    review = OptionBManualStaticReview(Path(args.repo_root).resolve(), args.input)
    result = review.build_review()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
