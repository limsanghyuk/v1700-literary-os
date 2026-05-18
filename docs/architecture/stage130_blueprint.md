# V1700 Stage130 — MultiWork Release Blueprint

## 0. 기준선

Stage130의 기준선은 `V1700 Stage129 — MultiWorkCIM + Cross-Work Canon Governor`이다. Stage127은 MultiWork preflight와 isolation audit를 수행했고, Stage128은 SharedWorld/SharedCharacter read-only absorption을 수행했으며, Stage129는 project-local CIM과 read-only cross-project influence edge, cross-work canon governor를 결합했다.

## 1. Stage130 정의

```text
Stage130 — MultiWork Release
목표: 다중 작품 운영 계층의 첫 clean release.
```

Stage130은 V571 MultiWork를 무제한 활성화하는 단계가 아니다. Stage127~129의 격리, read-only shared adapters, cross-work canon governor를 하나의 release authority로 봉인하는 단계다.

## 2. 비목표

- cross-project write를 허용하지 않는다.
- raw manuscript sharing을 허용하지 않는다.
- SharedWorldDB를 전체 canon source of truth로 승격하지 않는다.
- direct V571 trunk merge를 허용하지 않는다.
- Gate26/GIG를 hard block으로 켜지 않는다.
- active learning, ASD mutation, PNE runtime training을 켜지 않는다.

## 3. 핵심 불변조건

```text
stage127_preflight_pass = true
stage128_read_only_absorption_pass = true
stage129_cim_governor_pass = true
direct_v571_merge_detected = false
cross_project_write_allowed = false
unauthorized_cross_reads = 0
unauthorized_cross_writes = 0
raw_manuscript_cross_project_leakage = 0
canon_auto_resolution_count = 0
provider_default_calls = 0
live_provider_call_count_in_release_gate = 0
node2_raw_reveal_access = 0
branchpoint_lineage_preserved = true
```

## 4. 패키지 구조

```text
src/v1700/multiwork_release/
  __init__.py
  contracts.py
  release_matrix.py
  operational_surface.py
  gitnexus_preflight.py
  release_seal.py
  report.py

src/v1700/stage130/
  __init__.py
  stage130_runner.py

src/v1700/gates/stage130_release_gate.py

tools/run_stage130_multiwork_release.py
tools/run_stage130_release_gate.py

tests/test_stage130_multiwork_release.py
```

## 5. Release Matrix

Stage130은 Stage127~129 산출물을 다시 검증한다.

```text
Stage127 MultiWork Preflight & Isolation Audit → pass
Stage128 SharedWorld / SharedCharacter Read-Only Absorption → pass
Stage129 MultiWorkCIM + Cross-Work Canon Governor → pass
```

## 6. Operational Surface

Stage130에서 활성화되는 표면:

```text
project_isolation_audit
shared_character_read_only_adapter
shared_world_read_only_adapter
project_local_cim
cross_project_influence_edges_read_only
cross_work_canon_governor
multiwork_release_gate_authority
```

Stage130에서 여전히 차단되는 표면:

```text
cross_project_write
raw_manuscript_sharing
direct_v571_trunk_merge
canon_auto_resolution
shared_world_source_of_truth_promotion
gate26_hard_block
active_learning_runtime_mutation
```

## 7. Release Gate

Stage130 release gate는 다음을 확인한다.

```text
stage129_baseline_gate_pass
release_matrix_pass
operational_surface_pass
release_seal_pass
stage127_to_stage129_evidence_preserved
multiwork_release_authorized
direct_v571_merge_blocked
cross_project_write_blocked
unauthorized_cross_reads_writes_zero
raw_manuscript_leakage_zero
canon_auto_resolution_disabled
shared_world_source_of_truth_not_promoted
gate26_hard_block_deferred
provider_zero_pass
node2_boundary_pass
credential_leakage_zero
gitnexus_python_fallback_preflight_pass
branchpoint_survival_pass
repo_doctor_active_stage_ready
clean_zip_packaging_pass
```

## 8. 후속 단계

```text
Stage131 — GIG / Gate26 Advisory Absorption
Stage132 — Contradiction Classifier + Mystery Exemption
```
