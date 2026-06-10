#!/usr/bin/env python3
"""Option B Writer IDE static flow scaffold.

Transforms the accepted formula signal mapping artifact into static advisory
panels. This is not Page18 runtime implementation.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

FLOW_VERSION = "0.1.0"
DEFAULT_MAPPING_RESULT = "fixtures/option_b_validation/formula_signal_mapping_result.json"

ACCEPTED_MAPPING_STATUS = {"PASS", "PASS_WITH_WARNINGS"}
ACCEPTED_MAPPING_DECISION = {"ACCEPTED_FOR_WRITER_IDE_STATIC_FLOW", "ACCEPTED_WITH_WARNINGS"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


class OptionBWriterIDEStaticFlow:
    def __init__(self, repo_root: Path, mapping_result_path: str = DEFAULT_MAPPING_RESULT) -> None:
        self.repo_root = repo_root
        self.mapping_result_path = mapping_result_path
        self.blocking_failures: List[Dict[str, str]] = []
        self.warnings: List[Dict[str, str]] = []

    def build_flow(self) -> Dict[str, Any]:
        started_at = utc_now()
        self.blocking_failures = []
        self.warnings = []
        mapping_result = self._load_mapping_result()
        if mapping_result:
            self._validate_gate(mapping_result)
        panels = self._build_panels(mapping_result) if not self.blocking_failures else []
        return self._result(started_at, mapping_result, panels)

    def _load_mapping_result(self) -> Mapping[str, Any]:
        path = self.repo_root / self.mapping_result_path
        if not path.exists():
            self._block(self.mapping_result_path, "mapping result file is missing")
            return {}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._block(self.mapping_result_path, f"invalid JSON: {exc}")
            return {}
        if not isinstance(payload, Mapping):
            self._block(self.mapping_result_path, "mapping result must be an object")
            return {}
        return payload

    def _validate_gate(self, mapping_result: Mapping[str, Any]) -> None:
        if mapping_result.get("overall_status") not in ACCEPTED_MAPPING_STATUS:
            self._block(self.mapping_result_path, "mapping result is not accepted")
        if mapping_result.get("acceptance_status") not in ACCEPTED_MAPPING_DECISION:
            self._block(self.mapping_result_path, "mapping result is not accepted for static IDE flow")
        if mapping_result.get("blocking_failure_count") != 0:
            self._block(self.mapping_result_path, "mapping result has blocking failures")
        for key, expected in {
            "page18_status": "NOT_OPENED",
            "stage243_status": "NOT_CREATED",
            "canonical_mutation_status": "NO_CANONICAL_MUTATION",
        }.items():
            if mapping_result.get(key) != expected:
                self._block(self.mapping_result_path, f"{key} must be {expected}")

    def _build_panels(self, mapping_result: Mapping[str, Any]) -> List[Dict[str, Any]]:
        mappings = as_list(mapping_result.get("formula_signal_mappings"))
        if not mappings:
            self._block(self.mapping_result_path, "formula signal mappings are missing")
            return []
        panels: List[Dict[str, Any]] = []
        for index, mapping in enumerate(mappings):
            if not isinstance(mapping, Mapping):
                self._block(f"formula_signal_mappings[{index}]", "mapping is not an object")
                continue
            if mapping.get("advisory_only") is not True:
                self._block(str(mapping.get("formula_signal_id", index)), "mapping must remain advisory only")
                continue
            panels.append(
                {
                    "panel_id": f"writer_ide_panel_{mapping.get('formula_signal_id', index)}",
                    "panel_type": "FORMULA_SIGNAL_ADVISORY_PANEL",
                    "formula_signal_id": mapping.get("formula_signal_id"),
                    "formula_id": mapping.get("formula_id"),
                    "formula_name": mapping.get("formula_name"),
                    "formula_group": mapping.get("formula_group"),
                    "surface_label": self._surface_label(mapping),
                    "source_record_ids": mapping.get("source_record_ids", []),
                    "source_record_types": mapping.get("source_record_types", []),
                    "source_record_summaries": mapping.get("source_record_summaries", []),
                    "ide_action": "DISPLAY_ADVISORY_ONLY",
                    "advisory_only": True,
                    "value_proof_status": "NOT_PROOF_PREREGISTRATION_REQUIRED",
                    "learnable_critic_status": "NO_COEFFICIENT_UPDATE_AUDIT_REQUIRED",
                    "manual_review_required": True,
                }
            )
        return panels

    def _surface_label(self, mapping: Mapping[str, Any]) -> str:
        name = mapping.get("formula_name") or mapping.get("formula_group") or "Formula Signal"
        output = mapping.get("output_signal_value_or_label") or "fixture advisory"
        return f"{name}: {output}"

    def _result(self, started_at: str, mapping_result: Mapping[str, Any], panels: List[Dict[str, Any]]) -> Dict[str, Any]:
        completed_at = utc_now()
        if self.blocking_failures:
            overall_status = "BLOCKED"
            acceptance_status = "BLOCKED"
            downstream_status = "NOT_READY"
        elif self.warnings:
            overall_status = "PASS_WITH_WARNINGS"
            acceptance_status = "ACCEPTED_WITH_WARNINGS"
            downstream_status = "READY_FOR_MANUAL_STATIC_REVIEW"
        else:
            overall_status = "PASS"
            acceptance_status = "ACCEPTED_FOR_MANUAL_STATIC_REVIEW"
            downstream_status = "READY_FOR_MANUAL_STATIC_REVIEW"
        return {
            "result_id": f"option_b_writer_ide_static_flow_result_{completed_at}",
            "flow_version": FLOW_VERSION,
            "mapping_result_ref": self.mapping_result_path,
            "mapping_result_status": mapping_result.get("overall_status"),
            "mapping_acceptance_status": mapping_result.get("acceptance_status"),
            "overall_status": overall_status,
            "acceptance_status": acceptance_status,
            "downstream_status": downstream_status,
            "panel_count": len(panels),
            "warning_count": len(self.warnings),
            "blocking_failure_count": len(self.blocking_failures),
            "warnings": self.warnings,
            "blocking_failures": self.blocking_failures,
            "writer_ide_panels": panels,
            "provider_status": "DISABLED",
            "generation_status": "DISABLED",
            "memory_write_status": "DISABLED",
            "canonical_mutation_status": "NO_CANONICAL_MUTATION",
            "value_proof_status": "NOT_PROOF_PREREGISTRATION_REQUIRED",
            "learnable_critic_status": "NO_COEFFICIENT_UPDATE_AUDIT_REQUIRED",
            "page18_status": "NOT_OPENED",
            "stage243_status": "NOT_CREATED",
            "validation_started_at": started_at,
            "validation_completed_at": completed_at,
            "created_at": completed_at,
            "review_status": "GENERATED_BY_SCAFFOLD",
        }

    def _block(self, path: str, message: str) -> None:
        self.blocking_failures.append({"severity": "BLOCKING", "path": path, "message": message})


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Option B static Writer IDE advisory panels.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--mapping-result", default=DEFAULT_MAPPING_RESULT)
    parser.add_argument("--output", default="")
    args = parser.parse_args(argv)
    flow = OptionBWriterIDEStaticFlow(Path(args.repo_root).resolve(), args.mapping_result)
    result = flow.build_flow()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result["overall_status"] in {"PASS", "PASS_WITH_WARNINGS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
