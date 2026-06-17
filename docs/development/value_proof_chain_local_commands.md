# Value Proof Chain Local Commands

Created: 2026-06-17
Branch: corpus-absorption-formula-bridge-handoff

Run in order:

```powershell
git fetch --all --tags --prune
git checkout corpus-absorption-formula-bridge-handoff
git pull --ff-only origin corpus-absorption-formula-bridge-handoff
python -m pip install -e ".[dev]"
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/run_value_proof_arm_b_guidance_surface.py
python -m pytest tests/test_value_proof_arm_b_guidance_surface.py -q
python -m pytest tests/test_value_proof_arm_b_preregistration_packet_builder.py -q
python tools/run_value_proof_blind_evaluator_packet_builder.py
python -m pytest tests/test_value_proof_blind_evaluator_packet_builder.py -q
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage242_release_gate.py
python tools/run_release_gate.py
```

Expected reports:

```text
release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json
release/current/value_proof_arm_b_preregistration_pack/value_proof_arm_b_preregistration_packet_report.json
release/current/value_proof_blind_evaluator_pack/value_proof_blind_evaluator_packet_report.json
```

After reports exist, rerun Page18 readiness precheck.
