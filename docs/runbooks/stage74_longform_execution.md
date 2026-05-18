# Stage74 Longform Execution Runbook

From the active repo:

```powershell
python tools/run_stage73_1_release_gate.py
python tools/run_longform_execution_gate.py
python tools/run_stage74_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```

Expected result: all pass, provider default calls 0, Node2 raw reveal access 0.
