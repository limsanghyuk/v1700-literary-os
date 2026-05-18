# Stage72.3 Three-Expert Council Proposal

## 1. 제안의 핵심

`Stage72.3`의 목적은 단순한 과거 문서 정리가 아니다.

이번 단계의 본질은 다음과 같다.

```text
Stage01-39에서 태어난 핵심 개념을
현재 V1700 런타임, 테스트, 게이트, 문서 체계와 다시 연결하고,
앞으로의 모든 변경이 그 계보를 끊지 않도록
GitNexus식 영향 분석 절차를 개발 프로세스 자체에 내장한다.
```

즉, `Stage72.3`은 새 기능 하나를 추가하는 개발 단계가 아니라,
앞으로의 개발이 과거의 유산을 잃지 않게 만드는 `계보 복원 + 영향 통치` 단계다.

## 2. 논의에 참여한 세 역할

### 2.1 최고 수석 아키텍처

최고 수석 아키텍처의 판단은 다음과 같다.

```text
현재 active repo는 깨끗하고 강하다.
그러나 Stage01-39의 철학, 구조, 통제 원리 상당수가
형식적으로는 현재 계보 매니페스트 밖에 놓여 있다.
```

그 결과 다음의 문제가 반복될 수 있다.

```text
1. 지금 눈앞의 문제를 해결하는 패치가 들어온다.
2. 과거 핵심 개념 하나가 조용히 우회된다.
3. 수 단계 뒤, 누락된 논리를 다시 복원하느라 되돌아간다.
```

최고 수석 아키텍처는 이를 `개발 계보 단절 문제`로 규정한다.

그는 특히 아래 개념군의 복원을 우선시해야 한다고 본다.

```text
장편 구조:
Stage21 episode draft export
Stage22 series arc control
Stage39 longform scene-sequence planner
Stage39 temporal continuity
Stage39 emotional pressure valve

문체와 독자 체감 품질:
Stage14 Node2 literary quality engine
Stage15 literary depth calibration
Stage23 Node2 style evolution memory

거버넌스와 검증:
Stage17 review workflow
Stage18 human/agent review console
Stage24 boundary registry
Stage25 release candidate gate
Stage26-28 regression stream
Stage33 concept validation workbench

멀티 어댑터와 비용 통제:
Stage10 provider comparison
Stage11 provider tracing
Stage40 provider route
Stage54 routing
Stage58 provider safety
```

### 2.2 최고 수석 컴파일러

최고 수석 컴파일러의 판단은 다음과 같다.

```text
과거 자산을 다시 끌어오는 일은 "파일 복사"가 아니다.
반드시 machine-readable 구조로 재컴파일해야 한다.
```

그는 아래 원칙을 제안한다.

```text
1. 과거 개념은 concept card로 정규화한다.
2. 각 concept card는 source evidence를 반드시 가진다.
3. 각 개념은 현재 runtime/test/gate/doc anchor와 매핑된다.
4. 살아 있는 개념과 문서상 개념을 구분한다.
5. 앞으로의 변경은 concept impact review를 거쳐야 한다.
```

컴파일러 관점에서 필요한 산출물은 다음과 같다.

```text
manifests/pre_stage40_raw_evidence_index.json
manifests/pre_stage40_lineage_manifest.json
docs/stages/stage_001_039_foundation.md
docs/generated/wiki/foundation_lineage_wiki.md
docs/generated/skills/foundation_lineage_skill.md
docs/runbooks/organic_impact_review_protocol.md
manifests/change_impact_review_template.json
src/v1700/gates/pre_stage40_survival_gate.py
tools/run_pre_stage40_survival_gate.py
tests/test_stage72_3_pre_stage40_survival_gate.py
```

또한 컴파일러는 다음 분류 체계를 제시한다.

```text
LIVE_RUNTIME
LIVE_GATE_ONLY
PARTIAL
DOCUMENTED_ONLY
DEFERRED
REJECTED_WITH_REASON
UNKNOWN_NEEDS_REVIEW
```

이 분류가 있어야만,
“그 개념은 정말 현재 실행 경로에 살아 있는가?”라는 질문에
문서 감상이 아니라 판정으로 답할 수 있다.

## 3. 공동 진단

두 전문가는 다음 사항에 합의했다.

### 3.1 Stage72.2만으로는 충분하지 않다

`Stage72.2`는 GitNexus의 원리를 현재 코드 구조 분석에 흡수했다.

```text
query
context
impact
detect_changes
route_map
tool_map
shape_check
generated skills
deterministic wiki
```

그러나 이 기능들은 아직 `현재 코드베이스` 중심이다.

`Stage72.3`은 이 능력을 `프로젝트 역사 전체`로 확장해야 한다.

```text
현재 코드 그래프
  + 과거 단계 계보
  + 현재 생존 앵커
  + 누락 개념
  + 변경 영향 검토
```

### 3.2 Stage01-39는 폐기물이 아니라 창작기 원형이다

Stage01-39는 단지 오래된 실험이 아니다.
이 구간은 현재 문학 생성기의 여러 핵심 이론이 처음 형성된 원형 구간이다.

실제 근거 예시는 다음과 같다.

```text
series_arc_planner.py
series_arc_contract.py
style_evolution_analyzer.py
style_evolution_contract.py
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

이들은 다음 문제를 직접 다룬다.

```text
장편 시즌 아크
씬-시퀀스 유기 연산
문체 진화 메모리
시간 상태 연속성
브랜치 commit/rollback
감정 압력 해소
개념 검증 워크벤치
```

이는 사용자가 오랫동안 강조한 핵심 철학과 정확히 맞물린다.

## 4. 제안되는 개발 방향

### 4.1 Stage72.3의 정식 명명

```text
Stage72.3 - Foundation Lineage Recovery and Organic Impact Governance
```

한국어 설명:

```text
초기 단계 계보 복원 및 유기적 영향 통치 체계 구축
```

### 4.2 핵심 목표

```text
1. Stage01-39의 핵심 개념을 구조화한다.
2. 현재 V1700 내부에 살아 있는 지점을 찾는다.
3. 사라졌거나 부분 생존한 개념을 분류한다.
4. 후속 변경이 계보 단절을 일으키지 못하도록 영향 검토를 의무화한다.
5. 향후 장편 엔진 고도화 전에 바닥 계보를 잠근다.
```

### 4.3 개발 원칙

```text
Do:
개념 복원
현재 생존성 판정
게이트화
영향 보고서화
릴리스 승격 절차와 연결

Do not:
과거 파일을 무차별 복사
구형 코드를 그대로 active repo에 이식
문서만 늘리고 runtime anchor를 만들지 않기
영향 분석 없이 다음 창작 엔진 단계로 넘어가기
```

## 5. 우선 복원 순서

### 5.1 1순위: 장편 생성 구조

```text
Stage21
Stage22
Stage39
```

판단 이유:

```text
사용자의 중심 목표는 단문 렌더러가 아니라
유기적으로 씬과 시퀀스를 연산하는 장편 창작기다.
```

### 5.2 2순위: 문체와 독자 체감

```text
Stage14
Stage15
Stage23
```

판단 이유:

```text
사용자가 가장 직접적으로 체감하는 품질은 문체다.
문체가 얇으면 구조가 좋아도 제품은 약하게 느껴진다.
```

### 5.3 3순위: 검증과 경계

```text
Stage24
Stage25
Stage26-28
Stage33
```

판단 이유:

```text
계보 복원은 결국 승격 절차와 검증 체계 안으로 들어가야 한다.
```

### 5.4 4순위: 제공자 라우팅과 비용 통제

```text
Stage10
Stage11
Stage40
Stage54
Stage58
```

판단 이유:

```text
멀티 어댑터 철학은 후속 제품화에서 필수다.
```

## 6. 제안 결론

두 전문가는 다음의 결론에 합의했다.

```text
다음 대형 창작 기능 개발 전에 Stage72.3을 먼저 진행한다.
Stage72.3은 개발 속도를 늦추는 절차가 아니라,
이미 만들어 둔 철학과 효용을 다시 잃지 않게 만드는 가속 장치다.
```

정식 제안:

```text
Stage72.3을 즉시 실행 대상으로 승인한다.
Stage72.3 완료 전에는 대규모 장편 실행 엔진 확장을 보류한다.
단, 문서화와 생존성 판정에 필요한 최소 도구 구현은 Stage72.3 범위 안에서 허용한다.
```
