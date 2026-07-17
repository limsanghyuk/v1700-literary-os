# 신규 드라마 분석 상세 플레이북 v1

- Document ID: `DRAMA-NEW-WORK-DETAILED-PLAYBOOK-V1`
- Status: `AUTHORITATIVE_COMPANION`
- Updated: 2026-07-17
- Execution authority: `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md`
- Exact schema authority: `SCHEMA_CONTRACTS_V2.md`
- Validation cadence authority: `DRAMA_VALIDATION_AND_SESSION_EFFICIENCY_POLICY_V1.md`
- EXT6/HXT6: 기본 비활성
- Promotion: 사용자 승인 전 `PASS_CANDIDATE`, 승인 후에만 `CANONICAL`

## 0. 목적

이 문서는 신규 작품을 처음 분석하는 새 대화창이 V2 실행 가이드의 압축된 규칙을 실제 작업으로 옮길 수 있도록 원본 직접독해, Stage01~04, 클로드식 앙상블 폭, LocalEdge 선택성, 후보 전수 처분, 검증·계보·패키징을 한 흐름으로 설명한다.

이 문서는 V2 실행 가이드를 대체하지 않는다. 충돌 시 다음 순서를 따른다.

```text
1. SCHEMA_CONTRACTS_V2
2. DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2
3. DRAMA_VALIDATION_AND_SESSION_EFFICIENCY_POLICY_V1
4. DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V4
5. 이 상세 플레이북
6. ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY
7. CLOSE_READING_MASTER_PROTOCOL
8. LINEAGE_PACKAGE_HANDOFF
```

## 1. 새 대화창 로드

### 공식 최소 실행 세트

```text
1. DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md
2. SCHEMA_CONTRACTS_V2.md
```

신규 작품 선택 시 최신 `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-17.json` 또는 실제 DB work index를 추가한다.

### 처음 적용하는 모델의 상세 온보딩

```text
1. DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md
2. DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V1.md
3. SCHEMA_CONTRACTS_V2.md
4. DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-17.json
```

과거 대화·모든 세션 README·모든 역사 문서를 매번 전수 조사하지 않는다.

## 2. 고정 파이프라인

```text
source archive inventory
→ current DB와 작품 차집합
→ 신규 작품 1편 선택
→ original_extracted/{작품명}/ UTF-8 원본 저장
→ SourceLock
→ EP01 Q1~Q4 직접독해
→ Stage01 SceneCard
→ EpisodeMeta
→ Stage02 SequenceBlueprint·EpisodeArc
→ Stage03 앙상블 CharacterArc·RelationshipArc·LocalEdge·PayoffCandidate
→ episode light gate·checkpoint
→ 다음 회차 반복
→ 전반부/약 8회차 strong gate
→ 후반부 동일 절차·strong gate
→ full Stage01~03 gate
→ Stage04 candidate disposition 100%
→ CrossEpisodeEdge·FullSeriesArc
→ 독립 작품 ZIP·fresh extraction
→ 증분 DB 편입·전역 gate
→ DB ZIP·fresh extraction
→ PASS_CANDIDATE
```

## 3. 절대 규칙

```text
의미 독해 최소 단위 = quarter
의미 저작 원자 단위 = 1 episode
결정론적 직렬화 묶음 = 최대 4 episodes
강검증 블록 = 전반부 또는 약 8 episodes
Stage04 = full-series fan-in 1회
Fresh extraction = 최종 패키지 1회
```

- Python·템플릿으로 의미를 생성하지 않는다.
- 여러 회차의 의미를 한 번에 생성하지 않는다.
- 한 회차가 경량 게이트와 checkpoint를 통과하기 전 다음 회차를 완료로 계산하지 않는다.
- 회차마다 강검증·전체 SourceLock 재검사·ZIP·Fresh extraction을 반복하지 않는다.
- 검증과 패키징을 하나의 장기 프로세스로 결합하지 않는다.
- 원본 누락을 줄거리·방송 기억·추정으로 보완하지 않는다.

## 4. 신규 작품 선택과 SourceLock

### 작품 선택

```text
원본 아카이브 인벤토리
→ 현재 DB 작품 인덱스와 차집합
→ 회차 완전성·인코딩·중복 판본·장면 경계 비교
→ 원본 안정성이 가장 높은 신규 작품 1편
```

이미 DB에 있는 작품은 신규 작품으로 중복 분석하지 않는다. 원본 누락·회차 위장·중복 판본·장면 경계 잠금 실패는 `SOURCE_HOLD`다.

### 원본 저장

```text
seqcard_ko/original_extracted/{작품명}/
  {작품명}_01.txt
  {작품명}_02.txt
  ...
```

작품별 폴더 없이 루트에 TXT를 흩어 두지 않는다.

### SourceLock 이중 증거

```text
original_bytes_sha256
= 입수 ZIP/HWP/CP949/UTF-16 원래 바이트

canonical_storage_sha256
= original_extracted에 저장된 UTF-8 TXT 바이트
```

분석 전에 다음을 잠근다.

- 작품명과 실제 회차 번호
- 원본·UTF-8 저장본 SHA256
- canonical `scene_no=1..N`
- 회차별 장면 수
- Q1~Q4 범위
- source marker anomaly
- 제외한 비정본 파일
- `direct_reading_attested`
- `python_semantic_generation:false`
- 다음 재개 지점

인코딩 변환으로 두 해시가 다른 것은 정상이다. SceneCard JSON 해시를 원본 해시로 쓰면 실패다.

## 5. 회차 실행 루프

```text
Q1 원문 직접독해 → Stage01 부분 저장
Q2 원문 직접독해 → Stage01 부분 저장
Q3 원문 직접독해 → Stage01 부분 저장
Q4 원문 직접독해 → Stage01 완성
→ EpisodeMeta
→ SequenceBlueprint
→ EpisodeArc
→ Stage03 앙상블 스캔
→ CharacterArc
→ RelationshipArc
→ LocalEdge
→ PayoffCandidate
→ episode light gate
→ checkpoint·next_pointer
```

이미 직접독해와 의미 초안이 끝난 회차의 JSON/JSONL 직렬화·경량검사만 최대 4회차까지 묶을 수 있다. 원문 의미 생성은 계속 한 회차씩 한다.

## 6. 장면 직접독해 6질문

각 장면에서 내부적으로 반드시 답한다.

1. **행동** — 실제로 누가 무엇을 했는가.
2. **전략** — 말하기·숨기기·회피·유도·거부 중 어떤 수를 썼는가.
3. **정보 변화** — 누가 무엇을 새로 알거나 오해하게 됐는가.
4. **선택** — 무엇을 결정·거부·유예·포기했는가.
5. **구조 기능** — 설정·압박·전환·회수 중 무엇을 수행하는가.
6. **잔여 압력** — 다음 장면·시퀀스·후속 회차를 움직이는 미해결 원인은 무엇인가.

사건 요약 한 문장을 여러 필드에 복사하지 않는다. 후속 회차를 안다는 이유로 미래 의미를 앞 장면에 소급하지 않는다.

## 7. Stage01 — SceneCard

exact 9키:

```text
work_id, scene_no, heading, title, intent_gist,
core, core2, skin, by
```

- `heading`: 원본 provenance와 대응한다.
- `title`: 장면의 고유 전환을 압축한다.
- `intent_gist`: 욕망·압력·전략·정보·선택의 변화와 구조 기능을 구체적으로 쓴다.
- `core/core2`: CORE_ENUM 16의 실제 극적 기능만 사용한다.
- `skin`: 표면 장르·연출 질감이며 core를 반복하지 않는다.

금지:

- 키워드 조각
- `[EPxx-Syy]` 같은 가시적 템플릿
- 동일 시작구·동일 골격 반복
- 원문 장문 대사 복사
- 원문에 없는 인물·감정·인과
- Python 의미 생성

내용 깊이 권장:

```text
회차 평균 >= 3.0 / 4
최저 >= 2.5 또는 재저작
0점·1점 장면 = 0
```

## 8. EpisodeMeta·Stage02·EpisodeArc

EpisodeMeta exact 5키:

```text
work_id, scene_count, core_dist, episode_function, by
```

`scene_count`와 `core_dist`는 SceneCard에서 결정론적으로 재계산한다.

SequenceBlueprint exact 18키는 schema 문서를 따른다. 시퀀스는 장면 수 균등분할이 아니라 다음 3축으로 나눈다.

- **Goal**: POV 인물이 당장 얻으려는 것
- **Obstacle**: 인물·정보·제도·내적 저항 중 실제 방해
- **Turn**: 종료 시 되돌리기 어려운 상태 변화

필수 불변식:

```text
모든 장면이 정확히 하나의 sequence에 포함
누락 0 / 중복 0
sum(scene_budget) == scene_count
sum(runtime_share) == 1.0 ± 1e-6
core_mix는 member SceneCard의 실제 core/core2만 사용
sequence_count / scene_count >= 0.11
```

밀도 하한은 경보이지 숫자를 맞추기 위한 기계 분할 지시가 아니다.

EpisodeArc exact 13키는 실제 시퀀스를 근거로 한다.

```text
Entry state
→ Dramatic question
→ Escalation
→ Turning point
→ Exit state
```

시퀀스 수를 수학적으로 4등분해 act를 만들지 않는다.

## 9. Stage03 — 클로드식 앙상블 폭의 채택

### 채택하는 장점

회차마다 주인공만 보지 않고 다음 층을 폭넓게 스캔한다.

- 주인공·대립자
- 핵심 조력자·경쟁자
- 조직 내부 의사결정자
- 반대 진영 기능 인물
- 반복 등장하는 실무자·가족·동료
- 이번 회차에서 사건축을 바꾼 단역
- 동맹·경쟁·상하·공모·거래·은폐 관계

이 폭이 클로드식 분석에서 공식 채택하는 장점이다.

### 채택하지 않는 방식

- 등장인물 전원을 기계적으로 CharacterArc화
- 모든 관계쌍을 RelationshipArc화
- 회차별 고정 수량 채우기
- 같은 evidence 복사
- 모든 장면을 다음 장면과 LocalEdge로 연결
- 회차 간 연결을 LocalEdge에 저장
- 미처리 PayoffCandidate 방치
- 레코드 수량을 품질 점수로 사용

### A/B/C 분류

- **A**: 회차 시작과 끝의 상태가 실제로 달라진 인물
- **B**: 신뢰·권력·정보·의존·적대 조건이 이동한 관계쌍
- **C**: 단순 등장 또는 변화 없음

Stage03 대상은 A와 B다. C를 수량 채우기 위해 기록하지 않는다.

### 앙상블 누락 감사

```text
실제 변화가 있는데 빠진 핵심 의사결정자가 있는가?
실제 변화가 있는데 빠진 동맹·갈등·상하 관계가 있는가?
수량을 맞추기 위해 변화 없는 인물·관계를 넣었는가?
```

누락은 보강하고 수량 채우기는 삭제한다.

## 10. CharacterArc·RelationshipArc

CharacterArc exact 8키:

```text
work_id, character, episode_no, state_label,
state_delta, trigger_scene_no, by, evidence
```

생성 조건:

- 회차 입구와 출구 사이의 상태 변화
- trigger 장면에 실제 등장
- evidence가 구체적 변화 근거
- 변화가 이후 선택 가능성을 바꿈

RelationshipArc exact 9키:

```text
work_id, char_a, char_b, episode_no,
relation_state, relation_delta, trigger_scene_no,
evidence, by
```

생성 조건:

- 양쪽 인물이 함께 등장하거나 직접 통화·교신
- 신뢰·권력·의무·갈등·거리·연합·거래 조건 이동
- `relation_state`와 `relation_delta` 구분
- 이후 선택 조건 변화

`(A,B)`와 `(B,A)`를 중복 생성하지 않는다. 고정 최소치·최대치는 없다.

## 11. LocalEdge — 선별적 동일 회차 인과

하드 게이트:

```text
edge_type == causal
src_episode_no == tgt_episode_no
gap_episodes == 0
label == target SceneCard.core
source/target scene exists
```

필수 반사실 질문:

```text
source의 행동·정보·선택이 없었더라도
target이 같은 방식으로 발생했는가?
```

- 예: LocalEdge가 아니다.
- 아니오: 구체 인과를 note로 설명할 수 있을 때만 생성한다.

배제:

- 번호 인접성
- 같은 시퀀스
- 유사 주제·감정
- 모든 장면 next-scene 사슬
- 회차 간 LocalEdge
- 수량 목표

수동 선택성 감사 trigger:

```text
LocalEdge / SceneCard > 0.10
또는
adjacent-target LocalEdge ratio > 0.50
```

trigger는 자동 FAIL이 아니지만 감사 없이 PASS할 수 없다. 회차 간 LocalEdge는 한 건이라도 blocking error다.

## 12. PayoffCandidate와 후보 원장

PayoffCandidate exact 7키는 장거리 가능성이 구체적인 장면만 기록한다.

후보 대상:

- 이후 의미가 달라질 정보
- 반복될 물건·약속·위협
- 관계·권력 조건을 바꿀 미해결 선택

제외:

- 다음 장면에서 해결되는 문제
- 일반 대사
- 회말이라는 이유만의 훅
- 수량 채우기 후보

내부 후보 상태:

```text
OPEN → TARGET_FOUND → PROMOTE / REJECT / RECLASSIFY
```

이 원장은 Stage04 판단을 자동화하지 않고 원본 재탐색 시간을 줄이는 색인이다.

## 13. 검증 cadence

### Episode Light Gate

회차 종료 시 구조·재개 가능성만 검사한다.

- parse·exact schema·ID
- SceneCard coverage
- Sequence partition·runtime sum
- trigger·edge reference existence
- LocalEdge same episode/gap0
- checkpoint·next_pointer

회차마다 다음을 검사하지 않는다.

- 전역 의미 반복
- 앙상블 누락
- 관계쌍 역방향 전 시즌 스캔
- LocalEdge 밀도·인접 비율
- 회차 간 payoff
- 전체 SourceLock 재해시
- ZIP·Fresh extraction

### Half-season / 8-episode Strong Gate

- exact·masked skeleton repetition
- Stage02 grounding
- Stage01↔02↔03 참조
- 인물·조직명 표준화
- CharacterArc 앙상블 누락
- RelationshipArc 역방향 중복·근거
- LocalEdge 선택성·밀도·인접성·반사실 인과
- PayoffCandidate 중복·근거
- block ID/FK

실패 시 전체 블록을 다시 쓰지 않고 실패 범위만 원본 재독해한다.

### Full-series Gate

- Stage01~03 전체 FK·coverage·반복성
- 앙상블 실제 변화 누락·수량 채우기 감사
- 회차 간 LocalEdge 0
- Stage04 진입 가능 여부

## 14. Stage04 — 후보 100% disposition

전 시즌 Stage01~03 통과 후 한 번 수행한다.

```text
모든 PayoffCandidate 목록화
→ 원 장면 재확인
→ 후속 실제 회수·변형·반향 장면 확인
→ 후보별 disposition
→ 검증된 연결만 CrossEpisodeEdge
→ FullSeriesArc 재종합
```

허용 disposition:

```text
PROMOTED_CROSS_EDGE
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL
RESOLVED_WITHIN_EPISODE
REJECTED_DUPLICATE
REJECTED_INSUFFICIENT_EVIDENCE
REJECTED_SOURCE_MISMATCH
```

```text
미처리 후보 = 0
```

CrossEpisodeEdge는 다음을 만족한다.

```text
tgt_episode_no > src_episode_no
gap_episodes == tgt_episode_no - src_episode_no
edge_type ∈ {callback, plant_payoff, subplot_counterpoint}
```

금지:

- 이전 회 마지막 장면→다음 회 첫 장면 자동 브리지
- 멀다는 이유만의 복선·회수
- 후보 일괄 승격
- 동일 note 복사

FullSeriesArc exact 17키는 실제 매크로 전환, 인물·관계 변화, 검증된 plant/payoff를 기준으로 다시 작성한다.

## 15. 계보·증빙·패키징

분석본을 덮어쓰지 않는다.

```text
source → run → validation → checkpoint → comparison → promotion
```

GPT·Claude·다른 모델 run은 별도 `run_id`를 사용한다. 서로 다른 SceneCard ordinal lineage를 부분 혼합하지 않는다.

Quarantine 조건:

- Python 의미 생성
- keyword/template artifact
- 잘못된 scene boundary
- source mismatch
- Stage01 내용 FAIL
- Stage02 coverage FAIL
- 허위 Arc·Edge·Payoff

독립 작품 패키지는 원시 직접독해 증빙을 보존할 수 있다.

```text
lineage/evidence/quarter_audits/
lineage/evidence/raw_quarters/
```

운영 전체 DB는 대량 증빙 폴더를 기본 제외하고 SourceLock·provenance에 다음을 남긴다.

- `direct_reading_attested`
- attested episode count
- quarter audit count
- aggregate SHA256
- 독립 작품 ZIP 파일명·SHA256
- evidence retention policy

이는 증거 삭제가 아니라 독립 lineage 패키지와 운영 DB의 저장 계층 분리다.

## 16. 검증과 패키징 분리

```text
Process A — validation-only
작품 gate → VALIDATION_PASS

Process B — package-only
manifest·checksum → ZIP → 별도 디렉터리 재해제
→ 실제 CLI → pre/post tree 비교 → RELEASE_READY
```

최종 작품 ZIP에서만 Fresh extraction을 수행한다.

## 17. 전체 DB 증분 편입

이전 DB가 다음을 만족하면 immutable validated base로 계승한다.

- ZIP SHA256 고정
- 외부 Fresh Extraction 검증서 존재
- pre/post tree mismatch 0
- current registries PASS

신규 작품 편입:

```text
previous certified release
+ new work validator
+ new SourceLock
+ full registry/source/encoding/database/release gates
+ final fresh extraction
```

이전 tree가 바뀌지 않았다면 기존 전 작품 의미 validator를 매번 다시 실행하지 않는다. 이전 tree 변경, SHA 불일치, validator contract 변경, 검증서 부재 시에만 full revalidation한다.

## 18. 최종 릴리스 체크리스트

```text
[ ] 신규 작품 DB 차집합 확인
[ ] original_extracted/{작품명}/ UTF-8 원본 완비
[ ] SourceLock 이중 해시 PASS
[ ] Q1~Q4 직접독해·checkpoint
[ ] SceneCard9 / EpisodeMeta5
[ ] Sequence18 coverage·partition·runtime·density PASS
[ ] EpisodeArc13
[ ] CharacterArc 앙상블 누락 감사
[ ] RelationshipArc 관계 누락·역방향 중복 감사
[ ] 변화 없는 Arc 수량 채우기 0
[ ] LocalEdge cross-episode 0
[ ] LocalEdge automatic adjacency false
[ ] LocalEdge 선택성 trigger 감사 완료
[ ] PayoffCandidate disposition 100%
[ ] CrossEpisodeEdge automatic boundary bridge 0
[ ] FullSeriesArc17 counts 일치
[ ] exact duplicate·masked skeleton PASS
[ ] Python semantic generation false
[ ] lineage·quarantine·supersession 정리
[ ] individual ZIP Fresh Extraction PASS
[ ] incremental DB global gates PASS
[ ] DB ZIP Fresh Extraction PASS
[ ] 사용자 승인 전 PASS_CANDIDATE
```

## 19. 새 대화창 복사용 실행 지시문

```text
GitHub 저장소 limsanghyuk/v1700-literary-os의 현재 드라마 분석 권위 브랜치에서
다음 문서를 순서대로 읽어라.

1. docs/drama_analysis/DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md
2. docs/drama_analysis/DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V1.md
3. docs/drama_analysis/SCHEMA_CONTRACTS_V2.md
4. docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-17.json

원본 아카이브와 현재 DB의 작품 차집합으로 신규 드라마 한 편을 선택하라.
원본을 original_extracted/{작품명}/에 UTF-8 TXT로 저장하고 SourceLock 이중 해시를 작성하라.
한 회차를 Q1→Q4로 직접 읽어 Stage01→Stage02→EpisodeArc→Stage03을 저작하라.

Stage03에서는 클로드식 장점인 회차별 앙상블 인물·관계 추적 폭을 채택하라.
주인공뿐 아니라 조직·가족·팀·경쟁 진영에서 실제 상태나 관계가 변한 대상을 폭넓게 스캔하라.
단순 등장, 변화 없는 인물·관계, 고정 수량 채우기는 기록하지 마라.

LocalEdge는 동일 회차의 구체적 causal 연결만 허용하라.
장면 번호 인접성, 같은 시퀀스, 유사 주제를 근거로 자동 연결하지 마라.
회차 간 연결은 Stage04 CrossEpisodeEdge에서만 확정하라.

모든 PayoffCandidate를 Stage04에서 개별 disposition하고 미처리 후보를 0으로 만들어라.
이전 회 마지막 장면과 다음 회 첫 장면을 자동 브리지하지 마라.

의미 저작은 한 회차씩 수행하고, 결정론적 직렬화만 최대 4회차 묶음을 허용하라.
회차 경량 게이트, 전반부/약 8회차 강검증, 전 시즌 게이트, Stage04, 패키지 게이트를 분리하라.
Python은 추출·해시·검증·직렬화·패키징에만 사용하라.

독립 작품 ZIP의 Fresh extraction을 통과시킨 뒤 immutable validated DB에 증분 편입하라.
신규 작품 validator와 전역 registry/source/encoding/database/release gate를 실행하고 최종 DB ZIP을 재해제 검증하라.
사용자 승인 전에는 PASS_CANDIDATE, 승인 후에만 CANONICAL을 사용하라.
EXT6/HXT6은 별도 승인 전까지 비활성 상태로 보존하라.
```

## 20. 최종 원칙

```text
원본은 직접 읽는다.
앙상블 폭은 넓게 스캔한다.
Arc는 실제 변화만 기록한다.
LocalEdge는 인과가 아닌 것을 제거한다.
인접성은 인과 근거가 아니다.
회차 간 연결은 Stage04에서만 확정한다.
모든 후보는 전수 처분한다.
수량은 품질 목표가 아니다.
회차 경량검증과 블록 강검증을 분리한다.
검증과 패키징을 분리한다.
실제 파일·checkpoint·validator exit code가 채팅 보고보다 우선한다.
사용자 승인 전에는 CANONICAL로 승격하지 않는다.
```
