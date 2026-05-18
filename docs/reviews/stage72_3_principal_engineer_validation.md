# Stage72.3 Principal Engineer Validation

## 1. 검증 목적

최고 프린시펄 엔지니어는 다음 세 문서를 상호 검토했다.

```text
docs/proposals/stage72_3_pre_stage40_lineage_recovery_proposal.md
docs/proposals/stage72_3_three_expert_council_proposal.md
docs/architecture/stage72_3_foundation_lineage_recovery_blueprint.md
```

검증 초점은 다음과 같다.

```text
1. 전체 로직과 충돌하지 않는가?
2. Stage72.2 GraphNexus 체계와 유기적으로 연결되는가?
3. 문서화에 그치지 않고 실제 게이트와 릴리스 절차로 이어지는가?
4. 후속 장편 엔진 개발을 위한 기반으로 충분한가?
```

## 2. 총평

검증 결론:

```text
승인 가능.
단, "증거 수준"과 "생존 판정 기준"을 설계에 명시적으로 추가해야 한다.
```

`Stage72.3`은 현재 프로젝트의 가장 오래된 약점 하나를 정확히 겨냥한다.

그 약점은 다음과 같다.

```text
각 스테이지는 의미가 있었지만,
그 의미가 지금 코어 안에서 어디에 살아 있는지
항상 같은 기준으로 검증하지는 못했다.
```

이 문제가 반복되면,
앞으로도 새 패치가 과거 패치를 덮고,
나중에 다시 복원하는 개발 습관이 남는다.

`Stage72.3`은 그 반복을 끊는 데 적합하다.

## 3. 강점 검증

### 3.1 Stage72.2와의 연결성이 좋다

`Stage72.2`는 다음을 이미 제공한다.

```text
query
context
impact
detect_changes
route_map
tool_map
shape_check
```

`Stage72.3`은 이 토대 위에서
`현재 구조 영향 분석`을 `역사 계보 영향 분석`으로 확장한다.

이는 중복 개발이 아니라 자연스러운 계승이다.

### 3.2 active repo와 knowledge base의 역할 분리가 좋다

제안은 과거 파일 전체를 active repo에 복사하지 않는다.

대신 다음과 같이 구분한다.

```text
knowledge base:
역사 증거 저장소

active repo:
현재 실행 가능한 제품 코어

Stage72.3:
둘 사이의 해석 가능한 계보층
```

이 분리는 매우 중요하다.

### 3.3 다음 대형 단계의 선행조건으로 타당하다

사용자의 장기 목표는
유기적 씬-시퀀스 연산을 포함하는 장편 창작기다.

그 목표는 이미 과거 단계에서 여러 조각으로 설계되었다.

```text
series arc
scene-sequence planning
temporal continuity
branch commit/rollback
emotional pressure valve
style evolution memory
```

이들을 다시 정렬하지 않고 다음 대형 기능으로 넘어가면,
설계가 축적되지 않고 병렬 파편화될 수 있다.

따라서 `Stage72.3 -> 다음 장편 실행 단계` 순서는 논리적으로 옳다.

## 4. 발견된 보완 요구

### 4.1 Evidence Level을 추가해야 한다

현재 설계는 source evidence를 요구하지만,
증거의 강도를 구분하지 않는다.

다음 계층을 추가하는 것이 적절하다.

```text
E1_DOCUMENT
설계 문서나 설명서에만 존재

E2_ARTIFACT
매니페스트, 리포트, 샘플 산출물이 존재

E3_EXECUTABLE
실행 스크립트나 모듈이 존재

E4_TESTED
과거 또는 현재 테스트 증거가 존재

E5_LIVE_CURRENT
현재 active repo에서 runtime/test/gate 중 하나 이상에 연결
```

이 분류가 있어야
“이 개념은 존재했다”와 “이 개념은 검증되었다”를 구분할 수 있다.

### 4.2 Survival Status와 Evidence Level을 분리해야 한다

다음 둘은 다른 질문이다.

```text
Evidence Level:
과거에 얼마나 뚜렷하게 존재했는가?

Survival Status:
현재 V1700 안에서 얼마나 살아 있는가?
```

두 값을 섞으면 판정이 흐려진다.

예:

```text
Stage39 temporal continuity
Evidence Level: E4_TESTED
Survival Status: PARTIAL
```

이런 식의 분리가 필요하다.

### 4.3 Survival Gate의 실패 조건을 엄격히 정해야 한다

`pre_stage40_survival_gate`는 단지 파일 존재 여부를 보면 안 된다.

최소한 아래를 검사해야 한다.

```text
1. 필수 concept_id 집합이 누락되지 않았는가
2. source evidence가 비어 있지 않은가
3. LIVE/PARTIAL concept에 current anchor가 있는가
4. high-priority concept이 UNKNOWN 상태로 방치되지 않았는가
5. current anchor가 삭제된 경우 영향 검토 레코드가 있는가
```

### 4.4 개념군 우선순위는 현재 순서가 옳다

프린시펄 엔지니어는 아래 순서를 승인한다.

```text
1. 장편 생성 구조
2. 문체와 독자 체감
3. 검증과 경계
4. 제공자 라우팅과 비용 통제
```

특히 장편 생성 구조가 먼저인 이유는 명확하다.

```text
문체 개선은 지속 가능하다.
그러나 전체 구조를 잘못 잡으면
나중에 더 큰 재작성 비용이 든다.
```

### 4.5 자동 통합의 유혹을 막아야 한다

과거 지식 기반 안에는
현재에 바로 이식하면 오히려 구조를 흐릴 수 있는 코드도 있다.

따라서 설계는 다음 원칙을 명시해야 한다.

```text
No blind restore.
No automatic legacy merge.
Concept first, code later.
```

## 5. 전체 로직과의 충돌 검토

### 5.1 Node Authority

문제 없음.

`Stage72.3`은 Node1, Node2, Node3 권한 분리를 약화시키지 않는다.
오히려 어떤 초기 개념이 어느 노드와 결합되는지 더 선명하게 만든다.

### 5.2 Provider Cost Safety

문제 없음.

`Stage72.3`은 기본적으로 문서, 매니페스트, 게이트 중심 단계다.
기본 실행 경로에서 외부 provider 호출을 늘릴 이유가 없다.

### 5.3 Reveal Safety

문제 없음.

Node2 계보 복원 시에도
raw reveal 금지 규칙은 기존과 동일하게 유지되어야 한다.

### 5.4 Release Gate Flow

보완 필요.

최종적으로는 다음 흐름이 바람직하다.

```text
Stage72.2 release gate
  -> Stage72.3 pre-stage40 survival gate
  -> main release gate
  -> packaging eligibility
```

## 6. 추가 제안

프린시펄 엔지니어는 아래 두 가지 추가 산출물을 권고한다.

### 6.1 Foundation Evidence Policy

문서:

```text
docs/runbooks/foundation_evidence_policy.md
```

내용:

```text
evidence level 정의
survival status와의 구분
concept card 작성 최소 기준
```

### 6.2 Change Review Decision Matrix

문서:

```text
docs/runbooks/change_review_decision_matrix.md
```

내용:

```text
승인
조건부 승인
보류
복원 선행
폐기
```

이 문서가 있으면,
후속 스테이지에서 “무엇을 먼저 해야 하는가”를 빠르게 판정할 수 있다.

## 7. 최종 검증 결론

프린시펄 엔지니어의 최종 판정:

```text
Stage72.3 설계는 논리적으로 타당하다.
Stage72.2와도 자연스럽게 결합된다.
다음 장편 실행 단계 전에 반드시 수행할 가치가 있다.
```

단, 아래 세 보완을 최종 합의안에 반영해야 한다.

```text
1. Evidence Level 도입
2. Survival Status와 Evidence Level 분리
3. Survival Gate 실패 조건 명문화
```
