# 드라마 분석 현재 운영 보충 규범 — 2026-07-15

- Document ID: `DRAMA-ANALYSIS-CURRENT-OPERATING-SUPPLEMENT-2026-07-15`
- Status: `AUTHORITATIVE_CANDIDATE`
- Scope: 한국드라마04 원본 직접독해, Stage01~04, seqcard_ko 데이터베이스 삽입·업그레이드
- Exact schema authority: `docs/drama_analysis/SCHEMA_CONTRACTS_V2.md`
- Timezone: Asia/Seoul

## 0. 이 문서의 역할

이 문서는 새 대화창·새 모델·새 실행 환경이 과거 대화 전체를 읽지 않고도 드라마 한 작품을 선택하여 원본 해제, SourceLock, 회차별 4등분 직접독해, Stage01~03 검증, Stage04 전 시즌 fan-in, 독립 작품 패키지 생성, `seqcard_ko` 데이터베이스 삽입까지 수행하도록 만든 현재 운영 보충 규범이다.

이 문서는 Stage01~04 exact schema를 변경하지 않는다. exact keyset·자료형·enum·ID·FK·불변식은 항상 `SCHEMA_CONTRACTS_V2.md`가 우선한다.

## 1. 현재 권위 관계

충돌 시 다음 순서를 적용한다.

1. `SCHEMA_CONTRACTS_V2.md` — Stage01~04 exact schema·enum·ID·불변식
2. 이 문서 — 현재 실행 단위, 데이터베이스 삽입, EXT6 보류 정책
3. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 직접독해 방식·내용 깊이
4. `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md` — 강한 검증·릴리스
5. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — 계보·패키지·핸드오프
6. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 세션 안전·중단 복구
7. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json` — 현재 데이터베이스 상태와 다음 후보
8. 최신 `docs/sessions/*drama*/README.md` — 실제 작업 이력·재진입 지점

`docs/drama_analysis/README.md`는 단일 진입점이고, 위 문서군을 순서대로 연결한다.

## 2. 현재 확정 운영 결정

```text
Stage01~04 exact schema = v2 유지
v3 = 직접독해·검증·세션 안전·계보 강화
EXT6 = 기본 비활성, 별도 sidecar, 추후 재검토
기존 Stage04 완료작과 교차품질 비교 = 기본 필수 아님
품질 판정 = 동일 작품 내부의 원본·Stage01~03·Stage04 강검증으로 결정
CANONICAL = 사용자 승인 전 금지
```

## 3. 작업 단위와 8회차 블록

### 3.1 의미 저작 최소 단위

```text
1 episode = Q1 → Q2 → Q3 → Q4
```

Quarter는 극적 4막이 아니라 집중력 유지와 자동화 전환 방지를 위한 독해 구간이다.

### 3.2 원자 트랜잭션

```text
한 실행의 안전 범위 = 1 episode
```

한 회차의 Q1~Q4, Stage02, Stage03, 강한 게이트, 체크포인트가 영속화된 뒤에만 다음 회차로 이동한다.

### 3.3 사용자·개발자 전달 블록

현재 데이터베이스 구축 기본 블록은 8회차다.

```text
EP01 Q1→Q4→회차 잠금
→ ...
→ EP08 Q1→Q4→회차 잠금
→ EP01~EP08 통합 게이트
→ 다음 8회차 블록
```

예:

- 16부작: EP01~08 / EP09~16
- 20부작: EP01~08 / EP09~16 / EP17~20
- 24부작: EP01~08 / EP09~16 / EP17~24
- 31부작: EP01~08 / EP09~16 / EP17~24 / EP25~31

8회차를 한 번에 의미 생성하지 않는다. 내부 저작·검증·잠금은 항상 회차별이다.

## 4. 작품 선정과 데이터베이스 preflight

1. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json`에서 `STAGE01_04_COMPLETE` 작품을 제외한다.
2. 신규 작품이면 한국드라마04 원본 archive에서 회차 파일 존재·인코딩·장면 경계를 조사한다.
3. 업그레이드 작품이면 기존 Stage01·02·EpisodeArc와 원본 가용성을 확인한다.
4. 원본은 로컬/개발자용 데이터베이스의 다음 경로에 정규화해 저장한다.

```text
seqcard_ko/original_extracted/<작품>/<작품>_<NN>.txt
```

5. GitHub 허브에는 원문·대사·raw script를 커밋하지 않는다. 허브에는 SourceLock, SHA256, 장면 수, 검증·manifest·보고서만 기록한다.
6. SourceLock v2를 만들고 다음을 잠근다.
   - archive/file SHA256
   - 인코딩
   - canonical scene count
   - 물리 marker 이상
   - canonical ordinal 정책
   - quarter ranges
   - scene/heading hashes
   - 현재 완료 범위와 next pointer

SourceLock이 실패하면 Stage01을 시작하지 않는다.

## 5. Stage01 — SceneCard 직접독해

정본 저장은 exact 9키다.

```text
work_id, scene_no, heading, title, intent_gist,
core, core2, skin, by
```

### 5.1 내부 독해 질문

각 장면에서 반드시 다음을 구분한다.

1. 행동: 실제로 무엇이 일어났는가
2. 전략: 누가 무엇을 말하고, 숨기고, 피하고, 행동으로 대신했는가
3. 정보 변화: 어떤 사실·오해·관계 조건이 변했는가
4. 선택: 누가 무엇을 선택·거부·유예했는가
5. 구조 기능: 회차에서 이 장면이 왜 필요한가
6. 잔여 동력: 다음 장면·시퀀스를 구체적으로 밀어내는 원인은 무엇인가

이 여섯 질문은 사고 도구다. 정본에는 `title/intent_gist/core/core2/skin`으로 압축하되 같은 문장을 필드마다 반복하지 않는다.

### 5.2 의미 깊이

```text
4점: 행동·전략·정보·선택·구조 기능·다음 동력이 모두 구체적
3점: 대부분 구체적이나 한 축이 약함
2점: 사건 요약은 있으나 선택·정보 변화가 추상적
1점: 키워드·템플릿 중심
0점: 자동 생성·복사·환각
```

권장 기준:

```text
회차 평균 >= 3.0
최저 >= 2.5 또는 재저작
0점/1점 장면 = 0
```

### 5.3 금지

- 키워드 조각을 문장처럼 확장
- `[EPxx-Syy: ...]` 참조 표식 잔류
- 장면 요약을 여러 필드에 복사
- 여러 장면의 동일 골격 반복
- 원문에 없는 인물·행동·감정·인과
- Python/템플릿으로 title·intent·CORE 생성

## 6. Stage02 — SequenceBlueprint

exact 18키:

```text
seq_id, work_id, episode_no, seq_index,
member_scene_nos, scene_span, scene_budget,
sequence_intent, goal, obstacle, value_shift,
turn_type, turn_class, core_mix, pov_char,
place_cluster, runtime_share, by
```

### 6.1 시퀀스 경계

장면 수 균등분할이 아니라 다음 변화로 나눈다.

- 목표 주체 또는 목표 변화
- 장애 성격 변화
- 정보·관계·권력 가치 전환
- 새로운 극적 행동 단위 시작

### 6.2 필수 불변식

```text
I-COVER: 모든 장면이 정확히 하나의 sequence에 포함
I-PARTITION: 중복 0 / 누락 0
I-COUNT: sum(scene_budget) == scene_count
runtime_share sum == 1.0 ± 1e-6
core_mix ⊆ member SceneCard의 실제 core/core2
sequence_count / scene_count >= 0.11
```

`turn_type` 11종과 `turn_class` 파생은 `SCHEMA_CONTRACTS_V2.md`를 그대로 따른다.

## 7. Stage03 — 회차 렛저

Stage03은 Stage01·02를 직접 다시 읽고 회차별로 저작한다. 메타데이터 자동 파생이나 회차 요약 복사는 금지한다.

### 7.1 EpisodeArc — exact 13키

실제 시퀀스 전환을 근거로 극적 질문, entry/exit, turning point, 중심 갈등축, episode function, act structure를 작성한다. 모든 회차를 기계적으로 4막으로 만들지 않는다.

### 7.2 CharacterArc — exact 8키

```text
인물 × 실제 변화가 발생한 회차
```

- trigger scene에 해당 인물이 실제 등장
- state_delta는 그 회차의 변화량
- 단순 등장·수량 채우기 금지
- 같은 evidence를 여러 인물에게 복사 금지

### 7.3 RelationshipArc — exact 9키

```text
관계쌍 × 실제 상호작용·관계변화 회차
```

- trigger scene에 양쪽 인물이 함께 등장하거나 직접 통화·교신
- `(A,B)`와 `(B,A)` 중복 금지
- relation_state와 relation_delta 분리

### 7.4 LocalEdge — exact 12키

```text
edge_type == causal
src_episode_no == tgt_episode_no
gap_episodes == 0
label == target SceneCard.core
```

단순 번호 인접성·유사 주제·시퀀스 순서는 인과가 아니다.

### 7.5 PayoffCandidate — exact 7키

허용 guess:

```text
plant_payoff, callback, subplot_counterpoint, resolved_here
```

후속 회차를 확인하기 전에는 CrossEpisodeEdge로 승격하지 않는다.

## 8. Stage01~03 전 시즌 통합 검증

Stage04 전에 작품 전 회차 Stage01~03를 하나의 validator로 전수 검사한다.

필수 검사:

- SourceLock scene count와 Stage01 일치
- heading/hash alignment
- exact keyset·type·enum
- Stage02 coverage/partition/count/runtime/density/core_mix
- EpisodeArc act tiling·turning point FK
- CharacterArc trigger participant
- RelationshipArc 양쪽 participant
- LocalEdge 동일 회차·target core·구체 인과
- PayoffCandidate ID·scene reference·enum
- 작품 전체 ID 고유성
- title/intent/evidence/note 정확 중복
- 인물·장소·CORE 마스킹 후 골격 반복
- placeholder·미치환 변수·키워드 artifact
- Python 의미 생성 흔적

한 건이라도 blocking error가 있으면 Stage04로 이동하지 않는다.

기존 Stage04 완료 작품과의 교차품질 비교는 기본 게이트가 아니다. 신규 작품의 품질은 그 작품의 원본 근거와 내부 강검증으로 판정한다. 교차비교는 기준이 없거나 별도 연구가 필요할 때만 선택적으로 수행한다.

## 9. Stage04 — 전 시즌 fan-in

전 회차 Stage01~03가 잠긴 뒤 별도 실행으로 수행한다.

```text
PayoffCandidate 전수 목록화
→ 원 장면 재확인
→ 후속 실제 회수·변형·반향 장면 확인
→ source/target 의미 대조
→ 후보별 disposition
→ 검증된 연결만 CrossEpisodeEdge
→ FullSeriesArc 재종합
```

### 9.1 CandidateDisposition

모든 후보에 다음 중 하나를 기록한다.

```text
PROMOTED_CROSS_EDGE
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL
RESOLVED_WITHIN_EPISODE
REJECTED_DUPLICATE
REJECTED_INSUFFICIENT_EVIDENCE
REJECTED_SOURCE_MISMATCH
```

미처리 후보가 한 건이라도 있으면 Stage04 완료가 아니다.

### 9.2 CrossEpisodeEdge

- exact 12키
- target episode > source episode
- gap 산술 일치
- 허용 유형: callback, plant_payoff, subplot_counterpoint
- target label == target SceneCard.core
- 이전 화 마지막 → 다음 화 첫 장면 자동 브리지 금지
- 동일 처분문·동일 note 일괄 복사 금지

### 9.3 FullSeriesArc — exact 17키

실제 시퀀스·인물·복선의 매크로 전환을 기준으로 logline, central question, theme, protagonist/antagonist, season movements, macro turning points, resolution, open ending, tone, 잔여 갈등, core distribution을 작성한다.

## 10. EXT6 현재 정책

```text
DEFAULT_ENABLED = false
STATUS = DEFERRED_OPTIONAL_SIDECAR
```

EXT6은 Stage01~04 exact schema를 변경하지 않는 별도 sidecar다. 현재는 장편 한 작품의 컨텍스트·실행 한도 압박이 크므로 신규 분석·업그레이드의 기본 범위에서 제외한다.

- EXT6 파일럿·역사 산출물은 삭제하지 않는다.
- Stage01~04 데이터베이스 완료 수에 EXT6 존재 여부를 포함하지 않는다.
- 명시적 사용자 승인, 별도 실행 예산, 1회차 파일럿, 독립 lineage가 있을 때만 다시 활성화한다.
- 상세 계약은 `EXT6_DEFERRED_SIDECAR_POLICY_V1.md`와 `DRAMA_STAGE_EXT6_CONTRACT_MATRIX_V3.md`에 별도 보존한다.
- EXT6 비활성 작업에서는 validation Gate 4를 `NOT_APPLICABLE_EXT6_DEFERRED`로 기록하며 실패로 보지 않는다.

## 11. Python 경계

### 허용

- ZIP 해제·인코딩 복구
- scene marker 탐지·ordinal 생성
- SHA256·offset·line span
- Q 범위 계산
- JSON/JSONL 직렬화
- 스키마·coverage·FK·중복·반복 검사
- deterministic correction: runtime 합계, ID/FK 표기, 실제 core 기반 core_mix 정리
- manifest·SHA256SUMS·ZIP 생성
- 휴대형 validator 실행

### 금지

- SceneCard 의미 문장·CORE 생성
- Sequence goal/obstacle/value_shift 생성
- CharacterArc/RelationshipArc 의미 생성
- LocalEdge/Payoff/CrossEdge 의미 생성
- Stage04 승격·처분 판단 자동화
- FullSeriesArc 의미 생성

결정론적 계약 보정과 의미 재저작을 구분한다. 의미 결함은 원문 재독해 후 새 lineage로 작성한다.

## 12. 패키지와 데이터베이스 삽입

### 12.1 개발자 독립 작품 패키지

```text
<work>_stage01_04_full_series_<version>/
  README.md
  authored/
  authored_seq/
  authored_arc/
  authored_chararc/
  authored_relarc/
  authored_edges/
  quarter_audits/
  source_lock/
  validation/
  reports/
  lineage/
  FINAL_MANIFEST.json
  SHA256SUMS.txt
```

사용자가 지시한 로컬/개발자용 패키지는 `original_extracted/`를 포함할 수 있다. 이 경우 manifest에 원본 포함 사실과 사용자 지시를 명시한다. GitHub 허브에는 raw source를 커밋하지 않는다.

### 12.2 seqcard_ko 직접 삽입

검증된 작품 파일을 같은 디렉터리 규격으로 삽입한다.

```text
seqcard_ko/authored/
seqcard_ko/authored_seq/
seqcard_ko/authored_arc/
seqcard_ko/authored_chararc/
seqcard_ko/authored_relarc/
seqcard_ko/authored_edges/
seqcard_ko/original_extracted/<work>/
```

삽입 후:

1. 파일명·work_id·episode_no 정규화
2. 작품 전체 ID 중복 검사
3. `_ALL_series_arc.json` 재집계
4. 작품·회차·SceneCard·Stage04 완료 수 갱신
5. 전체 DB validator 실행
6. SHA256SUMS·ZIP CRC·fresh extraction 재검증
7. 독립 작품 ZIP과 전체 DB ZIP을 개발자에게 함께 제공

## 13. 최종 릴리스 조건

```text
errors == 0
blocking warnings == 0
candidate disposition == 100%
automatic episode bridge == 0
raw source hub commit == 0
python semantic generation == false
package SHA/CRC == PASS
```

상태:

- 검증 통과·사용자 승인 전: `PASS_CANDIDATE`
- 사용자 승인 후: `CANONICAL`
- 실패·오염: `QUARANTINE`
- 대체된 과거본: `SUPERSEDED`

## 14. 중단 복구

대화에서 “완료”라고 말했더라도 파일·validation·checkpoint가 없으면 미완료다.

재시작 시 확인:

1. SourceLock.current_completed_episodes
2. SourceLock.next
3. 직전 회차 QuarterAudit 4건
4. Stage01~03 파일 존재
5. validation PASS
6. checkpoint checksum

필요 컨텍스트만 로드한다.

```text
권위 인덱스·exact schema
직전 SourceLock
직전 checkpoint manifest
현재 회차 원본
누적 PayoffCandidate index
```

## 15. 새 대화창 즉시 실행 절차

```text
1. docs/drama_analysis/README.md 읽기
2. DRAMA_ANALYSIS_AUTHORITY_INDEX_V3.md 읽기
3. SCHEMA_CONTRACTS_V2.md exact keyset 로드
4. 이 운영 보충 규범 읽기
5. DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json 읽기
6. 완료 작품 제외·작품 1편 선정
7. 원본 archive inventory 및 SourceLock v2 생성
8. 8회차 블록 계획 고정
9. EP01 Q1 직접독해 시작
10. 각 회차 영속화 후 다음 회차
11. 작품 전체 Stage01~03 강검증
12. Stage04 fan-in
13. 독립 ZIP·DB 통합 ZIP 생성
```

### 새 대화창 재개 지시문

```text
개발자 허브의 docs/drama_analysis/README.md, DRAMA_ANALYSIS_AUTHORITY_INDEX_V3.md,
SCHEMA_CONTRACTS_V2.md, DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md,
DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json을 순서대로 읽어라.
EXT6은 기본 비활성 sidecar로 보류한다.
현재 데이터베이스의 Stage01~04 완료 작품을 제외하고 작품 1편을 선정하라.
원본을 original_extracted에 정규화하고 SourceLock v2를 만든 뒤,
8회차 블록을 계획하되 실제 저작은 회차별 Q1→Q4·체크포인트로 수행하라.
전 회차 Stage01~03 강검증 후 Stage04 fan-in을 완료하고,
독립 작품 ZIP과 갱신된 seqcard_ko 전체 DB ZIP을 제공하라.
Python은 추출·직렬화·검증·패키징에만 사용하라.
```
