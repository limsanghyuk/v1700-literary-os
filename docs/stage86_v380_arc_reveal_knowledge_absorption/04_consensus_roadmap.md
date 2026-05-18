# Stage86 합의 로드맵

작성일: 2026-05-13

## 1. 3인 합의 결론

최고 수석 아키텍트, 최고 수석 컴파일러, 최고 프린시펄 엔지니어는 다음에 합의한다.

```text
Stage86은 Reader-Facing Quality Loop가 아니라
V380 Arc-Reveal-Knowledge Absorption으로 진행한다.
```

이유:

```text
Stage85가 traceability를 완성했으므로,
이제 V380의 장편 기능을 흡수해도 기존 분기점 붕괴를 감지할 수 있다.
```

## 2. 단계별 로드맵

### Phase 0. Stage85 Baseline Lock

목적:

Stage86 구현 전 Stage85 상태를 고정한다.

작업:

- Stage85 release gate 통과 확인
- Stage85 GitNexus index quality report 보존
- Symbol-to-Branchpoint baseline 보존
- provider_default_calls 0 확인
- Node2 raw reveal access 0 확인

산출물:

```text
release/current/stage86_phase0_stage85_baseline_lock_report.json
```

### Phase 1. V380 Feature Map

목적:

V380 기능을 V1700 구조로 매핑한다.

작업:

- SeriesArcPlanner feature map
- CausalPlotGraph feature map
- EpisodeRevealBudget feature map
- CharacterKnowledgeProseBridge feature map
- V380 용어와 V1700 용어 충돌 정리

산출물:

```text
manifests/stage86_v380_feature_map_manifest.json
docs/stages/stage86_v380_feature_map.md
```

### Phase 2. Arc Runtime Contracts

목적:

16부작/24부작 arc를 데이터 계약으로 만든다.

작업:

- ArcAct
- ArcPlotNode
- ArcPlotEdge
- SeriesArcPlanner
- CausalPlotGraph
- tension curve
- act structure validation

산출물:

```text
src/v1700/arc_reveal_knowledge/arc_contracts.py
src/v1700/arc_reveal_knowledge/series_arc_planner.py
src/v1700/arc_reveal_knowledge/causal_plot_graph.py
tests/test_stage86_series_arc_planner.py
tests/test_stage86_causal_plot_graph.py
```

### Phase 3. Reveal Budget Runtime

목적:

비밀, 복선, 지연 공개, 차단 정책을 episode 단위로 제어한다.

작업:

- RevealPolicy
- EpisodeRevealBudget
- RevealBudgetViolationError
- RevealBlockedError
- RevealForeshadowOnlyError
- policy summary
- fact journey

산출물:

```text
src/v1700/arc_reveal_knowledge/reveal_budget.py
tests/test_stage86_episode_reveal_budget.py
```

### Phase 4. Character Knowledge Bridge

목적:

인물별 지식 상태를 산문 렌더링 제약으로 바꾼다.

작업:

- KnowledgeStatus
- KnowledgeRenderConstraint
- CharacterKnowledgeProseBridge
- KnowledgeLeakageError
- asymmetry pressure
- prose contract enrichment

산출물:

```text
src/v1700/arc_reveal_knowledge/knowledge_contracts.py
src/v1700/arc_reveal_knowledge/character_knowledge_bridge.py
src/v1700/arc_reveal_knowledge/prose_contract_bridge.py
tests/test_stage86_character_knowledge_bridge.py
```

### Phase 5. GraphNexus and Branchpoint Integration

목적:

Stage86 기능을 Stage85 traceability와 GraphNexus 권위 체계에 연결한다.

작업:

- Stage86 branchpoint 추가
- symbol-to-branchpoint trace 확장
- NarrativeGraph adapter 정의
- GitNexus index quality report 갱신

산출물:

```text
manifests/stage86_branchpoint_trace_manifest.json
release/current/stage86_gitnexus_index_quality_report.json
```

### Phase 6. Stage86 Release Gate

목적:

Stage86 전체 기능을 통합 검증한다.

작업:

- Stage85 gate 선행 확인
- arc graph smoke
- reveal budget smoke
- knowledge bridge smoke
- Node2 no leakage 확인
- provider-zero 확인

산출물:

```text
src/v1700/gates/stage86_release_gate.py
tools/run_stage86_release_gate.py
release/current/stage86_release_gate_report.json
tests/test_stage86_release_gate.py
```

### Phase 7. Developer Handoff and Packaging

목적:

개발자에게 전체 통합 병합 레포지토리를 제공한다.

작업:

- README 갱신
- STAGE_INDEX 갱신
- live_core_manifest 갱신
- package_manifest 갱신
- ZIP 패키징
- ZIP extraction probe

산출물:

```text
packages/v1700_stage86/V1700_stage86_v380_arc_reveal_knowledge_absorption_integrated_repository.zip
release/current/stage86_developer_handoff_report.md
release/current/stage86_zip_probe_report.md
```

## 3. Stage86 최종 게이트

Stage86 최종 통과 조건:

```text
compileall = pass
pytest >= 80 passed
stage85_release_gate = pass
stage86_release_gate = pass
main_release_gate = pass
symbol_to_branchpoint_trace_gate = pass
gitnexus_index_quality_gate = pass
provider_default_calls = 0
node2_raw_reveal_access_count = 0
reveal_leakage_count = 0
knowledge_leakage_count = 0
zip_probe = pass
```

## 4. 이후 단계 재정렬

Stage86 이후의 단계는 다음으로 조정한다.

```text
Stage87: Full Episode Scale-up, 8~16화 endurance proof
Stage88: Human Editorial Benchmark, 외부 작가/편집자/독자 평가
Stage89: Writer Studio UI + Export Pipeline
Stage90: External Model Adapter Governance
```

## 5. 최종 합의

```text
Stage86은 V1700이 상용 문학 생성 엔진으로 가기 위한 첫 번째 실질 문학 기능 흡수 단계다.
Stage85가 방어막이라면 Stage86은 장편 서사 근육이다.
```

