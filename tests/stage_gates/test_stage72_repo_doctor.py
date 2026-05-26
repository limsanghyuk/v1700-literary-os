import json
from pathlib import Path

STAGE101_AND_PRIOR = {"stage83.1", "stage84", "stage85", "stage86", "stage87", "stage88", "stage89", "stage90", "stage91", "stage92", "stage93", "stage94", "stage95", "stage96", "stage97", "stage97.1", "stage97.2", "stage98", "stage99", "stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127", "stage128", "stage129", "stage130", "stage131", "stage132", "stage133", "stage134", "stage135", "stage136", "stage137", "stage138", "stage139"}
KNOWN_ACTIVE_STAGES = STAGE101_AND_PRIOR | {"stage140", "stage141", "stage142", "stage143", "stage144", "stage145", "stage146", "stage147", "stage148", "stage149", "stage150", "stage151", "stage152", "stage153", "stage154", "stage155", "stage156", "stage157", "stage158", "stage159", "stage160", "stage161", "stage162", "stage163", "stage164", "stage165", "stage166", "stage167", "stage168"}


def test_stage72_manifests_exist_and_point_to_live_core():
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    assert manifest["active_version"] in {"stage72", "stage72.1", "stage72.2", "stage72.3", "stage73", "stage73.1", "stage74", "stage75", "stage76", "stage77", "stage78", "stage79", "stage80", "stage81", "stage81.1", "stage82", "stage83", *KNOWN_ACTIVE_STAGES}
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


def test_stage139_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage139":
        gates = manifest.get("active_gates", [])
        assert "stage138_release_gate" in gates
        assert "stage139_corpus_governance_pipeline" in gates
        assert "stage139_release_gate" in gates


def test_stage140_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage140":
        gates = manifest.get("active_gates", [])
        assert "stage139_release_gate" in gates
        assert "stage140_release_integrity" in gates
        assert "stage140_release_gate" in gates


def test_stage141_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage141":
        gates = manifest.get("active_gates", [])
        assert "stage140_release_gate" in gates
        assert "stage141_prose_generation_e2e" in gates
        assert "stage141_release_gate" in gates


def test_stage142_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage142":
        gates = manifest.get("active_gates", [])
        assert "stage141_release_gate" in gates
        assert "stage142_longform_benchmark_pack" in gates
        assert "stage142_release_gate" in gates


def test_stage143_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage143":
        gates = manifest.get("active_gates", [])
        assert "stage142_release_gate" in gates
        assert "stage143_user_cli_api_docs" in gates
        assert "stage143_release_gate" in gates


def test_stage144_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage144":
        gates = manifest.get("active_gates", [])
        assert "stage143_release_gate" in gates
        assert "stage144_split_ci_runtime_strategy" in gates
        assert "stage144_release_gate" in gates


def test_stage145_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage145":
        gates = manifest.get("active_gates", [])
        assert "stage144_release_gate" in gates
        assert "stage145_body_constitution" in gates
        assert "stage145_release_gate" in gates


def test_stage146_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage146":
        gates = manifest.get("active_gates", [])
        assert "stage145_release_gate" in gates
        assert "stage146_narrative_state_contract" in gates
        assert "stage146_release_gate" in gates


def test_stage147_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage147":
        gates = manifest.get("active_gates", [])
        assert "stage146_release_gate" in gates
        assert "stage147_project_manifest_body" in gates
        assert "stage147_release_gate" in gates


def test_stage148_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage148":
        gates = manifest.get("active_gates", [])
        assert "stage147_release_gate" in gates
        assert "stage148_node_boundary_constitution" in gates
        assert "stage148_release_gate" in gates


def test_stage149_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage149":
        gates = manifest.get("active_gates", [])
        assert "stage148_release_gate" in gates
        assert "stage149_body_constitution_release_gate" in gates
        assert "stage149_release_gate" in gates


def test_stage167_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage167":
        gates = manifest.get("active_gates", [])
        assert "stage166_release_gate" in gates
        assert "stage167_evaluation_contract" in gates
        assert "stage167_release_gate" in gates


def test_stage168_release_gate_registered_when_active():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    if manifest["active_version"] == "stage168":
        gates = manifest.get("active_gates", [])
        assert "stage167_release_gate" in gates
        assert "stage168_local_evaluation_packet_store" in gates
        assert "stage168_release_gate" in gates
