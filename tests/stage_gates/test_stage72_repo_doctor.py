import json
from pathlib import Path

STAGE101_AND_PRIOR = {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89", "stage90", "stage91", "stage92", "stage93", "stage94", "stage95", "stage96", "stage97", "stage97.1", "stage97.2", "stage98", "stage99", "stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127", "stage128", "stage129", "stage130", "stage131", "stage132", "stage133", "stage134", "stage135", "stage136", "stage137", "stage138"}


def test_stage72_manifests_exist_and_point_to_live_core():
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    assert manifest["active_version"] in {"stage72", "stage72.1", "stage72.2", "stage72.3", "stage73", "stage73.1", "stage74", "stage75", "stage76", "stage77", "stage78", "stage79", "stage80", "stage81", "stage81.1", "stage82", "stage83", *STAGE101_AND_PRIOR}
    assert (root / manifest["runtime_entrypoint"]).exists()
    if manifest["active_version"] == "stage72.1":
        assert "graph_nexus_release_gate" in manifest["active_gates"]
    if manifest["active_version"] == "stage72.2":
        assert "stage72_2_release_gate" in manifest["active_gates"]

    if manifest["active_version"] in STAGE101_AND_PRIOR:
        assert "stage83_1_release_gate" in manifest["active_gates"]
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1"}:
        assert "stage84_release_gate" in manifest["active_gates"]
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84"}:
        assert "stage85_release_gate" in manifest["active_gates"]
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85"}:
        assert "stage86_release_gate" in manifest["active_gates"]

    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86"}:
        assert "stage87_release_gate" in manifest.get("active_gates", [])
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87"}:
        assert "stage88_release_gate" in manifest.get("active_gates", [])
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88"}:
        assert "stage89_release_gate" in manifest.get("active_gates", [])
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89"}:
        assert "stage90_release_gate" in manifest.get("active_gates", [])
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89", "stage90"}:
        assert "stage91_release_gate" in manifest.get("active_gates", [])
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89", "stage90", "stage91"}:
        assert "stage92_release_gate" in manifest.get("active_gates", [])
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89", "stage90", "stage91", "stage92"}:
        assert "stage93_release_gate" in manifest.get("active_gates", [])


def test_stage93_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89", "stage90", "stage91", "stage92"}:
        assert "stage93_release_gate" in manifest.get("active_gates", [])


def test_stage94_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] in STAGE101_AND_PRIOR - {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89", "stage90", "stage91", "stage92", "stage93"}:
        assert "stage94_release_gate" in manifest.get("active_gates", [])


def test_stage96_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage96":
        assert "stage95_release_gate" in manifest.get("active_gates", [])
        assert "stage96_release_gate" in manifest.get("active_gates", [])


def test_stage97_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage97":
        assert "stage96_release_gate" in manifest.get("active_gates", [])
        assert "stage97_release_gate" in manifest.get("active_gates", [])


def test_stage97_1_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage97.1":
        assert "stage96_release_gate" in manifest.get("active_gates", [])
        assert "stage97_release_gate" in manifest.get("active_gates", [])
        assert "stage97_1_release_gate" in manifest.get("active_gates", [])


def test_stage97_2_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage97.2":
        assert "stage96_release_gate" in manifest.get("active_gates", [])
        assert "stage97_release_gate" in manifest.get("active_gates", [])
        assert "stage97_1_release_gate" in manifest.get("active_gates", [])
        assert "stage97_2_release_gate" in manifest.get("active_gates", [])


def test_stage98_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage98":
        assert "stage96_release_gate" in manifest.get("active_gates", [])
        assert "stage97_release_gate" in manifest.get("active_gates", [])
        assert "stage97_1_release_gate" in manifest.get("active_gates", [])
        assert "stage97_2_release_gate" in manifest.get("active_gates", [])
        assert "stage98_release_gate" in manifest.get("active_gates", [])


def test_stage100_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage100":
        assert "stage98_release_gate" in manifest.get("active_gates", [])
        assert "stage99_release_gate" in manifest.get("active_gates", [])
        assert "stage100_release_gate" in manifest.get("active_gates", [])


def test_stage101_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] in {"stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage98_release_gate" in manifest.get("active_gates", [])
        assert "stage99_release_gate" in manifest.get("active_gates", [])
        assert "stage100_release_gate" in manifest.get("active_gates", [])
        assert "stage101_release_gate" in manifest.get("active_gates", [])


def test_stage102_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] in {"stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage98_release_gate" in manifest.get("active_gates", [])
        assert "stage99_release_gate" in manifest.get("active_gates", [])
        assert "stage100_release_gate" in manifest.get("active_gates", [])
        assert "stage101_release_gate" in manifest.get("active_gates", [])
        assert "stage102_release_gate" in manifest.get("active_gates", [])


def test_stage103_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] in {"stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage98_release_gate" in manifest.get("active_gates", [])
        assert "stage99_release_gate" in manifest.get("active_gates", [])
        assert "stage100_release_gate" in manifest.get("active_gates", [])
        assert "stage101_release_gate" in manifest.get("active_gates", [])
        assert "stage102_release_gate" in manifest.get("active_gates", [])
        assert "stage103_release_gate" in manifest.get("active_gates", [])


def test_stage104_to_stage107_release_gates_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    active = manifest["active_version"]
    gates = manifest.get("active_gates", [])
    if active in {"stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage104_release_gate" in gates
    if active in {"stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage105_release_gate" in gates
    if active in {"stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage106_release_gate" in gates
    if active in {"stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage107_release_gate" in gates


def test_stage114_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage114":
        gates = manifest.get("active_gates", [])
        assert "stage112_release_gate" in gates
        assert "stage113_release_gate" in gates
        assert "stage114_adaptive_momentum_weights" in gates
        assert "stage114_release_gate" in gates


def test_stage115_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage115":
        gates = manifest.get("active_gates", [])
        assert "stage112_release_gate" in gates
        assert "stage113_release_gate" in gates
        assert "stage114_release_gate" in gates
        assert "stage115_character_influence_matrix" in gates
        assert "stage115_release_gate" in gates


def test_stage116_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage116":
        gates = manifest.get("active_gates", [])
        assert "stage112_release_gate" in gates
        assert "stage113_release_gate" in gates
        assert "stage114_release_gate" in gates
        assert "stage115_release_gate" in gates
        assert "stage116_domain_rag_fusion" in gates
        assert "stage116_release_gate" in gates


def test_stage117_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage117":
        assert "stage116_release_gate" in manifest.get("active_gates", [])
        assert "stage117_release_gate" in manifest.get("active_gates", [])
        assert "stage117_narrative_tension_curve" in manifest.get("active_gates", [])


def test_stage118_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage118":
        assert "stage117_release_gate" in manifest.get("active_gates", [])
        assert "stage118_release_gate" in manifest.get("active_gates", [])
        assert "stage118_nil_orchestrator" in manifest.get("active_gates", [])


def test_stage119_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] in {"stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        assert "stage118_release_gate" in manifest.get("active_gates", [])
        assert "stage119_release_gate" in manifest.get("active_gates", [])
        assert "stage119_nie_adversarial_regression" in manifest.get("active_gates", [])


def test_stage127_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage127":
        assert "stage126_release_gate" in manifest.get("active_gates", [])
        assert "stage127_multiwork_preflight" in manifest.get("active_gates", [])
        assert "stage127_release_gate" in manifest.get("active_gates", [])


def test_stage136_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage136":
        gates = manifest.get("active_gates", [])
        assert "stage134_release_gate" in gates
        assert "stage135_release_gate" in gates
        assert "stage136_schema_registry" in gates
        assert "stage136_release_gate" in gates


def test_stage137_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage137":
        gates = manifest.get("active_gates", [])
        assert "stage136_release_gate" in gates
        assert "stage137_migration_manager" in gates
        assert "stage137_release_gate" in gates


def test_stage138_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage138":
        gates = manifest.get("active_gates", [])
        assert "stage137_release_gate" in gates
        assert "stage138_losdb_storage_contracts" in gates
        assert "stage138_release_gate" in gates
