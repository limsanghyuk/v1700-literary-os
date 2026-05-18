# V1700 Stage129 설계도
## MultiWorkCIM + Cross-Work Canon Governor

## 0. 기준선

현재 기준선은 `V1700 Stage128 — SharedWorld / SharedCharacter Read-Only Absorption`이다.

Stage128은 SharedCharacterDB와 SharedWorldDB를 read-only adapter로 흡수했고, 다음을 금지했다.

```text
cross-project write = 0
raw manuscript sharing = 0
license 없는 character reuse = BLOCK
shared world source-of-truth promotion = false
```

Stage129는 이 위에 **작품별 CIM을 유지하면서 cross-project influence를 read-only edge로만 계산**하고, 작품 간 canon 충돌을 Governor가 판단하는 단계다.

## 1. Stage129 목표

```text
Stage129 — MultiWorkCIM + Cross-Work Canon Governor
```

목표:

1. Project-local CIM을 유지한다.
2. Cross-project influence는 read-only edge로만 계산한다.
3. cross-project write를 계속 차단한다.
4. CanonConflictScore를 기계 판독형으로 계산한다.
5. PASS / WARN / BLOCK canon decision을 release evidence로 남긴다.
6. Canon auto-resolution은 허용하지 않는다.
7. Stage130 MultiWork Release 전 safety authority를 제공한다.

## 2. 비목표

Stage129에서는 다음을 하지 않는다.

```text
1. MultiWork release를 공식 완성 상태로 선언하지 않는다.
2. SharedCharacterDB / SharedWorldDB write 권한을 열지 않는다.
3. cross-project influence write를 허용하지 않는다.
4. canon conflict를 자동 수정하지 않는다.
5. AuthorLicense / IP Boundary를 최종 완성하지 않는다.
6. Gate26 GIG를 hard block으로 활성화하지 않는다.
7. Active learning, ASD mutation, PNE runtime training을 켜지 않는다.
```

## 3. 핵심 공식

### 3.1 MultiWorkCIM Boundary

```text
MultiWorkCIM = CIM_project_local + CrossProjectInfluenceEdges(read_only)
```

초기 Stage129 조건:

```text
cross_project_influence_write = 0
```

### 3.2 Cross-Work Access Formula

```text
AccessAllowed(project_i, project_j, resource) =
license_edge_exists
AND isolation_policy_allows
AND resource_scope_permits
AND author_approval_valid
AND access_type in {read, reference}
AND read_only == true
```

### 3.3 Canon Conflict Score

```text
CanonConflictScore =
timeline_conflict × 0.35
+ world_rule_conflict × 0.30
+ character_identity_conflict × 0.20
+ relationship_conflict × 0.15
```

초기 threshold:

```text
score <= 0.30        => PASS
0.30 < score <= 0.60 => WARN
score > 0.60         => BLOCK
```

## 4. 패키지 구조

```text
src/v1700/multiwork_cim_governor/
  __init__.py
  contracts.py
  fixtures.py
  project_local_cim.py
  cross_project_influence.py
  canon_governor.py
  gitnexus_preflight.py
  report.py

src/v1700/stage129/
  __init__.py
  stage129_runner.py

src/v1700/gates/stage129_release_gate.py

tools/
  run_stage129_multiwork_cim_governor.py
  run_stage129_release_gate.py

tests/
  test_stage129_multiwork_cim_governor.py
```

## 5. 데이터 계약

### ProjectCIMSnapshot

```python
@dataclass(frozen=True)
class ProjectCIMSnapshot:
    project_id: str
    canon_root_id: str
    local_character_count: int
    local_world_rule_count: int
    local_relation_count: int
    cross_project_influence_write: int = 0
    raw_manuscript_exported: bool = False
```

### CrossProjectInfluenceEdge

```python
@dataclass(frozen=True)
class CrossProjectInfluenceEdge:
    edge_id: str
    source_project_id: str
    target_project_id: str
    entity_id: str
    access_type: Literal["read", "reference", "adapt", "write"]
    license_edge_exists: bool
    approved_by_author: bool
    resource_scope_permits: bool
    read_only: bool = True
```

### CanonConflict

```python
@dataclass(frozen=True)
class CanonConflict:
    conflict_id: str
    source_project_id: str
    target_project_id: str
    entity_id: str
    timeline_conflict: float
    world_rule_conflict: float
    character_identity_conflict: float
    relationship_conflict: float
    evidence: tuple[str, ...]
    recommended_action: str
```

## 6. Release Gate

Stage129 release gate는 다음을 확인한다.

```text
stage128_baseline_gate_pass
project_local_cim_builder_pass
cross_project_influence_read_only_pass
cross_work_canon_governor_pass
project_local_cim_preserved
cross_project_write_blocked
unauthorized_cross_reads_writes_zero
license_boundary_preserved
canon_conflict_block_fixture_pass
canon_auto_resolution_disabled
cross_work_canon_merge_disabled
raw_manuscript_leakage_zero
provider_zero_pass
node2_boundary_pass
credential_leakage_zero_pass
gitnexus_python_fallback_preflight_pass
gitnexus_shape_check_pass
branchpoint_survival_pass
stage130_multiwork_release_deferred
docs_manifest_pass
repo_doctor_active_stage_ready
clean_zip_packaging_pass
secret_scan_pass
```

## 7. Release Block 조건

```text
Stage128 baseline gate fails
project-local CIM becomes cross-project mutable
cross-project write allowed
license edge missing but access allowed
unauthorized cross read/write > 0
canon BLOCK case not blocked
canon auto-resolution enabled
cross-work canon merge enabled
raw manuscript provider leakage > 0
Node2 raw reveal access > 0
provider live call count > 0
credential leakage > 0
GitNexus shape_check fails
branchpoint survival fails
manifest/evidence missing
repo doctor does not recognize stage129
ZIP contains cache/backslash/private env files
```

## 8. Local Codex 실행 명령

```bash
python -m compileall src tools
python -m v1700.cli --help
python tools/run_stage129_multiwork_cim_governor.py
python tools/run_stage129_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest -q tests/test_stage129_multiwork_cim_governor.py
```

## 9. 다음 단계

Stage129가 통과하면 다음 단계는 다음이다.

```text
Stage130 — MultiWork Release
```

Stage130은 다중 작품 운영 계층의 첫 clean release다.
