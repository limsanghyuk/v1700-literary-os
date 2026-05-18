# Stage72.3 Consensus Roadmap

## 1. 최종 합의

최고 수석 아키텍처, 최고 수석 컴파일러, 최고 프린시펄 엔지니어는
`Stage72.3`을 다음과 같이 최종 정의한다.

```text
Stage72.3 - Foundation Lineage Recovery and Organic Impact Governance
```

최종 목적:

```text
Stage01-39의 핵심 개념을 현재 V1700의 실행 구조에 다시 연결하고,
앞으로의 변경이 그 유산을 훼손하지 못하도록
영향 검토와 생존 게이트를 릴리스 절차에 포함한다.
```

## 2. 합의된 설계 원칙

```text
1. 과거 파일을 그대로 복원하지 않는다.
2. 과거 개념을 먼저 구조화한다.
3. 현재 생존 여부를 runtime/test/gate/doc anchor로 판정한다.
4. evidence level과 survival status를 분리한다.
5. 다음 대형 기능 개발 전, 계보 복원과 영향 통치를 선행한다.
6. 미래의 major change는 organic impact review 없이는 승격하지 않는다.
```

## 3. 최종 데이터 모델

### 3.1 Evidence Level

```text
E1_DOCUMENT
E2_ARTIFACT
E3_EXECUTABLE
E4_TESTED
E5_LIVE_CURRENT
```

### 3.2 Survival Status

```text
LIVE_RUNTIME
LIVE_GATE_ONLY
PARTIAL
DOCUMENTED_ONLY
DEFERRED
REJECTED_WITH_REASON
UNKNOWN_NEEDS_REVIEW
```

### 3.3 Concept Card 필수 필드

```text
concept_id
stage_origins
title
problem_solved
source_evidence
evidence_level
current_runtime_anchor
current_test_anchor
current_gate_anchor
survival_status
missing_runtime_work
promotion_priority
review_notes
```

## 4. 단계별 로드맵

### Phase 0. Baseline Lock

목적:

```text
현재 Stage72.2가 정상 기준선임을 다시 고정한다.
```

실행:

```text
python tools/run_stage72_2_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
gitnexus list
```

완료 조건:

```text
Stage72.2 gate pass
main release gate pass
pytest green
GitNexus alias 확인
```

### Phase 1. Historical Evidence Scan

목적:

```text
Stage01-39의 증거 파일을 raw evidence index로 만든다.
```

주요 산출물:

```text
manifests/pre_stage40_raw_evidence_index.json
```

완료 조건:

```text
Stage01-39 관련 문서, 매니페스트, 테스트, 실행 스크립트가 인덱싱된다.
evidence candidate 수가 기록된다.
```

### Phase 2. Foundation Concept Recovery

목적:

```text
고가치 개념을 concept card로 정규화한다.
```

주요 산출물:

```text
manifests/pre_stage40_lineage_manifest.json
docs/stages/stage_001_039_foundation.md
```

우선 회수 개념군:

```text
longform generation
literary/style quality
governance and boundary
provider routing and cost safety
```

완료 조건:

```text
20개 이상 high-value concept 분류
각 concept에 stage origin과 source evidence 존재
evidence level 부여 완료
```

### Phase 3. Current Survival Mapping

목적:

```text
각 개념이 현재 V1700 어디에 살아 있는지 판정한다.
```

주요 산출물:

```text
docs/generated/wiki/foundation_lineage_wiki.md
docs/generated/skills/foundation_lineage_skill.md
```

완료 조건:

```text
LIVE/PARTIAL 개념에 current anchor 존재
DOCUMENTED_ONLY와 LIVE_RUNTIME이 명확히 분리
high-priority UNKNOWN concept이 방치되지 않음
```

### Phase 4. Organic Impact Governance

목적:

```text
미래 변경이 계보를 끊지 않도록 검토 프로토콜을 의무화한다.
```

주요 산출물:

```text
docs/runbooks/organic_impact_review_protocol.md
docs/runbooks/foundation_evidence_policy.md
docs/runbooks/change_review_decision_matrix.md
manifests/change_impact_review_template.json
```

완료 조건:

```text
변경 검토 템플릿이 stage origins, affected concepts, tests, gates, rollback plan을 요구
evidence level과 survival status 사용 규칙이 정의됨
승인/조건부 승인/보류/복원 선행/폐기 판정 규칙이 문서화됨
```

### Phase 5. Survival Gate Implementation

목적:

```text
계보 복원을 릴리스 절차에 실제로 연결한다.
```

주요 산출물:

```text
src/v1700/gates/pre_stage40_survival_gate.py
tools/run_pre_stage40_survival_gate.py
tests/test_stage72_3_pre_stage40_survival_gate.py
```

게이트 실패 조건:

```text
required concept_id 누락
source evidence 누락
LIVE/PARTIAL concept의 current anchor 누락
high-priority concept이 UNKNOWN_NEEDS_REVIEW 상태로 남음
anchor 삭제 후 impact review record 부재
```

완료 조건:

```text
survival gate pass
게이트 실패 케이스 테스트 존재
release gate chain에 편입 가능
```

### Phase 6. Release Readiness and Handoff

목적:

```text
Stage72.3을 다음 개발 단계가 실제로 의지할 수 있는 기준선으로 고정한다.
```

주요 산출물:

```text
release/current/stage72_3_developer_handoff_report.md
packages/v1700_stage72_3/*
```

완료 조건:

```text
Stage72.2 gate pass
Stage72.3 survival gate pass
main release gate pass
pytest green
provider default calls 0
Node2 raw reveal access 0
패키징 적합성 판정 완료
```

## 5. 이후 발전 방향과 연결

3인의 최종 합의는 다음과 같다.

```text
Stage72.3 이후의 다음 대형 기능 단계는
"장편 시즌 실행 엔진"이어야 한다.
```

그 이유는,
Stage72.3에서 복원하는 최상위 개념들이
바로 이 기능의 이론적 선행조건이기 때문이다.

예상되는 다음 단계 주제:

```text
season/episode/sequence/scene organic planner
temporal state ledger reintegration
branch commit/rollback runtime revival
emotional pressure wave controller
Node2 style memory reintegration for longform prose
```

단, 위 기능은 `Stage72.3` 완료 뒤
복원된 계보 매니페스트와 impact review 규칙을 참조해 진행한다.

## 6. 최종 판정

```text
Stage72.3은 선택 사항이 아니라,
이 프로젝트가 더 이상 과거 패치를 잃지 않기 위한 필수 구조 보강이다.
```

3인 합의 결론:

```text
설계 승인.
로드맵 승인.
다음 실행 단계는 Stage72.3 Phase 0부터 순차 진행.
```
