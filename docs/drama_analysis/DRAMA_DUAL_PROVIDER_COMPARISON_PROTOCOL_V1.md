# GPT×Claude 이중저작 비교 프로토콜 v1

- Document ID: `DRAMA-DUAL-PROVIDER-COMPARISON-V1`
- Status: `AUTHORITATIVE_CANDIDATE`

## 1. 목적

각 모델의 내부 분석 방식은 유지하면서, 동일 원본·동일 장면 경계·동일 스키마로 독립 저작한 결과를 비교해 사실 오류, 규격 결함, 유효한 해석 차이를 분리한다.

## 2. 독립성 규칙

```text
공통 SourceLock과 계약 배포
→ GPT 독립 저작
→ Claude 독립 저작
→ 각자 Gate A/B 통과
→ 각자 RUN_LOCKED
→ 상대 row-level 데이터 공개
→ full outer join 비교
```

잠금 전 상대의 행 단위 결과를 읽지 않는다. 설계 문서나 공통 계약을 공유하는 것은 허용하지만, 실제 정답 행을 공유하면 blind 비교가 아니다.

## 3. 공통 고정 항목

- source archive SHA
- canonical logical scene boundary
- SourceSceneAlignment schema
- exact row keyset·enum
- character_key 규칙
- 계산식
- 검증기 버전
- comparison key

모델별 에이전트 수·내부 메모·분업 방식은 다를 수 있다.

## 4. 비교 단위

### EntityBridge

- canonical_name/alias 정규화
- 장소·조직 오등록
- 동일 인물 분리·서로 다른 인물 병합

### CastPresence

공식 full outer join key:

```text
work_id, episode_no, scene_no, normalized_entity_key
```

판정:

```text
BOTH_PRESENT_LABEL_MATCH
BOTH_PRESENT_LABEL_MISMATCH
GPT_ONLY_DETECTION
CLAUDE_ONLY_DETECTION
BOTH_ABSENT_NOT_MATERIALIZED
ENTITY_MAPPING_UNRESOLVED
```

### CharacterLoad

CastPresence 합의본에서 결정론으로 다시 계산한다. 두 모델의 Load 숫자를 평균하지 않는다.

## 5. 오류와 해석 차이 분리

### 사실/계약 오류

- 원본에 없는 인물
- 실제 등장 인물 누락
- speaking 여부의 명백한 오판
- 장면 번호·FK 오류
- enum/계산식 위반

원본 재대조로 하나를 교정한다.

### 유효한 해석 차이

- PRIMARY와 SECONDARY focality
- 장면의 중심이 복수일 때의 강조 차이
- alias 표기의 선택

원본 근거와 창작 활용성을 비교해 합의 또는 dissent를 유지한다.

## 6. 정량 지표

조건부 κ만으로 완료 판정하지 않는다.

필수:

```text
character detection precision/recall/F1
scene-level character set Jaccard
presence_mode agreement + Cohen κ 또는 Gwet AC1
speaking_status conditional agreement
focality conditional agreement
critical omission rate
entity normalization unresolved rate
```

클래스 불균형이 크므로 κ와 함께 F1/Jaccard를 보고한다.

## 7. adjudication

각 불일치에 다음을 기록한다.

```text
comparison_id
source_ref
GPT_value
Claude_value
disagreement_type
adjudication_evidence
final_value
decision_status
by
```

권장 상태:

```text
GPT_ONLY
CLAUDE_ONLY
BOTH_AGREED
BOTH_CORRECT_DIFFERENT_EMPHASIS
USER_DECIDED
UNRESOLVED_HOLD
```

자동 majority vote, union, average, last-write-wins는 금지한다.

## 8. 최종 산출물

```text
PHASE_COMPARISON_MATRIX
CONSENSUS_AND_DISSENT_LEDGER
FINAL_CONSENSUS_CONTRACT
CONSENSUS_GOLD_DATA
```

`CONSENSUS_GOLD_DATA`는 양측 run을 보존한 별도 lineage이며 어느 한쪽 run을 덮어쓰지 않는다.

## 9. 역할 구조

현재 Literary OS 프로젝트에서는:

- Claude: 기존 드라마 분석 방법론과 계층 설계의 주 작성자.
- GPT: 독립 원본독해, 반례 탐지, 규격·계산·근거 감사.
- Claude: 양측 결과를 기반으로 통합안 작성 가능.
- GPT: 통합안 재감사.
- 사용자: 최종 권위와 canonical 승인.

이 역할은 결과를 자동으로 Claude 우선값으로 정한다는 뜻이 아니다. 원본 근거와 계약을 우선한다.
