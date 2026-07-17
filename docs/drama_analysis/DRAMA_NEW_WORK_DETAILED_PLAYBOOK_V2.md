# 신규 드라마 분석 상세 플레이북 v2

- Document ID: `DRAMA-NEW-WORK-DETAILED-PLAYBOOK-V2`
- Status: `AUTHORITATIVE_COMPANION`
- Updated: 2026-07-17
- Execution authority: `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`
- Exact schema authority: `SCHEMA_CONTRACTS_V2.md`
- Machine policy authority: `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json`
- Latest DB status: `DRAMA_ANALYSIS_DATABASE_STATUS_V12.json`
- EXT6/HXT6: 기본 비활성
- Promotion: 사용자 승인 전 `PASS_CANDIDATE`, 승인 후에만 `CANONICAL`

## 0. 목적

이 문서는 새 대화창이 V3 실행 가이드의 압축 규칙을 실제 신규 작품 분석에 바로 적용하도록 만든 상세 해설서다. 원본 직접독해, Stage01~04, 클로드식 앙상블 폭, LocalEdge 선택성, 후보 전수 처분, 구조·의미 이중 검증, 패키징·DB 편입을 하나의 실행 흐름으로 설명한다.

이 문서는 V3·Schema·Manifest를 대체하지 않는다.

```text
1. SCHEMA_CONTRACTS_V2
2. DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3
3. DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5
4. DRAMA_ANALYSIS_DATABASE_STATUS_V12
5. 이 상세 플레이북
6. ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY
7. CLOSE_READING_MASTER_PROTOCOL
8. LINEAGE_PACKAGE_HANDOFF
```

## 1. 새 대화창 로드

### 공식 최소 실행 세트

```text
1. DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md
2. SCHEMA_CONTRACTS_V2.md
3. 신규 작품 선정 시 DRAMA_ANALYSIS_DATABASE_STATUS_V12.json 또는 최신 작품 인덱스
4. 원본 아카이브
```

### 처음 적용하는 모델의 상세 온보딩

```text
1. DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md
2. DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md
3. SCHEMA_CONTRACTS_V2.md
4. DRAMA_ANALYSIS_DATABASE_STATUS_V12.json
```

과거 대화 전체·모든 세션 README·모든 역사 문서를 시작 전에 전수 조사하지 않는다.

## 2. 완료 판정의 3축

```text
STRUCTURAL_PASS
+ SEMANTIC_QUALITY_PASS
+ PACKAGE_FRESH_EXTRACTION_PASS
= PASS_CANDIDATE
```

- JSON·schema·coverage가 통과해도 의미 품질이 낮으면 완료가 아니다.
- 의미 품질이 좋아도 SourceLock·checksum·Fresh extraction이 실패하면 릴리스가 아니다.
- 사용자 승인 전 `CANONICAL`로 승격하지 않는다.
- 하나라도 실패하면 `FAIL_SEMANTIC_REVIEW_REQUIRED`, `QUARANTINE`, 또는 `SOURCE_HOLD`다.

## 3. 고정 파이프라인

```text
source archive inventory
→ 최신 DB와 작품 차집합
→ 신규 작품 1편 선택
→ original_extracted/{작품명}/ UTF-8 원본 저장
→ SourceLock
→ EP01 Q1~Q4 직접독해·QuarterAudit
→ Stage01 SceneCard
→ EpisodeMeta
→ Stage02 SequenceBlueprint·EpisodeArc
→ Stage03 CharacterArc·RelationshipArc·LocalEdge·PayoffCandidate
→ episode light gate·checkpoint
→ 다음 회차 반복
→ 전반부/약 8회차 structural+semantic strong gate
→ 후반부 동일 절차·strong gate
→ full Stage01~03 dual gate
→ Stage04 candidate disposition 100%
→ CrossEpisodeEdge·FullSeriesArc
→ individual ZIP·Fresh extraction
→ immutable base에 증분 DB 편입
→ 신규 작품 structural+semantic validator·전역 gate
→ DB ZIP·Fresh extraction
→ PASS_CANDIDATE
```

## 4. 속도와 품질의 절대 규칙

```text
의미 독해 최소 단위 = quarter
의미 저작 원자 단위 = 1 episode
결정론적 직렬화 묶음 = 최대 4 episodes
강검증 블록 = 전반부 또는 약 8 episodes
Stage04 = full-series fan-in 1회
Fresh extraction = 최종 작품 ZIP 1회 + 최종 DB ZIP 1회
```

- Python·템플릿으로 의미 필드를 생성하지 않는다.
- 여러 회차 원문을 한 번에 넣어 의미 레코드를 일괄 생성하지 않는다.
- Quarter checkpoint 없이 반 시즌이 갑자기 완성되거나 동일 문장 골격이 대량 반복되면 속도 이상 감사를 실행한다.
- 회차마다 강검증·전체 SourceLock 재검사·ZIP·Fresh extraction을 반복하지 않는다.
- 수량 할당량을 채우기 위해 Arc·Edge·Payoff를 만들지 않는다.

## 5. 신규 작품 선택과 SourceLock

### 작품 선택

```text
원본 아카이브 inventory
→ 최신 DB 작품 인덱스와 차집합
→ 회차 완전성·인코딩·중복 판본·재수록 구간·장면 경계 비교
→ 원본 안정성이 가장 높은 신규 작품 1편
```

실제 회차 누락, 충돌 판본, 위장 회차, 장면 경계 잠금 실패, 인코딩 복구 불가는 `SOURCE_HOLD`다.

### 원본 저장

```text
seqcard_ko/original_extracted/{작품명}/
  {작품명}_01.txt
  {작품명}_02.txt
  ...
```

### SourceLock 이중 증거

```text
original_bytes_sha256
= 입수 ZIP/HWP/CP949/UTF-16 원래 바이트

canonical_storage_sha256
= original_extracted에 저장된 UTF-8 TXT 바이트
```

필수:

- 작품명·실제 회차 번호
- 원본·UTF-8 저장본 SHA256
- canonical `scene_no=1..N`
- 회차별 장면 수·Q1~Q4 범위
- 중복·재수록·제외 장면 대응표
- source marker anomaly
- `direct_reading_attested`
- `python_semantic_generation:false`
- `next_pointer`

SceneCard JSON 해시를 원본 해시로 기록하면 실패다.

## 6. 장면 경계와 Quarter

1. HWP/TXT의 물리 표식·문단 스타일·번호형 heading을 조사한다.
2. 장소·시간·행동 단위가 실제로 바뀌는 논리 장면을 확정한다.
3. 회차 간 재수록 장면은 후속 회차 정본에서 제외하고 원본→정본 대응을 SourceLock에 기록한다.
4. canonical ordinal은 `1..N` 연속이어야 한다.

Quarter는 극적 4막이 아니라 독해·영속화 단위다.

- 장면 경계를 자르지 않는다.
- 총 장면 수를 약 25%씩 균형 분할한다.
- 사건 덩어리를 깨지 않는다.
- Quarter 종료 즉시 부분 Stage01·QuarterAudit·checksum을 저장한다.

## 7. 회차 실행 루프

```text
Q1 원문 직접독해 → Stage01 부분 저장 → QuarterAudit
Q2 원문 직접독해 → Stage01 부분 저장 → QuarterAudit
Q3 원문 직접독해 → Stage01 부분 저장 → QuarterAudit
Q4 원문 직접독해 → Stage01 완성 → QuarterAudit
→ EpisodeMeta
→ SequenceBlueprint
→ EpisodeArc
→ CharacterArc
→ RelationshipArc
→ LocalEdge
→ PayoffCandidate
→ episode light gate
→ checkpoint·next_pointer
```

Stage03 네 계층은 회차별 수직 처리한다. 계층별로 전 시즌을 반복해서 읽지 않는다. 의미 초안이 끝난 회차의 결정론적 직렬화만 최대 4회차 묶음이 가능하다.

## 8. 장면 직접독해 6질문

1. **행동** — 실제로 누가 무엇을 했는가.
2. **전략** — 누가 무엇을 말하고, 숨기고, 피하고, 유도했는가.
3. **정보·관계 변화** — 누가 무엇을 새로 알거나 오해하고, 권력 조건이 어떻게 변했는가.
4. **선택** — 누가 무엇을 결정·거부·유예했는가.
5. **구조 기능** — 설정·압박·전환·회수 중 무엇을 수행하는가.
6. **잔여 압력** — 어떤 구체적 미해결 원인이 다음 장면·시퀀스를 미는가.

이를 새 키로 추가하지 않고 `title`, `intent_gist`, `core/core2`, `skin`에 서로 다른 역할로 압축한다.

## 9. Stage01 의미 품질

SceneCard exact 9키는 schema 문서를 따른다.

- `heading`: 원본 provenance와 대응
- `title`: 장면의 고유 전환
- `intent_gist`: 욕망·전략·정보/관계 변화·선택·구조 기능
- `core/core2`: 실제 극적 기능
- `skin`: 표면 장르·연출 질감

내용 깊이 0~4:

- 0: 원문 불일치·환각·placeholder
- 1: 사건·대사 요약만 있음
- 2: 행동 주체와 표면 목적은 있으나 선택·변화가 약함
- 3: 행동·전략·정보/관계 변화·구조 기능이 구체적
- 4: 선택·가치 이동·잔여 인과 압력까지 원문 근거로 설명

권장 게이트:

```text
회차 평균 >= 3.0
2.5 미만 장면 재검토
0점·1점 장면 = 0
```

금지:

- 원문 파편을 제목에 기계적으로 접합
- 모든 intent의 동일 종결 문장
- 인물명·장소명만 교체한 동일 골격
- 필드 간 동일 요약 복사
- 원문에 없는 인물·감정·인과
- 장문 대사 복사

## 10. Stage02·EpisodeArc

SequenceBlueprint exact 18키와 EpisodeArc exact 13키는 schema 문서를 따른다.

시퀀스 경계:

- 목표 주체·목표 변화
- 장애 성격 변화
- 정보·관계·권력 가치 변화
- POV·행동 계획 변화
- 새로운 극적 행동 단위

불변식:

```text
모든 장면이 정확히 한 sequence에 포함
누락 0 / 중복 0
sum(scene_budget) == scene_count
sum(runtime_share) == 1.0 ± 1e-6
sequence_count / scene_count >= 0.11
권장 밀도 0.12~0.17
core_mix는 member SceneCard의 실제 core/core2만 사용
```

시퀀스 수를 수학적으로 4등분해 act를 만들지 않는다. 회차 내 `goal`, `obstacle`, `sequence_intent` 복사를 금지한다.

## 11. Stage03 — 클로드식 앙상블 폭의 채택

### 채택하는 장점

회차마다 다음 층을 폭넓게 스캔한다.

- 주인공·대립자
- 핵심 조력자·경쟁자
- 조직 내부 의사결정자
- 반대 진영 기능 인물
- 반복 등장 실무자·가족·동료
- 이번 회차에서 사건축을 바꾼 단역
- 동맹·경쟁·상하·공모·거래·은폐 관계

### 배제하는 방식

- 등장인물 전원을 기계적으로 CharacterArc화
- 모든 관계쌍을 RelationshipArc화
- 회차별 고정 수량 채우기
- 같은 evidence 복사
- 과도한 LocalEdge
- 장면 인접성 자동 연결
- 회차 간 LocalEdge
- 미처리 PayoffCandidate

### A/B/C 분류

- **A**: 회차 시작과 끝의 상태가 실제로 달라진 인물
- **B**: 신뢰·권력·정보·의존·적대 조건이 이동한 관계쌍
- **C**: 단순 등장 또는 변화 없음

Stage03 대상은 A와 B다. C를 수량 때문에 기록하지 않는다.

앙상블 감사:

```text
실제 변화가 있는데 빠진 핵심 의사결정자가 있는가?
실제 변화가 있는데 빠진 동맹·갈등·상하 관계가 있는가?
수량을 맞추기 위해 변화 없는 인물·관계를 넣었는가?
```

## 12. CharacterArc·RelationshipArc

CharacterArc:

- 인물×회차 단위
- trigger 장면에 실제 등장
- `state_label`은 회차 종료 상태
- `state_delta`는 이번 회차 변화량
- 단순 등장·고정 수량 금지

RelationshipArc:

- 관계쌍×회차 단위
- trigger 장면에 양쪽 인물이 함께 등장·통화·교신
- `(A,B)`와 `(B,A)` 중복 금지
- 신뢰·권력·정보·의존·적대의 실제 변화만 기록

## 13. LocalEdge — 선별적 동일 회차 인과

하드 게이트:

```text
edge_type == causal
src_episode_no == tgt_episode_no
gap_episodes == 0
label == target SceneCard.core
source/target scene exists
```

반사실 질문:

```text
source가 없었다면 target 사건이 발생하지 않거나 실질적으로 달라지는가?
```

아니라면 LocalEdge로 만들지 않는다.

배제:

- 번호 인접성
- 같은 시퀀스
- 유사 감정·주제
- 모든 장면 next-scene 사슬
- 회차 간 LocalEdge
- 수량 목표

감사 trigger:

```text
LocalEdge / SceneCard > 0.10
adjacent-target ratio > 0.50
```

자동 FAIL은 아니지만 수동 선택성 감사 없이 PASS할 수 없다. 회차 간 LocalEdge는 blocking error다.

## 14. PayoffCandidate·Stage04

PayoffCandidate는 장거리 회수 가능성이 구체적인 물건·정보·약속·위협·선택만 남긴다. 다음 장면에서 닫히는 문제, 일반 대사, 회말이라는 이유만의 후보는 제외한다.

후보 원장:

```text
OPEN → TARGET_FOUND → PROMOTE / REJECT / RECLASSIFY
```

전 시즌 Stage01~03 dual pass 후 Stage04를 한 번 수행한다.

```text
모든 후보 목록화
→ 원 장면 재확인
→ 후속 회수·변형·반향 장면 확인
→ 후보별 disposition
→ 검증된 연결만 CrossEpisodeEdge
→ FullSeriesArc 재종합
```

```text
미처리 후보 = 0
```

금지:

- 이전 회 마지막→다음 회 첫 장면 자동 브리지
- 규칙적 `EP n → EP n+2` 자동 배치
- 소수 target 장면에 CrossEdge 집중
- 멀다는 이유만의 복선·회수
- 후보 일괄 승격
- 동일 note 복사

동일 target에 CrossEpisodeEdge가 3건 이상 집중되면 수동 의미 감사를 실시한다.

## 15. 검증 cadence

### Episode Light Gate

- parse·exact schema·ID
- SceneCard coverage
- Sequence partition·runtime
- trigger·edge reference existence
- LocalEdge same episode/gap0
- checkpoint·next_pointer

회차마다 전역 반복·앙상블 누락·LocalEdge 밀도·Stage04·ZIP을 반복 검사하지 않는다.

### Half-season / 8-episode Strong Gate

#### 구조

- exact schema·enum·ID·FK
- SceneCard coverage
- Sequence partition·density·core_mix
- EpisodeArc act tiling·turning point
- ID 전역 유일성

#### 의미

- 원문 대비 title·intent 정확성
- exact semantic duplicate 0
- masked skeleton repetition 감사
- 동일 종결 템플릿·메타데이터 파생 흔적 0
- CharacterArc trigger participant
- RelationshipArc 양쪽 participant·역방향 중복 0
- 앙상블 변화 누락
- LocalEdge 반사실 인과·밀도·인접성
- PayoffCandidate 근거·중복

반복 임계:

```text
largest masked skeleton group > 5% → FAIL 또는 재저작
전체 반복 비율 > 15% → FAIL 또는 재저작
3건 이상 동일 skeleton → 수동 감사
```

### Full-series Gate

- Stage01~03 구조·의미 dual pass
- 전체 FK·coverage·반복성
- 앙상블 누락·수량 채우기
- 회차 간 LocalEdge 0
- Stage04 진입 가능 여부

### Speed Anomaly Audit

다음이면 독립 감사한다.

- quarter/checkpoint 없이 반 시즌 또는 전 시즌 완성
- 같은 시각에 대량 증빙 일괄 생성
- 회차별 Arc·Edge·Payoff 수가 기계적으로 동일
- 문법 붕괴·원문 파편형 제목·동일 종결 템플릿

## 16. 계보·증빙·패키징

```text
source → run → validation → checkpoint → comparison → promotion
```

GPT·Claude·다른 모델 run은 별도 `run_id`를 사용한다. 서로 다른 SceneCard ordinal lineage를 부분 혼합하지 않는다.

Quarantine:

- Python 의미 생성
- keyword/template artifact
- source mismatch·잘못된 scene boundary
- Stage01 의미 FAIL
- Stage02 coverage FAIL
- 허위 Arc·Edge·Payoff

독립 작품 패키지는 raw quarter evidence를 보존한다. 운영 DB는 bulk evidence를 기본 제외하고 SourceLock·provenance에 attestation, counts, aggregate hash, 독립 작품 ZIP SHA, semantic-quality report를 남긴다.

## 17. 검증과 패키징 분리

```text
Process A — validation-only
STRUCTURAL_PASS + SEMANTIC_QUALITY_PASS
→ VALIDATION_PASS

Process B — package-only
manifest·checksum → ZIP → 별도 디렉터리 재해제
→ 실제 CLI → pre/post tree 비교
→ PACKAGE_FRESH_EXTRACTION_PASS
```

## 18. 전체 DB 증분 편입

이전 DB가 고정 ZIP SHA, 외부 Fresh Extraction 검증서, pre/post mismatch 0, current registry PASS를 가지면 immutable validated base로 계승한다.

```text
previous certified release
+ new work structural validator
+ new work semantic-quality validator
+ new SourceLock
+ full registry/source/encoding/database/release gates
+ final fresh extraction
```

이전 tree가 바뀌지 않았다면 기존 전 작품 의미 validator를 매번 다시 실행하지 않는다.

## 19. 완료 시 기본 전달물

한 작품 완료 보고에서 함께 제공한다.

- 개별 작품 Stage01~04 ZIP
- 개별 Fresh Extraction 검증서
- 작품을 편입한 최신 전체 DB ZIP
- 전체 DB 최종 검증서
- 각 ZIP SHA256·주요 집계

## 20. 최종 체크리스트

```text
[ ] 신규 작품 DB 차집합
[ ] 원본 UTF-8 정규 저장·SourceLock 이중 해시
[ ] QuarterAudit·checkpoint
[ ] SceneCard9 / EpisodeMeta5
[ ] Sequence18 coverage·partition·runtime·density
[ ] EpisodeArc13
[ ] CharacterArc 앙상블 누락 감사
[ ] RelationshipArc grounding·역방향 중복 0
[ ] 변화 없는 Arc 수량 채우기 0
[ ] LocalEdge cross-episode 0
[ ] LocalEdge automatic adjacency false
[ ] LocalEdge counterfactual·밀도 감사
[ ] PayoffCandidate disposition 100%
[ ] CrossEpisodeEdge automatic pattern·boundary bridge 0
[ ] Cross target concentration 감사
[ ] FullSeriesArc17 counts 일치
[ ] exact duplicate 0
[ ] masked skeleton threshold PASS
[ ] speed anomaly audit PASS
[ ] Python semantic generation false
[ ] STRUCTURAL_PASS
[ ] SEMANTIC_QUALITY_PASS
[ ] individual ZIP Fresh Extraction PASS
[ ] incremental DB global gates PASS
[ ] DB ZIP Fresh Extraction PASS
[ ] 사용자 승인 전 PASS_CANDIDATE
```

## 21. 새 대화창 복사용 실행 지시문

```text
GitHub 저장소 limsanghyuk/v1700-literary-os의 현재 드라마 분석 권위 브랜치에서
다음 문서를 순서대로 읽어라.

1. docs/drama_analysis/DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md
2. docs/drama_analysis/DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md
3. docs/drama_analysis/SCHEMA_CONTRACTS_V2.md
4. docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_V12.json

원본 아카이브와 최신 DB의 차집합으로 신규 드라마 한 편을 선정하라.
원본을 original_extracted/{작품명}/에 UTF-8 TXT로 저장하고 SourceLock 이중 해시를 작성하라.
한 회차를 Q1→Q4로 직접 읽어 Stage01→Stage02→EpisodeArc→Stage03을 수직 처리하라.

Stage03에서는 클로드식 장점인 회차별 앙상블 인물·관계 추적 폭을 채택하라.
조직·가족·팀·경쟁 진영의 실제 변화 인물과 관계를 폭넓게 스캔하되,
단순 등장·변화 없음·고정 수량 채우기는 기록하지 마라.

LocalEdge는 동일 회차의 구체적 causal 연결만 허용하라.
장면 인접성·같은 시퀀스·유사 주제를 근거로 자동 연결하지 마라.
회차 간 연결은 Stage04 CrossEpisodeEdge에서만 확정하라.
모든 PayoffCandidate를 개별 disposition하고 미처리 후보를 0으로 만들어라.
자동 회차 경계 브리지, 규칙적 n→n+2 CrossEdge, 소수 target 집중을 감사하라.

회차 경량 게이트와 전반부/약 8회차 structural+semantic strong gate를 분리하라.
구조 PASS만으로 완료를 선언하지 말고 semantic-quality report를 작성하라.
Python은 추출·해시·검증·직렬화·패키징에만 사용하라.

개별 작품 ZIP과 Fresh Extraction 검증서를 만든 뒤 immutable DB에 증분 편입하라.
신규 작품 structural/semantic validator와 전역 registry/source/encoding/database/release gate를 실행하고,
갱신 전체 DB ZIP과 최종 검증서를 같은 보고에서 제공하라.
사용자 승인 전에는 PASS_CANDIDATE, 승인 후에만 CANONICAL을 사용하라.
EXT6/HXT6은 별도 승인 전까지 비활성 상태로 보존하라.
```

## 22. 최종 원칙

```text
원본은 직접 읽는다.
앙상블 폭은 넓게 스캔한다.
Arc는 실제 변화만 기록한다.
LocalEdge는 인과가 아닌 것을 제거한다.
인접성은 인과 근거가 아니다.
회차 간 연결은 Stage04에서만 확정한다.
모든 후보는 전수 처분한다.
수량은 품질 목표가 아니다.
구조 PASS와 의미 품질 PASS를 분리한다.
속도 이상과 반복 템플릿을 감사한다.
검증과 패키징을 분리한다.
실제 파일·checkpoint·validator exit code가 채팅 보고보다 우선한다.
사용자 승인 전에는 CANONICAL로 승격하지 않는다.
```
