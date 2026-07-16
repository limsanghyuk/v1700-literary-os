# 새 대화창 드라마 분석 즉시 실행 가이드 v2

- Document ID: `DRAMA-NEW-CONVERSATION-EXECUTION-GUIDE-V2`
- Status: `AUTHORITATIVE`
- Updated: 2026-07-17
- Exact schema authority: `SCHEMA_CONTRACTS_V2.md`
- Replaces for execution: `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md`

## 0. 목적

새 대화창은 프로젝트 전체, 과거 대화, 모든 방법론 문서를 다시 전수 조사하지 않는다. 다음 두 문서만 읽고 즉시 실행한다.

1. 이 문서
2. `SCHEMA_CONTRACTS_V2.md`

작품을 새로 선택할 때만 최신 DB 인덱스 또는 최신 `DRAMA_ANALYSIS_DATABASE_STATUS_*.json`을 추가로 읽는다. 중단 작업을 재개할 때만 해당 작품의 compact checkpoint JSON을 읽는다. 역사 문서·세션 README·비교평가 문서는 충돌이나 감사가 발생했을 때만 연다.

## 1. 절대 규칙

```text
의미 저작 최소 단위 = quarter
의미 저작 원자 단위 = 1 episode
결정론적 직렬화 묶음 = 최대 4 episodes
사용자 전달·강검증 블록 = 전반부 또는 약 8 episodes
Stage04 = full-series fan-in 1회
Fresh extraction = 최종 패키지 1회
```

- Python·템플릿으로 의미를 생성하지 않는다.
- 한 번에 여러 회차의 의미를 동시에 저작하지 않는다.
- 한 회차가 경량 게이트와 checkpoint를 통과하기 전 다음 회차를 완료로 계산하지 않는다.
- 회차마다 강검증하지 않는다.
- 기존 검증 완료 DB를 새 작품 하나 때문에 작품별로 전수 재검증하지 않는다.
- 사용자 승인 전 `CANONICAL`로 승격하지 않는다.

## 2. 신규 작품 선택

```text
원본 아카이브 인벤토리
→ 현재 DB 작품 인덱스와 차집합
→ 회차 완전성·인코딩·중복 판본·장면 경계 비교
→ 원본 안정성이 가장 높은 신규 작품 1편 선택
```

기존 DB에 있는 작품은 신규 분석 대상으로 선택하지 않는다. 원본 누락·회차 위장·중복 판본·장면 경계 잠금 실패가 있으면 `SOURCE_HOLD`로 둔다.

## 3. SourceLock preflight

Stage01 전에 다음만 잠근다.

- 작품명과 실제 회차 번호
- 원본 파일·정규화 UTF-8 파일 SHA256
- canonical `scene_no=1..N`
- 회차별 장면 수
- Q1~Q4 범위
- source marker anomaly
- `python_semantic_generation:false`
- 다음 재개 지점

원본 대본과 raw text는 허브에 커밋하지 않는다.

## 4. 회차 실행 절차

각 회차를 반드시 아래 순서로 처리한다.

```text
Q1 원문 직접독해 → Stage01 부분 저장
Q2 원문 직접독해 → Stage01 부분 저장
Q3 원문 직접독해 → Stage01 부분 저장
Q4 원문 직접독해 → Stage01 완성
→ EpisodeMeta
→ Stage02 SequenceBlueprint
→ EpisodeArc
→ Stage03 CharacterArc / RelationshipArc / LocalEdge / PayoffCandidate
→ 회차 경량 게이트
→ episode checkpoint 저장
→ next_pointer 갱신
```

각 장면은 내부적으로 여섯 질문을 사용한다.

1. 실제 행동은 무엇인가.
2. 누가 어떤 전략을 쓰거나 무엇을 숨기는가.
3. 정보·오해·조건 중 무엇이 바뀌는가.
4. 누가 무엇을 선택·거부·유예하는가.
5. 회차 구조에서 이 장면의 기능은 무엇인가.
6. 어떤 잔여 압력이 다음 장면·시퀀스를 미는가.

Stage01~04 exact keyset·enum·ID·FK는 `SCHEMA_CONTRACTS_V2.md`만 따른다.

## 5. 회차 경량 게이트

회차 종료 시 다음만 검사한다.

1. JSON·JSONL 파싱
2. exact keyset·자료형·ID 형식
3. SceneCard `scene_no=1..N` coverage
4. Sequence 장면 partition: 누락 0, 중복 0
5. `sum(scene_budget)==scene_count`
6. `sum(runtime_share)==1.0 ± 1e-6`
7. Arc trigger·turning point·Edge 장면 참조 존재
8. LocalEdge 동일 회차·`gap_episodes=0`·`edge_type=causal`
9. 파일 존재·checkpoint checksum·`next_pointer`

회차 경량 게이트에서는 다음을 검사하지 않는다.

- exact/masked 의미문장 전역 중복
- 앙상블 인물 누락
- 관계쌍 역방향 중복의 전 시즌 스캔
- LocalEdge 밀도·인접 target 비율
- 회차 간 인과·payoff 연결
- 전체 SourceLock 해시 전수 재검사
- ZIP·Fresh extraction

이 항목을 회차마다 반복하면 같은 데이터를 계속 재독해하여 속도와 세션 한도를 낭비한다.

## 6. 결정론적 직렬화 최적화

의미 저작은 계속 한 회차씩 수행한다. 다만 이미 직접독해와 의미 초안이 끝난 회차의 JSON/JSONL 직렬화와 경량검사는 최대 4회차까지 한 묶음으로 실행할 수 있다.

허용:

```text
EP01 의미 저작 완료
EP02 의미 저작 완료
EP03 의미 저작 완료
EP04 의미 저작 완료
→ EP01~04 결정론적 직렬화·경량검사 묶음
```

금지:

```text
EP01~04 원문을 한꺼번에 입력
→ Python/템플릿으로 의미 레코드 생성
```

## 7. 전반부 또는 8회차 블록 강검증

전반부가 끝났거나 약 8회차가 완성된 뒤 한 번만 실행한다.

- Stage01 exact·masked skeleton repetition
- Stage02 goal·obstacle·value_shift·turn grounding
- Stage01↔02↔03 참조 정합성
- 인물명·조직명 표준화
- CharacterArc 앙상블 누락 감사
- RelationshipArc 역방향 중복·근거 감사
- LocalEdge 선택성·인접성·밀도 감사
- PayoffCandidate 중복·근거 감사
- 블록 전체 ID 유일성

LocalEdge 비율 `>0.10`, 인접 target 비율 `>0.50`은 자동 FAIL이 아니라 수동 선택성 감사 trigger다.

강검증 실패 시 전체 블록을 다시 쓰지 않는다. 실패한 회차·장면·레코드 범위만 원본을 재독해해 수정한다.

## 8. 후반부와 전 시즌

```text
후반부 회차별 경량 게이트
→ 후반부 블록 강검증 1회
→ 전 시즌 Stage01~03 통합 강검증 1회
→ Stage04
```

전 시즌 Stage01~03가 통과하기 전 Stage04를 생성하지 않는다.

## 9. Stage04

- 모든 PayoffCandidate를 100% disposition한다.
- 검증된 회차 간 연결만 CrossEpisodeEdge로 승격한다.
- 이전 회 마지막 장면→다음 회 첫 장면 자동 브리지를 만들지 않는다.
- FullSeriesArc를 작성한다.
- Stage04 강검증은 한 번 실행한다.

## 10. 패키징·Fresh extraction

검증과 패키징은 분리한다.

```text
Process A — validation-only
작품 gate → VALIDATION_PASS

Process B — package-only
manifest·checksum → ZIP → 별도 디렉터리 재해제
→ 실제 CLI → pre/post tree 비교 → RELEASE_READY
```

회차·블록 중간 ZIP과 Fresh extraction을 반복하지 않는다. 최종 작품 ZIP에서 한 번 수행한다.

## 11. 전체 DB 증분 편입

기존 DB가 Fresh Extraction PASS를 받은 immutable release라면 신규 작품 편입 시 다음을 사용한다.

```text
이전 릴리스 ZIP SHA·외부 검증서 계승
+ 신규 작품 current validator
+ 신규 SourceLock 검사
+ 전체 registry/source/encoding/database/release gate
+ 최종 ZIP Fresh extraction에서 신규 작품과 전역 gate 재실행
```

새 작품 하나 때문에 이전 전 작품의 의미 validator를 매번 다시 실행하지 않는다. 이전 tree가 변경됐거나 검증서·SHA가 없을 때만 전체 작품 재검증을 수행한다.

## 12. 직접독해 증빙 저장 정책

독립 작품 ZIP은 원시 증빙을 보존할 수 있다.

```text
lineage/evidence/quarter_audits/
lineage/evidence/raw_quarters/
```

운영 전체 DB에는 대량 `quarter_audits/`와 `direct_reading_evidence/` 폴더를 두지 않는 것을 기본으로 한다. 대신 SourceLock·provenance에 다음을 남긴다.

- `direct_reading_attested`
- attested episode count
- quarter audit count
- aggregate SHA256
- 독립 작품 ZIP 파일명·SHA256
- evidence retention policy

원시 증빙 삭제가 아니라 **독립 lineage 패키지로 분리 보존**하는 정책이다.

## 13. 새 대화창 재개 규칙

새 대화창은 과거 대화 전체를 다시 읽지 않는다. 다음 compact checkpoint 하나를 우선한다.

```json
{
  "work_id": "작품명",
  "source_lock_sha256": "...",
  "completed_episodes": [1,2,3],
  "next_pointer": "EP04_Q1",
  "current_phase": "FRONT_HALF_STAGE01_03",
  "last_gate": "EP03_LIGHT_PASS",
  "artifact_root": "...",
  "meaning_drafts_pending_serialization": []
}
```

파일 증거와 checkpoint가 대화 보고보다 우선한다.

## 14. 최소 개발자 보고

```text
작품 / 완료 범위 / 주요 레코드 수 / gate / errors·warnings / ZIP SHA256 / next
```

회차별 진행 상황을 장황하게 보고하지 않는다. 다만 중단·FAIL·SourceHold가 발생하면 정확한 파일 기준 완료 지점과 복구 지점을 즉시 보고한다.

## 15. 금지 목록

- 매 새 대화창마다 모든 허브 문서·과거 대화 전수 학습
- 회차별 강검증
- 회차별 Fresh extraction
- 8회차 동시 의미 생성
- Python 의미 생성
- 강검증과 패키징을 한 장기 프로세스에 결합
- 검증 완료 이전에 “분석 완료” 보고
- 신규 작품 선택 전 현재 DB 작품 차집합 생략
- 독립 lineage 없이 운영 DB 증빙 폴더만 삭제

## 16. 즉시 실행 명령

새 대화창에서 이 문서와 `SCHEMA_CONTRACTS_V2.md`를 읽은 뒤 다음 포인터에서 바로 시작한다.

```text
SELECT_NEW_WORK
→ SOURCE_ARCHIVE_INVENTORY
→ DATABASE_SET_DIFFERENCE
→ SourceLock
→ EP01_Q1
```
