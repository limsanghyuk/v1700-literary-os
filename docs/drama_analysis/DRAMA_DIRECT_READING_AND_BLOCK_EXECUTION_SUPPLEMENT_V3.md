# 드라마 직접독해·블록 실행 운영 보충 규범 V3

- 문서 ID: `DRAMA_DIRECT_READING_BLOCK_EXECUTION_SUPPLEMENT_V3`
- 기준일: 2026-07-16
- 적용 범위: 신규 작품 분석, 기존 Stage01~04 업그레이드, 장편 작품, 세션 한도 관리
- 기본 상태: EXT6/HXT6 비활성 유지, 사용자 승인 전 `PASS_CANDIDATE`

## 0. 권위와 정정

이 문서는 기존 스키마를 대체하지 않는다. exact keyset·자료형·enum·ID·FK는 `SCHEMA_CONTRACTS_V2.md`가 우선한다. 다음 운영 규칙은 충돌하는 과거 문장을 대체한다.

1. `LocalEdge`는 동일 회차만 허용한다. `src_episode_no == tgt_episode_no`, `gap_episodes == 0`이다.
2. 회차 경계를 넘는 연결은 Stage04 `CrossEpisodeEdge`에서만 확정한다.
3. LocalEdge·CharacterArc·RelationshipArc·PayoffCandidate에 고정 최소 수량을 두지 않는다.
4. 매 회차 의미 강검증을 반복하지 않는다. 회차별 경량 게이트, 약 8회차 블록 강검증, 전 시즌 강검증을 분리한다.
5. QuarterAudit는 직접독해 직후 작성된 동시대 증빙이어야 한다. 완성 데이터의 사후 4등분을 직접독해 증거로 승격하지 않는다.
6. `original_extracted/{작품명}/`에 원본 TXT를 먼저 저장하지 않은 작품은 완전한 SourceLock 상태가 아니다.

## 1. 직접독해의 최소 사고 단위

장면을 줄거리 한 문장으로 압축하지 말고 다음 여섯 질문으로 읽는다.

1. 행동: 실제로 누가 무엇을 했는가.
2. 전략: 말하기·숨기기·회피·유도·거부 중 어떤 수를 썼는가.
3. 정보 변화: 누가 무엇을 새로 알거나 오해하게 됐는가.
4. 선택: 인물이 무엇을 결정·보류·포기했는가.
5. 구조 기능: 설정·압박·전환·회수 중 이 장면이 맡는 기능은 무엇인가.
6. 잔여 압력: 다음 장면이나 후속 회차를 움직이는 미해결 원인은 무엇인가.

SceneCard의 `intent_gist`는 행동문을 반복하지 않고 2~6번 중 핵심 기능을 압축한다. 장면 제목은 사건 표면, intent는 서사 기능을 담당한다.

## 2. 시퀀스 독해의 3축

연속 장면을 묶을 때 장면 수를 먼저 정하지 않는다.

- Goal: 이 구간에서 POV 인물이 당장 얻으려는 것은 무엇인가.
- Obstacle: 그 시도를 막는 인물·정보·제도·내적 저항은 무엇인가.
- Turn: 구간 종료 시 되돌리기 어려운 상태 변화는 무엇인가.

장소가 바뀌어도 같은 목표가 계속되면 한 시퀀스일 수 있고, 같은 장소에서도 목표나 권력 조건이 바뀌면 시퀀스를 나눌 수 있다. 밀도 하한은 품질 경보이지 숫자를 맞추기 위한 분할 지시가 아니다.

## 3. 회차와 시즌을 이해하는 방법

### 회차

- Entry state: 회차 시작 시 인물·관계·정보 조건
- Dramatic question: 이번 회차가 실제로 시험하는 질문
- Escalation: 선택 비용이 커지는 과정
- Turning point: 질문의 답을 뒤집는 시퀀스
- Exit state: 다음 회차가 물려받는 새 조건

Act 구조를 시퀀스 수로 수학적 4등분하지 않는다. 실제 압력과 선택이 바뀌는 지점으로 구분한다.

### 시즌

장기 서사는 사건 목록이 아니라 반복되면서 의미가 변하는 패턴으로 읽는다.

- 첫 등장과 재등장의 의미 차이
- 같은 약속·물건·대사가 다른 권력 조건에서 되풀이되는 방식
- 인물의 want가 need 또는 파국으로 변하는 경로
- 관계의 신뢰·권력·정보·의존·적대 축이 이동하는 방향

## 4. 신규 분석과 업그레이드의 시작점

작업 전에 작품을 다음 중 하나로 판정한다.

- `NEW_ANALYSIS`: 기존 의미 자산 없음
- `NORMAL_UPGRADE`: Stage01·02 정상, Stage03·04 중심
- `STAGE02_PARTIAL_REAUTHOR`: 일부 회차만 의미 드리프트
- `STAGE02_FULL_REAUTHOR`: 반복 골격·기계 분절로 Stage02 전면 재저작
- `SOURCE_HOLD`: 원본 누락·중복·손상으로 진행 금지

업그레이드 작품은 기존 SceneCard를 색인, 원본을 최종 증거로 사용한다. 정상 자산을 백지에서 다시 쓰는 것은 품질 향상이 아니라 재작업 증가일 수 있다.

## 5. 원본 저장과 SourceLock의 이중 증거

분석 전에 반드시 다음 구조를 만든다.

```text
seqcard_ko/original_extracted/{작품명}/
  {작품명}_01.txt
  {작품명}_02.txt
  ...
```

SourceLock에는 두 종류의 해시를 구분한다.

- `original_bytes_sha256`: ZIP/HWP/CP949 등 입수 당시 원본 바이트
- `canonical_storage_sha256`: UTF-8 TXT로 정규화되어 `original_extracted`에 저장된 파일

인코딩 변환 후 두 해시가 다르다는 이유로 오류로 보지 않는다. SceneCard JSON 해시를 원본 장면 해시로 기록하면 SourceLock 실패다. 원본의 결번·중복·하위 씬 번호는 물리 표식으로 보존하고, 분석 참조는 별도의 canonical ordinal `1..N`을 사용한다.

## 6. 회차 다이제스트

원본과 기존 JSON을 반복해서 여러 창에서 열지 말고 한 회차의 증거를 한 화면에 모은다.

```text
EPxx
Entry / Exit / Central conflict
SEQ01 [S01-S07]: goal / obstacle / turn / POV
SEQ02 ...
Character changes
Relationship changes
Local causal candidates
Long-range candidate ledger
Open questions for next episode
```

Python은 파일을 정렬하고 다이제스트를 출력할 수 있지만 goal·turn·변화·후보의 의미를 생성해서는 안 된다.

## 7. Stage03 회차별 수직 처리

권장 방식:

```text
EPxx 독해
→ EpisodeArc 확인/재저작
→ CharacterArc
→ RelationshipArc
→ LocalEdge
→ PayoffCandidate
→ 경량 참조 게이트
→ 회차 잠금
```

먼저 세 집합을 만든다.

- A: 시작과 끝의 상태가 실제로 다른 인물
- B: 신뢰·권력·정보·의존·적대 조건이 이동한 관계쌍
- C: 단순 등장 또는 변화 없음

Stage03 대상은 A와 B다. 수량 할당량을 채우기 위해 C를 Arc로 만들지 않는다.

## 8. 인물·관계 변화의 증명 질문

### CharacterArc

- 회차 시작과 끝에서 상태가 달라졌는가.
- 그 변화가 실재 장면 하나로 증명되는가.
- 다음 행동의 선택 가능성을 바꾸는가.

### RelationshipArc

- 두 인물이 실제로 상호작용했는가.
- 신뢰·권력·정보·의존·적대 중 어느 축이 이동했는가.
- 단순 대화가 아니라 이후 선택 조건이 달라졌는가.

같은 사건을 공유해도 인물별·관계별 evidence는 그 사건이 각 대상에게 갖는 의미를 다르게 쓴다.

## 9. LocalEdge와 후보 절제

LocalEdge는 다음을 모두 통과할 때만 만든다.

1. source가 없으면 target 사건이 같은 방식으로 발생하지 않는가.
2. source와 target 사이에 구체적 원인·결과가 있는가.
3. 단순히 인접 장면이라 연결한 것은 아닌가.
4. 동일 회차인가.
5. label이 target SceneCard core와 일치하는가.

회차당 2~3건이 자주 적절하지만 할당량이 아니다. PayoffCandidate는 장거리 의미가 가능한 정보·물건·약속·위협·선택만 남긴다. 다음 장면에서 해결되는 문제, 일반 대사, 회말이라는 이유만의 훅은 제외한다.

## 10. Stage04 후보 원장

Stage03에서 후보를 만들 때 다음 상태를 함께 관리한다.

```text
OPEN → TARGET_FOUND → PROMOTE / REJECT / RECLASSIFY
```

후속 회차에서 대상 장면을 발견하면 candidate_id와 target episode/scene을 메모한다. 이는 Stage04 판정을 자동 생성하는 것이 아니라 나중에 원본을 다시 찾는 시간을 줄이는 색인이다. 전 시즌 종료 후 모든 후보를 다시 대조하여 100% disposition하고, 마지막 장면→다음 회 첫 장면을 자동 연결하지 않는다.

## 11. 검증 주기

### 회차별 경량 게이트

- 파일 저장 여부
- JSON/JSONL 파싱
- 필수 키와 ID 형식
- SceneCard ordinal
- Stage02 coverage·중복·합계
- trigger/edge scene 존재
- 명백한 placeholder·자동 문형
- 다음 재진입 포인터

### 블록 강검증

기본 운영 블록은 약 8회다.

- 16회: 1~8 / 9~16
- 24회: 1~8 / 9~16 / 17~24
- 31회: 1~8 / 9~16 / 17~24 / 25~31
- 54회: 1~8 / 9~16 / 17~24 / 25~32 / 33~40 / 41~48 / 49~54

블록 종료 시 정확 중복, 마스킹 골격, 인물명, 관계쌍 역순, ID 전역성, Stage01↔02↔03 참조를 강검증한다. 오류가 난 범위만 다시 읽는다.

### 전 시즌 게이트

모든 블록이 잠긴 후 전체 FK, 반복성, 시즌 Arc, 후보 100% 처분, 자동 경계 브리지, ZIP·SHA·fresh extraction을 검사한다.

## 12. 장편 작품의 속도와 토큰 관리

- 중간 보고보다 실제 파일 저장을 우선한다.
- 한 회차를 읽고 같은 회차의 Stage03를 함께 끝낸다.
- 이미 잠긴 회차를 습관적으로 다시 열지 않는다.
- 원문 전체를 매번 재로딩하지 않고 회차 다이제스트와 필요한 장면 범위만 연다.
- 체크포인트에는 `completed`, `next`, 파일 해시, 경량 게이트 결과만 기록한다.
- 블록 종료 전에는 전 시즌 반복 검사와 전체 SHA 재생성을 수행하지 않는다.
- 세션 한도에 가까워지면 새 의미 저작을 시작하지 않고 현재 회차 파일을 먼저 영속화한다.

빠른 작업은 읽는 속도를 높이는 것이 아니라 재독해·재검증·재보고를 줄이는 것이다.

## 13. 중단 복구와 허위 완료 방지

대화의 완료 문장보다 실제 파일이 우선한다.

- 파일 없음: `INTERRUPTED_BEFORE_PERSISTENCE`
- 파일 존재, 검증 없음: `FILES_PRESENT_VALIDATION_PENDING`
- 회차 경량 게이트 통과: `EPISODE_LIGHT_LOCKED`
- 블록 강검증 통과: `BLOCK_STRONG_LOCKED`
- 전 시즌 Stage01~03 통과: `FULL_STAGE01_03_LOCKED`

체크포인트가 파일을 참조하지만 파일이 없으면 해당 체크포인트는 무효다.

## 14. Stage01 내용 깊이 감사

Stage01은 SceneCard 수와 JSON 형식만으로 통과하지 않는다.

- title과 intent의 고유성
- core를 마스킹한 뒤 문장 골격 다양성
- intent가 행동문 복사인지 여부
- 회차 내 bridge/intercut 장면의 기능 밀도
- 원본 heading/ordinal 정렬
- 인물 선택·정보 변화가 실제 장면과 일치하는 표본 대조

높은 문장 다양성은 필요조건일 뿐 충분조건이 아니다. SourceLock 정렬이 불완전하면 의미 밀도가 높아도 `PRESERVE_CANDIDATE`로 두고 원본 대조를 보강한다.

## 15. 결정론적 교정과 의미 재저작의 분리

Python 허용: key 순서, ID 형식, work_id, runtime_share, core_mix 재계산, count, hash, parse, 중복 탐지, 패키징.

직접 재저작: sequence_intent, goal, obstacle, value_shift, EpisodeArc 의미, CharacterArc, RelationshipArc, LocalEdge note와 인과 선택, PayoffCandidate, disposition, CrossEpisodeEdge, FullSeriesArc.

형식 오류를 고치면서 의미를 은밀히 바꾸지 않는다. 의미 결함은 원본을 다시 읽고 수정 범위를 ledger에 남긴다.

## 16. 실제 실패 신호

- 모든 Sequence가 같은 공식 문형
- goal·obstacle 고유 문장이 극소수
- EpisodeArc를 수학적으로 같은 비율로 분할
- QuarterAudit가 완성본 이후 같은 시각에 일괄 생성
- SourceLock 해시가 SceneCard JSON 해시와 동일
- LocalEdge가 회차마다 first→last 한 건씩 자동 생성
- 후보가 회차당 정확히 같은 수량
- disposition 이유가 후보 description 복사
- Python 파일이 core data 폴더 안에 남아 있음

이 신호가 발견되면 포장 무결성과 의미 품질을 분리 판정한다. ZIP CRC가 PASS여도 의미 계층은 QUARANTINE될 수 있다.

## 17. 완료 판정

```text
원본 TXT 정규 저장
→ SourceLock
→ Stage01~03 블록 잠금
→ 전 시즌 강검증
→ Stage04 100% disposition
→ 개별 작품 fresh extraction
→ DB 삽입
→ 전체 DB validator
→ 전체 DB ZIP fresh extraction
→ PASS_CANDIDATE
```

사용자의 명시 승인 없이는 CANONICAL로 승격하지 않는다.
