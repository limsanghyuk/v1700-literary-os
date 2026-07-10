# Local P8.1 Validation Execution Manual

Date: 2026-07-04  
Status: local execution manual loaded to hub  
Scope: Codex-local validation / JSON parse / schema validation / cross-level integrity / result packet creation

## 0. Purpose

This manual defines the local execution work required after remote P8.1 protocol preparation.

The goal is to produce:

```text
release/current/season_wiring_pack/full_season_validation_result_p8_1.json
```

This result file is required before P9 Scorecard Preflight can be interpreted.

## 1. Local Root

Recommended local repository root:

```powershell
C:\AI_Codex\codex-work\gpt
```

If the repository is located elsewhere, run the same commands from the actual repository root.

## 2. Branch and Pull

Run:

```powershell
cd C:\AI_Codex\codex-work\gpt
git status
git checkout corpus-absorption-formula-bridge-handoff
git pull origin corpus-absorption-formula-bridge-handoff
```

Confirm that the following files exist:

```powershell
Test-Path release/current/season_wiring_pack/full_season_candidate_package_fixture_v1.json
Test-Path release/current/season_wiring_pack/full_season_candidate_package_schema_v1.json
Test-Path release/current/season_wiring_pack/full_season_hard_rule_self_check_v1.json
Test-Path release/current/season_wiring_pack/full_season_validation_protocol_p8_1.json
```

## 3. Python Environment

Use the local Python available on the machine.

Recommended:

```powershell
python --version
python -m pip --version
```

If `jsonschema` is missing, install it:

```powershell
python -m pip install jsonschema
```

If internet access is not available, create a JSON parse result first and mark schema validation as blocked until `jsonschema` is available.

## 4. Minimal Validation Script

Create a temporary local script:

```powershell
notepad tools\validate_full_season_p8_1.py
```

If `tools` does not exist:

```powershell
mkdir tools
```

Recommended script content:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "release/current/season_wiring_pack/full_season_candidate_package_fixture_v1.json"
SCHEMA = ROOT / "release/current/season_wiring_pack/full_season_candidate_package_schema_v1.json"
SELF_CHECK = ROOT / "release/current/season_wiring_pack/full_season_hard_rule_self_check_v1.json"
OUT = ROOT / "release/current/season_wiring_pack/full_season_validation_result_p8_1.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    result: Dict[str, Any] = {
        "document_type": "full_season_validation_result",
        "version": "1.0-stage243-p8.1",
        "created_at": "2026-07-04",
        "source_fixture": str(FIXTURE.relative_to(ROOT)).replace("\\\\", "/"),
        "source_schema": str(SCHEMA.relative_to(ROOT)).replace("\\\\", "/"),
        "json_parse_pass": False,
        "json_parse_error_count": 0,
        "parsed_file_count": 0,
        "schema_validation_pass": False,
        "schema_error_count": 0,
        "schema_error_paths": [],
        "cross_level_integrity_pass": False,
        "integrity_error_count": 0,
        "integrity_warning_count": 0,
        "blocking_integrity_findings": [],
        "boundary_invariants_pass": False,
        "boundary_error_count": 0,
        "boundary_warning_count": 0,
        "overall_validation_status": "blocked",
        "gate_a_ready_after_validation": False,
        "scorecard_preflight_allowed": False,
        "required_next_actions": [],
        "promotion_status": {
            "macro_planner_promotion": "blocked",
            "full_author_promotion": "blocked",
            "live_generation_readiness": "blocked",
        },
    }

    parsed: Dict[str, Any] = {}
    for name, path in [("fixture", FIXTURE), ("schema", SCHEMA), ("self_check", SELF_CHECK)]:
        try:
            parsed[name] = load_json(path)
            result["parsed_file_count"] += 1
        except Exception as exc:
            result["json_parse_error_count"] += 1
            result.setdefault("json_parse_errors", []).append({"file": str(path), "error": str(exc)})

    result["json_parse_pass"] = result["json_parse_error_count"] == 0

    if not result["json_parse_pass"]:
        result["overall_validation_status"] = "fail_validation"
        result["required_next_actions"] = ["fix_json_parse_errors"]
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    fixture = parsed["fixture"]
    schema = parsed["schema"]
    self_check = parsed["self_check"]

    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(fixture), key=lambda e: list(e.path))
        result["schema_error_count"] = len(errors)
        result["schema_error_paths"] = ["/" + "/".join(map(str, e.path)) + ": " + e.message for e in errors]
        result["schema_validation_pass"] = len(errors) == 0
    except Exception as exc:
        result["schema_validation_pass"] = False
        result["schema_error_count"] = 1
        result["schema_error_paths"] = ["schema_validation_blocked: " + str(exc)]

    # Cross-level integrity checks for current metadata-only fixture.
    integrity_findings: List[str] = []

    expected_counts = fixture.get("included_artifact_inventory", {})
    if expected_counts.get("full_series_arc_spec_count", 0) < 1:
        integrity_findings.append("missing_full_series_arc_spec_ref")
    if expected_counts.get("season_plan_count", 0) < 1:
        integrity_findings.append("missing_season_plan_ref")
    if expected_counts.get("episode_arc_chain_count", 0) < 1:
        integrity_findings.append("missing_episode_arc_chain_ref")
    if expected_counts.get("sequence_blueprint_count", 0) < 1:
        integrity_findings.append("missing_sequence_blueprint_refs")
    if expected_counts.get("scene_blueprint_count", 0) < 1:
        integrity_findings.append("missing_scene_blueprint_refs")
    if expected_counts.get("renderer_prompt_packet_count", 0) < 1:
        integrity_findings.append("missing_renderer_prompt_packet_refs")

    if fixture.get("package_identity", {}).get("target_episode_count") not in (16, 24):
        integrity_findings.append("invalid_target_episode_count")

    checks = fixture.get("cross_level_integrity_checks", {})
    not_run_checks = [k for k, v in checks.items() if isinstance(v, dict) and v.get("status") == "not_run"]
    if not_run_checks:
        result["integrity_warning_count"] += len(not_run_checks)
        result.setdefault("integrity_warnings", []).extend(["not_run:" + x for x in not_run_checks])

    result["blocking_integrity_findings"] = integrity_findings
    result["integrity_error_count"] = len(integrity_findings)
    result["cross_level_integrity_pass"] = len(integrity_findings) == 0

    # Boundary invariants.
    boundary_errors: List[str] = []
    authority = fixture.get("authority", {})
    safety = fixture.get("safety_boundary", {})
    if authority.get("provider_call_count") != 0:
        boundary_errors.append("provider_call_count_not_zero")
    if authority.get("runtime_generation") is not False:
        boundary_errors.append("runtime_generation_not_false")
    if authority.get("draft_text_exported") is not False:
        boundary_errors.append("draft_text_exported_not_false")
    if authority.get("promotion_claim") is not False:
        boundary_errors.append("promotion_claim_not_false")
    if safety.get("actual_provider_call_allowed") is not False:
        boundary_errors.append("actual_provider_call_allowed_not_false")
    if safety.get("actual_prose_generation_allowed") is not False:
        boundary_errors.append("actual_prose_generation_allowed_not_false")

    result["boundary_error_count"] = len(boundary_errors)
    result["boundary_errors"] = boundary_errors
    result["boundary_invariants_pass"] = len(boundary_errors) == 0

    if not result["schema_validation_pass"]:
        result["overall_validation_status"] = "fail_validation"
        result["required_next_actions"] = ["fix_schema_validation_errors"]
    elif not result["boundary_invariants_pass"]:
        result["overall_validation_status"] = "blocked"
        result["required_next_actions"] = ["fix_boundary_invariant_errors"]
    elif not result["cross_level_integrity_pass"]:
        result["overall_validation_status"] = "manual_review_required"
        result["required_next_actions"] = ["fix_cross_level_integrity_findings"]
    elif result["integrity_warning_count"] > 0:
        result["overall_validation_status"] = "pass_with_warning"
        result["required_next_actions"] = ["run_deeper_instantiated_integrity_checks", "rerun_hard_rule_gate"]
    else:
        result["overall_validation_status"] = "pass"
        result["required_next_actions"] = ["rerun_hard_rule_gate", "consider_scorecard_preflight_if_allowed"]

    hard_rule_pass = self_check.get("self_check_summary", {}).get("hard_rule_pass") is True
    result["gate_a_ready_after_validation"] = result["overall_validation_status"] in {"pass", "pass_with_warning"} and hard_rule_pass
    result["scorecard_preflight_allowed"] = result["gate_a_ready_after_validation"]
    result["next_required_step"] = "rerun_hard_rule_gate_before_scorecard" if result["overall_validation_status"] in {"pass", "pass_with_warning"} else "resolve_validation_findings"

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps({
        "json_parse_pass": result["json_parse_pass"],
        "schema_validation_pass": result["schema_validation_pass"],
        "cross_level_integrity_pass": result["cross_level_integrity_pass"],
        "boundary_invariants_pass": result["boundary_invariants_pass"],
        "overall_validation_status": result["overall_validation_status"],
        "gate_a_ready_after_validation": result["gate_a_ready_after_validation"],
        "scorecard_preflight_allowed": result["scorecard_preflight_allowed"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

## 5. Run Validation

Run:

```powershell
python tools\validate_full_season_p8_1.py
```

Confirm output:

```powershell
Test-Path release/current/season_wiring_pack/full_season_validation_result_p8_1.json
Get-Content release/current/season_wiring_pack/full_season_validation_result_p8_1.json -TotalCount 80
```

## 6. Interpret Result

Use these rules:

```text
overall_validation_status: pass -> rerun hard-rule gate, then consider P9 if allowed
overall_validation_status: pass_with_warning -> review warnings, rerun hard-rule gate, then consider P9 if allowed
overall_validation_status: manual_review_required -> fix or justify findings before P9
overall_validation_status: fail_validation -> fix JSON/schema errors
overall_validation_status: blocked -> fix boundary invariant errors immediately
```

Do not run P9 if:

```text
scorecard_preflight_allowed: false
```

## 7. Commit and Push

After result creation:

```powershell
git status
git add release/current/season_wiring_pack/full_season_validation_result_p8_1.json
git commit -m "Add full-season validation result P8.1"
git push origin corpus-absorption-formula-bridge-handoff
```

## 8. Optional: Commit the local script

If the validation script should become part of the repository, commit it:

```powershell
git add tools/validate_full_season_p8_1.py
git commit -m "Add local full-season validation script P8.1"
git push origin corpus-absorption-formula-bridge-handoff
```

If the script is only a temporary execution helper, do not commit it.

## 9. Required Return Report

After local execution, report:

```text
commit SHA
json_parse_pass
schema_validation_pass
schema_error_count
cross_level_integrity_pass
integrity_error_count
integrity_warning_count
boundary_invariants_pass
overall_validation_status
gate_a_ready_after_validation
scorecard_preflight_allowed
```

## 10. Boundary

During this local validation task, do not perform:

```text
provider calls
live prose generation
canonical mutation
training update
adapter promotion
promotion claim
```

## 11. Final Local Decision

The local task is complete only when:

```text
release/current/season_wiring_pack/full_season_validation_result_p8_1.json
```

exists, is committed, and is pushed to the working branch.
