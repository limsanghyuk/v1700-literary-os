# 새 대화창 한국 드라마 분석 즉시 실행 가이드 v3

- Document ID: `DRAMA-NEW-CONVERSATION-EXECUTION-GUIDE-V3`
- Status: `AUTHORITATIVE`
- Updated: 2026-07-17
- Exact schema authority: `SCHEMA_CONTRACTS_V2.md`
- Replaces for execution: `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md`
- Incident basis: `스타일` V1 structural-pass / semantic-fail and V2 reauthor

## 0. 새 대화창 최소 로드

새 대화창은 다음만 읽고 즉시 실행한다.

1. 이 문서
2. `SCHEMA_CONTRACTS_V2.md`
3. 신규 작품 선정 시에만 최신 DB 상태 또는 작품 인덱스 1개
4. 중단 작업 재개 시에만 해당 작품 compact checkpoint 1개

과거 대화 전체, 모든 세션 README, 모든 방법론 문서를 시작 전에 전수 조사하지 않는다. 충돌·품질 감사·계약 변경이 발생할 때만 관련 전문 문서를 부분 조회한다.

## 1. 완료 판정의 이중 권위

```text
STRUCTURAL_PASS
+ SEMANTIC_QUALITY_PASS
+ PACKAGE_FRESH_EXTRACTION_PASS
= PASS_CANDIDATE
```

- 구조 PASS만으로 의미 품질 PASS를 선언하지 않는다.
- 파일·checkpoint·validator exit code가 채팅 보고보다 우선한다.
- 사용자 승인 전 `CANONICAL`로 승격하지 않는다.
- 하나라도 실패하면 `FAIL_SEMANTIC_REVIEW_REQUIRED` 또는 `SOURCE_HOLD`로 둔다.

## 2. 속도와 품질의 절대 규칙

```text
의미 저작 최소 단위 = quarter
의미 저작 원자 단위 = 1 episode
결정론적 직렬화 묶음 = 최대 4 episodes
강검증 블록 = 전반부 또는 약 8 episodes
Stage04 = full-series fan-in 1회
Fresh extraction = 최종 작품 ZIP 1회 + 최종 DB ZIP 1회
```

- Python·템플릿으로 의미 필드를 생성하지 않는다.
- 여러 회차 원문을 한 번에 넣어 의미 레코드를 일괄 생성하지 않는다.
- 이미 검증된 회차를 습관적으로 다시 읽지 않는다.
- quarter checkpoint 없이 반 시즌이 완성되거나 동일 문장 골격이 대량 반복되면 속도 이상 감사를 실행한다.
- 수량 할당량을 채우기 위해 Arc·Edge·Payoff를 만들지 않는다.

## 3. 신규 작품 선정과 SourceLock

```text
원본 아카이브 inventory
→ 최신 DB 작품 인덱스와 차집합
→ 회차 완전성·인코딩·중복 판본·재수록 구간·장면 경계 비교
→ 원본 안정성이 가장 높은 신규 작품 1편
```

다음은 `SOURCE_HOLD`다: 실제 회차 누락, 충돌 판본, 장면 경계 잠금 실패, 위장 회차, 인코딩 복구 불가.

SourceLock 최소 항목:

- 작품명·실제 회차 번호
- 원본 바이트 SHA256
- 정규화 UTF-8 파일 SHA256
- canonical `scene_no=1..N`
- 회차별 장면 수와 Q1~Q4 범위
- 중복·재수록·제외 장면 대응표
- source marker anomaly
- `python_semantic_generation:false`
- `next_pointer`

## 4. 장면 경계와 Quarter 분할

1. HWP/TXT의 물리 장면 표식, 문단 스타일, 번호형 heading을 조사한다.
2. 장소·시간·행동 단위가 실제로 바뀌는 논리 장면을 확정한다.
3. 회차 간 재수록 장면은 후속 회차 정본에서 제외하고 SourceLock에 원본→정본 대응을 기록한다.
4. canonical ordinal은 `1..N` 연속이어야 한다.

Quarter는 극적 4막이 아니라 독해·영속화 단위다.

- 장면 경계를 자르지 않는다.
- 총 장면 수를 약 25%씩 균형 분할한다.
- 사건 덩어리를 깨지 않는다.
- 각 Quarter 종료 즉시 부분 Stage01, QuarterAudit, checksum을 저장한다.

## 5. 회차 실행 순서

```text
Q1 원문 직접독해 → Stage01 부분 저장 → QuarterAudit
Q2 원문 직접독해 → Stage01 부분 저장 → QuarterAudit
Q3 원문 직접독해 → Stage01 부분 저장 → QuarterAudit
Q4 원문 직접독해 → Stage01 완성 → QuarterAudit
→ EpisodeMeta
→ Stage02 SequenceBlueprint
→ EpisodeArc
→ Stage03 CharacterArc / RelationshipArc / LocalEdge / PayoffCandidate
→ 회차 경량 게이트
→ episode checkpoint
→ next_pointer 갱신
```

회차 하나를 읽을 때 Stage03 네 계층을 함께 작성하는 수직 처리를 사용한다. 계층별로 전 시즌을 반복해서 읽지 않는다.

## 6. Stage01 의미 해석

각 장면은 내부적으로 다음 여섯 질문에 답한다.

1. 실제 행동은 무엇인가.
2. 누가 어떤 전략을 쓰거나 무엇을 숨기고 피하는가.
3. 정보·오해·관계·권력 조건 중 무엇이 바뀌는가.
4. 누가 무엇을 선택·거부·유예하는가.
5. 회차 구조에서 이 장면의 기능은 무엇인가.
6. 어떤 구체적 잔여 압력이 다음 장면·시퀀스를 미는가.

이를 새 키로 추가하지 않고 `title`, `intent_gist`, `core/core2`, `skin`에 서로 다른 역할로 압축한다.

### 내용 깊이 0~4

- 0: 원문 불일치·환각·placeholder
- 1: 사건 또는 대사 요약만 있음
- 2: 행동 주체와 표면 목적은 있으나 선택·변화가 약함
- 3: 행동·전략·정보/관계 변화·구조 기능이 구체적임
- 4: 선택과 가치 이동, 잔여 인과 압력까지 원문 근거로 설명함

권장 게이트: 회차 평균 3.0 이상, 2.5 미만 장면 재검토, 0점·1점 장면 0건.

금지 패턴:

- 원문 파편을 제목에 기계적으로 접합
- 모든 `intent_gist`의 동일 종결 문장
- 인물명·장소명만 교체한 동일 골격
- 필드 간 동일 요약 복사
- 원문에 없는 인물·감정·인과
- 장문 대사 복사

## 7. Stage02 의미 밀도와 분할

시퀀스는 장면 수 균등분할이 아니다. 목표 주체, 목표, 장애 성격, 정보·관계·권력 가치, POV·장소 클러스터, 행동 계획 중 하나가 바뀌는 지점에서 경계를 둔다.

불변식:

- 모든 장면이 정확히 한 시퀀스에 포함
- 누락·중복 0
- `sum(scene_budget)==scene_count`
- `sum(runtime_share)==1.0 ± 1e-6`
- `sequence_count / scene_count >= 0.11`
- 권장 밀도 0.12~0.17
- 회차 내 `goal`, `obstacle`, `sequence_intent` 복사 금지

## 8. Stage03 저작 기준

### CharacterArc

- 인물×회차 단위
- trigger 장면에 해당 인물이 실제 등장
- `state_label`은 회차 종료 상태
- `state_delta`는 이번 회차 변화량
- 단순 등장 인물 생성 금지
- 고정 수량 금지

### RelationshipArc

- 관계쌍×회차 단위
- trigger 장면에 양쪽 인물이 함께 등장·통화·교신
- `(A,B)`와 `(B,A)` 중복 금지
- 신뢰·권력·정보·의존·적대 조건의 실제 변화만 기록

### LocalEdge

반사실 질문을 통과한 경우만 생성한다.

```text
source가 없었다면 target 사건이 발생하지 않거나 실질적으로 달라지는가?
```

필수: 동일 회차, `gap_episodes=0`, `edge_type=causal`, target core와 label 일치. 단순 인접·유사 감정·같은 시퀀스는 인과가 아니다.

감사 trigger: `LocalEdge / SceneCard > 0.10`, 바로 다음 장면 target 비율 `>0.50`. 자동 FAIL이 아니라 수동 선택성 감사 신호다.

### PayoffCandidate

장거리 회수 가능성이 구체적인 물건·정보·약속·위협·선택만 남긴다. 다음 장면에서 닫히는 문제나 회차 말이라는 이유만의 후보는 제외한다. 후보 수 할당량은 없다.

## 9. 회차 경량 게이트

1. JSON·JSONL 파싱
2. exact keyset·자료형·ID
3. SceneCard `1..N` coverage
4. Sequence partition·span·budget
5. runtime 합
6. Arc trigger·turning point·Edge 참조 존재
7. LocalEdge 동일 회차·gap 0·causal
8. 파일 존재·checkpoint checksum·next_pointer

경량 게이트에서는 전역 의미 중복, 앙상블 누락, 관계 역방향 전 시즌 스캔, LocalEdge 밀도, CrossEpisodeEdge, ZIP을 반복하지 않는다.

## 10. 블록 강검증

전반부 또는 약 8회차 종료 후 한 번 수행한다.

### 구조 강검증

- exact schema·enum·ID·FK
- SceneCard coverage
- Sequence partition·density·core_mix
- EpisodeArc act tiling·turning point
- ID 전역 유일성

### 의미 품질 강검증

- 원문 대비 title·intent 정확성
- exact semantic duplicate 0
- masked skeleton repetition 감사
- 동일 종결 템플릿·메타데이터 파생 흔적 0
- CharacterArc trigger participant
- RelationshipArc 양쪽 participant·역방향 중복 0
- 앙상블 변화 누락 감사
- LocalEdge 반사실 인과·밀도·인접성
- PayoffCandidate 구체 근거·중복

반복 판정:

- 중요 서술 필드의 exact duplicate는 원칙적으로 FAIL
- 인물명·장소명·ID·숫자를 마스킹한 동일 골격이 3회 이상이면 수동 감사
- 한 골격이 해당 필드의 5%를 넘거나 반복 레코드 총합이 15%를 넘으면 FAIL
- 짧은 상태 label은 예외가 가능하나 `delta`와 `evidence` 반복은 허용하지 않는다.

속도 이상 감사 trigger:

- QuarterAudit 없이 여러 회차가 한 번에 완성됨
- 모든 회차의 Arc 수가 기계적으로 동일함
- 모든 시퀀스가 회차별 동일 goal/obstacle을 공유함
- SceneCard 동일 문장 골격 대량 반복
- 구조 validator만 있고 semantic-quality report가 없음
- 분석 시간에 비해 직접독해 증빙과 checkpoint가 부족함

시간 자체로 실패시키지 않고 산출물 고유성·근거·계보로 판정한다.

## 11. 후반부·전 시즌·Stage04

```text
후반부 회차별 경량 게이트
→ 후반부 블록 구조+의미 강검증
→ 전 시즌 Stage01~03 통합 구조+의미 강검증
→ Stage04
```

Stage04 순서:

1. 모든 PayoffCandidate 목록화
2. 원 장면 재확인
3. 후속 회차 target 탐색
4. source/target 의미 대조
5. 후보 100% disposition
6. 검증된 연결만 CrossEpisodeEdge 승격
7. FullSeriesArc 재종합

금지:

- 이전 회 마지막 장면→다음 회 첫 장면 자동 브리지
- `EP n → EP n+2` 같은 규칙적 자동 배치
- 동일 note 복사
- 후보 일괄 승격
- 소수 target 장면에 근거 없는 엣지 집중

동일 target에 3건 이상 집중되면 각 모티프가 독립적으로 회수되는지 수동 감사한다.

## 12. 검증·패키징 분리

```text
Process A — validation-only
structural gate + semantic quality gate → VALIDATION_PASS

Process B — package-only
manifest·SHA256SUMS → ZIP → 별도 디렉터리 재해제
→ 실제 CLI 재실행 → pre/post tree 비교 → RELEASE_READY
```

최종 패키지에서만 Fresh Extraction을 한 번 실행한다.

## 13. 전체 DB 증분 편입

```text
이전 DB ZIP SHA·Fresh Extraction 검증서 계승
+ 신규 작품 structural validator
+ 신규 작품 semantic-quality validator
+ 신규 SourceLock
+ 전체 registry/source/encoding/database/release gate
+ 최종 DB ZIP Fresh Extraction
```

이전 tree가 바뀌지 않았다면 기존 작품의 무거운 의미 validator를 모두 재실행하지 않는다. validator 계약 변경, SHA 불일치, 증빙 부재일 때만 전체 재검증한다.

## 14. 완료 시 개발자 전달물

작품 분석 완료 시 기본적으로 다음을 함께 제공한다.

1. 개별 작품 Stage01~04 ZIP
2. 개별 작품 Fresh Extraction 검증서
3. 해당 작품을 편입한 최신 전체 DB ZIP
4. 전체 DB 최종 검증서
5. 각 ZIP SHA256
6. 작품·회차·SceneCard·Stage 계층 집계

사용자가 독립 패키지만 명시적으로 요청한 경우를 제외하고 개별 ZIP과 전체 DB ZIP을 같은 완료 보고에서 제공한다.

## 15. 증빙·격리·재작성

- 실패본을 삭제하거나 덮어쓰지 않는다.
- `lineage/quarantine` 또는 provenance에 실패 원인·대체본·supersession을 기록한다.
- 의미 결함은 자동 수정하지 않고 원문을 다시 읽어 새 버전으로 재저작한다.
- 운영 DB는 raw quarter 폴더를 제외하고 aggregate hash·독립 ZIP SHA·semantic report·incident lineage만 보존한다.

## 16. compact checkpoint

```json
{
  "work_id": "작품명",
  "source_lock_sha256": "...",
  "completed_episodes": [1,2,3],
  "next_pointer": "EP04_Q1",
  "current_phase": "FRONT_HALF_STAGE01_03",
  "last_light_gate": "EP03_LIGHT_PASS",
  "last_semantic_gate": null,
  "artifact_root": "...",
  "meaning_drafts_pending_serialization": []
}
```

## 17. 새 대화창 실행 요약

```text
V3 실행 가이드와 Schema Contracts V2를 읽는다.
최신 DB 인덱스로 신규 작품을 선정한다.
SourceLock과 canonical 장면 경계를 잠근다.
원문을 Quarter 순서로 직접 읽고 회차별 Stage01~03을 수직 작성한다.
회차마다 경량 게이트만 수행한다.
전반부·후반부·전 시즌 경계에서 구조와 의미 품질 강검증을 각각 수행한다.
Stage04는 모든 후보를 100% 처분하고 검증된 회수만 연결한다.
구조 PASS와 의미 PASS가 모두 있어야 작품을 완료로 선언한다.
최종 작품 ZIP과 편입된 전체 DB ZIP을 함께 제공한다.
```