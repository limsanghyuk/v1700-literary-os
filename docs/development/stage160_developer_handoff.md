# Stage160 Developer Handoff

Run:

```bash
python -m compileall -q src tools
python tools/run_stage159_release_gate.py
python tools/run_stage160_page03_release_seal.py
python tools/run_stage160_release_gate.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage160_page03_release_seal.py -q
```

Stage161 may begin only after Stage160 passes.
