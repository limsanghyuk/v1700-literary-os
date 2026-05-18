# GraphNexus Release Runbook

1. Run `python tools/run_gitnexus_probe.py`.
2. Run `python tools/run_lineage_preflight.py --goal "Stage72.1 GraphNexus restoration"`.
3. Run `python tools/run_graph_nexus_impact.py --target Node2ProseCompiler`.
4. Run `python tools/run_legacy_logic_survival.py`.
5. Run `python tools/run_graph_nexus_detect_changes.py`.
6. Run `python tools/run_graph_nexus_release_gate.py`.
7. Run `python tools/run_release_gate.py`.
8. Run `python -m pytest -q tests`.

GitNexus is optional. If the probe reports it is missing, the Python fallback path is the expected passing path.
