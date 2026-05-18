# Stage72.3 Foundation Lineage Recovery Blueprint

## 1. 설계 목적

이 설계도는 `Stage72.3`을 실제로 구현 가능한 구조로 변환한다.

목표는 다음 세 가지다.

```text
1. Stage01-39의 핵심 개념을 기계가 읽을 수 있는 형태로 복원한다.
2. 각 개념이 현재 V1700 어디에 살아 있는지 판정한다.
3. 이후의 변경이 기존 계보를 훼손하지 못하도록 영향 검토 게이트를 만든다.
```

## 2. 전체 구조

```mermaid
flowchart LR
    A["Historical Knowledge Base<br/>Stage01-39 artifacts"] --> B["Evidence Scanner"]
    B --> C["Raw Evidence Index"]
    C --> D["Concept Normalizer"]
    D --> E["Pre-Stage40 Lineage Manifest"]
    E --> F["Current Anchor Resolver"]
    F --> G["Survival Matrix"]
    G --> H["Organic Impact Review"]
    H --> I["Pre-Stage40 Survival Gate"]
    I --> J["Release Gate / Developer Handoff"]
```

## 3. 핵심 구성요소

### 3.1 Evidence Scanner

역할:

```text
knowledge_base 안의 Stage01-39 관련 문서, 매니페스트, 테스트, 실행 스크립트, 결과 리포트를 수집한다.
```

출력:

```text
manifests/pre_stage40_raw_evidence_index.json
```

기본 수집 대상:

```text
docs
manifests
reports
tests
run_stage*.py
*_contract.py
*_planner.py
*_gate.py
```

우선 확인 대상 예시:

```text
series_arc_planner.py
style_evolution_analyzer.py
commit_rollback_protocol.py
temporal_delta_controller.py
pressure_threshold_monitor.py
pressure_relief_event_planner.py
longform_scene_sequence_planner.py
run_stage33_workbench.py
run_stage39_phase39_4_temporal_continuity.py
run_stage39_phase39_5_longform_scene_sequence_planner.py
run_stage39_phase39_6_branch_commit_rollback.py
run_stage39_phase39_7_emotional_pressure_valve.py
```

### 3.2 Concept Normalizer

역할:

```text
과거 자산을 stage-by-stage 파일 목록이 아니라 concept-by-concept 카드로 바꾼다.
```

출력:

```text
manifests/pre_stage40_lineage_manifest.json
docs/stages/stage_001_039_foundation.md
```

개념 카드 기본 필드:

```json
{
  "concept_id": "foundation.longform.series_arc_control",
  "stage_origins": ["STAGE22", "STAGE39"],
  "title": "Series Arc Control",
  "problem_solved": "장편 시즌 진행이 단기 장면 조합으로 붕괴하지 않도록 통제한다.",
  "source_evidence": [],
  "current_runtime_anchor": [],
  "current_test_anchor": [],
  "current_gate_anchor": [],
  "survival_status": "PARTIAL",
  "missing_runtime_work": [],
  "promotion_priority": "HIGH"
}
```

### 3.3 Current Anchor Resolver

역할:

```text
과거 개념이 현재 active repo에서 어디에 계승되었는지 찾는다.
```

현재 앵커 후보:

```text
src/v1700/*
tests/*
docs/*
manifests/*
release/current/*
```

앵커 분류:

```text
runtime anchor
gate anchor
test anchor
documentation anchor
release evidence anchor
```

판정 원칙:

```text
문서만 있으면 DOCUMENTED_ONLY
테스트만 있으면 LIVE_GATE_ONLY가 아니라 PARTIAL
실행 경로와 테스트가 모두 있으면 LIVE_RUNTIME
현행 구조와 충돌하면 DEFERRED 또는 REJECTED_WITH_REASON
```

### 3.4 Survival Matrix

역할:

```text
각 개념이 실제로 살아 있는지, 반쯤 살아 있는지, 문서상만 남았는지 냉정하게 판정한다.
```

출력:

```text
docs/generated/wiki/foundation_lineage_wiki.md
docs/generated/skills/foundation_lineage_skill.md
```

상태 분류:

```text
LIVE_RUNTIME
LIVE_GATE_ONLY
PARTIAL
DOCUMENTED_ONLY
DEFERRED
REJECTED_WITH_REASON
UNKNOWN_NEEDS_REVIEW
```

### 3.5 Organic Impact Review

역할:

```text
향후 기능 추가나 수정이 들어올 때,
그 변경이 어떤 과거 개념과 연결되며 무엇을 깨뜨릴 수 있는지 먼저 보고하게 한다.
```

출력:

```text
docs/runbooks/organic_impact_review_protocol.md
manifests/change_impact_review_template.json
```

템플릿 핵심 필드:

```text
change_intent
related_stage_origins
related_concepts
affected_runtime_modules
affected_tests
affected_gates
node_authority_risks
reveal_leakage_risks
provider_cost_risks
graphnexus_context
graphnexus_impact
rollback_plan
promotion_decision
```

### 3.6 Pre-Stage40 Survival Gate

역할:

```text
필수 초기 개념이 계보 매니페스트에서 사라졌거나,
LIVE/PARTIAL 개념에 source evidence 또는 현재 앵커가 누락되면 실패한다.
```

구현 대상:

```text
src/v1700/gates/pre_stage40_survival_gate.py
tools/run_pre_stage40_survival_gate.py
tests/test_stage72_3_pre_stage40_survival_gate.py
```

## 4. GraphNexus 확장 설계

`Stage72.2`의 GraphNexus 도구는 현재 코드 구조를 본다.
`Stage72.3`은 그 위에 계보 레이어를 얹는다.

제안 모듈:

```text
src/v1700/graph_nexus/tools/foundation_lineage.py
src/v1700/graph_nexus/tools/concept_impact.py
src/v1700/graph_nexus/tools/survival_matrix.py
src/v1700/graph_nexus/tools/change_review.py
```

역할:

```text
foundation_lineage.py
  -> 역사 개념 카드 읽기

concept_impact.py
  -> 특정 변경이 어떤 과거 개념과 얽히는지 계산

survival_matrix.py
  -> 현재 생존 상태 계산

change_review.py
  -> 변경 검토 패킷 생성
```

## 5. 현재 로직과의 유기적 연결

### 5.1 Node1

Node1은 다음 개념군과 직접 연결된다.

```text
series arc control
episode progression
scene-sequence planning
temporal continuity
pressure relief timing
```

따라서 Node1 관련 변경은 `장편 구조 계보`를 반드시 참조해야 한다.

### 5.2 Node2

Node2는 다음 개념군과 직접 연결된다.

```text
literary quality engine
style evolution memory
anti-LLM prose control
reader-facing prose renderer
```

따라서 Node2 관련 변경은 `문체 계보`와 `노출 금지 경계`를 함께 검토해야 한다.

### 5.3 Node3

Node3는 다음 개념군과 직접 연결된다.

```text
boundary registry
concept validation workbench
release candidate gate
reveal leakage check
provider cost safety
```

따라서 Node3 변경은 곧 릴리스 신뢰도와 연결된다.

## 6. 단계별 구현 설계

### Phase 0. Baseline Lock

```text
Stage72.2 release gate pass
main release gate pass
pytest green
GitNexus alias check
```

### Phase 1. Evidence Index Build

```text
raw evidence scan
artifact class tagging
stage-origin tagging
```

### Phase 2. Concept Recovery

```text
20개 이상 high-value concept card 작성
각 concept에 source evidence 연결
```

### Phase 3. Survival Mapping

```text
현재 runtime/test/gate/doc anchor 매핑
LIVE/PARTIAL/DOCUMENTED_ONLY 판정
```

### Phase 4. Governance Integration

```text
impact review protocol 작성
change review template 추가
pre-stage40 survival gate 구현
```

### Phase 5. Release Readiness

```text
generated wiki/skill 생성
developer handoff report 작성
패키징 여부 최종 판정
```

## 7. 승인 기준

`Stage72.3`은 아래 조건을 충족할 때만 완료로 본다.

```text
at least 20 foundation concepts classified
all concepts have source evidence
all LIVE/PARTIAL concepts have current anchors
pre-stage40 survival gate pass
organic impact review protocol exists
Stage72.2 release gate still pass
main release gate still pass
pytest green
provider default calls remain 0
Node2 raw reveal access remains 0
```

## 8. 설계 결론

이 설계는 개발을 과거로 되돌리자는 제안이 아니다.

오히려 다음을 가능하게 하는 전진 설계다.

```text
더 빠르게 개발하되
더 적게 잃고
더 명확하게 승격한다.
```

`Stage72.3`이 끝나면,
다음 대형 단계인 장편 시즌 실행 엔진은
과거 철학의 복원 여부를 따지는 단계가 아니라,
복원된 철학 위에서 실제 기능을 확장하는 단계로 갈 수 있다.
