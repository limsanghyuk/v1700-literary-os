# 새 대화창 한국 드라마 분석 즉시 실행 가이드 v3

- Document ID: `DRAMA-NEW-CONVERSATION-EXECUTION-GUIDE-V3`
- Status: `AUTHORITATIVE / CURRENT POLICY REVISION`
- Updated: `2026-07-18`
- Exact schema authority: `SCHEMA_CONTRACTS_V2.md`
- Full onboarding authority: `START_HERE_NEW_DRAMA_ANALYSIS.md`
- Version note: **문서 버전을 올리지 않고 운영 규칙만 갱신한다.**

이 문서는 새 대화창에서 새 드라마를 즉시 분석하기 위한 압축 실행 가이드다. 상세 저작 기준과 예시는 `START_HERE_NEW_DRAMA_ANALYSIS.md`를 따른다.

---

## 0. 최소 로드

새 대화창은 다음만 읽는다.

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. 신규 작품 선정 시 최신 DB 작품 인덱스 1개
4. 중단 재개 시 작품별 단일 `checkpoint.json`

과거 대화 전체와 모든 방법론 문서를 전수 조사하지 않는다.

---

## 1. 핵심 원칙

```text
직접독해와 의미 저작이 본 작업이다.
검증은 파일 손상과 명백한 계약 위반만 확인한다.
```

- Python·템플릿으로 의미 필드를 생성하지 않는다.
- 회차를 순서대로 처리한다.
- 여러 회차를 한 번에 의미 생성하지 않는다.
- GPT와 Claude는 동일 정본 스키마를 사용하는 공동 Provider다.
- Provider별 내부 메모·프롬프트·세션 방식은 달라도 된다.
- EXT6는 기본 비활성이다.
- 사용자의 명시적 승인 없이는 새 DB 릴리즈 번호를 만들지 않는다.

---

## 2. 신규 작품 선정과 SourceLock Core

```text
원본 목록
→ 최신 DB와 차집합
→ 회차 완전성
→ 중복·수정본·재수록
→ 인코딩·장면 표식
→ 가장 안정적인 신규 작품 1편
```

다음은 `SOURCE_HOLD`다.

- 회차 누락
- 충돌 판본 판별 불가
- 인코딩 복구 불가
- 장면 경계 잠금 실패
- 회차 번호와 실제 내용 불일치

작품당 SourceLock은 한 파일만 유지한다.

필수:

```text
work_id
series_title
episodes_total
source_archive_sha256
numbering_policy
scene_boundary_policy
direct_reading_required: true
python_semantic_generation: false
provider
model
run_id
status
episodes
completed_episodes
next
```

각 회차에는 source filename, bytes SHA256, canonical scene count, Q1~Q4 범위, anomaly만 기록한다. 장면별 해시는 사고가 있을 때만 추가한다.

---

## 3. 회차 처리

Q1~Q4는 극적 4막이 아니라 직접독해 분할 단위다.

```text
Q1 직접독해
→ Q2 직접독해
→ Q3 직접독해
→ Q4 직접독해
→ SceneCard
→ EpisodeMeta
→ SequenceBlueprint
→ EpisodeArc
→ CharacterArc
→ RelationshipArc
→ LocalEdge
→ PayoffCandidate
→ 정본 저장
→ 최소 구조검사
→ 단일 checkpoint
→ 다음 회차
```

한 회차의 Stage01~03을 수직으로 끝낸 뒤 다음 회차로 이동한다.

각 장면에서 확인한다.

1. 실제 행동
2. 목표·전략·은폐·회피
3. 정보·관계·권력·의존 변화
4. 선택·거부·유예
5. 회차 구조 기능
6. 다음 장면을 미는 잔여 압력

---

## 4. Stage01

SceneCard exact 9키:

```text
work_id scene_no heading title intent_gist core core2 skin by
```

CORE 16:

```text
ESTABLISH ORACLE INTRO BOND CONFLICT REVERSAL LOSS PUNISH
REVELATION REUNION RELIEF ROMANCE PERIL RESCUE DESIRE HOOK
```

SceneCard는 대사·사건 요약만 쓰지 않는다. 행동 주체, 전략, 장애, 정보·관계 변화, 선택, 구조 기능을 구체적으로 압축한다.

EpisodeMeta exact 5키:

```text
work_id scene_count core_dist episode_function by
```

---

## 5. Stage02

SequenceBlueprint exact 18키는 `SCHEMA_CONTRACTS_V2.md`를 따른다.

시퀀스 경계는 다음 변화로 결정한다.

- 목표 주체·목표
- 장애 성격
- 정보·관계·권력 가치
- 행동 계획
- POV·장소 클러스터
- 극적 방향

필수 불변식:

- 모든 장면 정확히 1개 시퀀스
- 누락·중복 0
- span·budget 일치
- runtime 합 1.0
- core_mix 원본 SceneCard 근거
- seq_index 연속

turn_type 11종:

```text
RISE BOND PUNISH FALL LOSS REVEAL ORACLE REVERSAL STALL HOOK CONFLICT
```

turn_class:

```text
RISE FALL REVEAL STALL
```

---

## 6. EpisodeArc와 Stage03

EpisodeArc exact 13키는 스키마 계약을 따른다. 실제 entry→turning point→exit 변화와 회차 기능을 기록한다.

### CharacterArc

```text
이전 상태 → trigger → 선택·거부 → 새 상태 → 후속 영향
```

실제 변화가 있는 인물만 기록한다.

### RelationshipArc

신뢰·권력·정보 비대칭·의존·적대·거래·은폐·공모·보호·통제·위계의 실제 변화만 기록한다. trigger 장면에 양쪽 인물이 등장·통화·교신해야 한다.

### LocalEdge

```text
edge_type = causal
같은 회차
gap_episodes = 0
label = target core
```

반사실 질문을 통과한 경우만 생성한다.

```text
source가 없었다면 target이 발생하지 않거나 실질적으로 달라지는가?
```

장면 인접성, 같은 시퀀스, 유사 감정은 인과 근거가 아니다.

### PayoffCandidate

구체적인 물건·정보·약속·위협·선택처럼 장거리 회수 가능성이 있는 경우만 기록한다. 수량 할당량은 없다.

---

## 7. 회차 최소 구조검사

회차마다 한 번만 실행한다.

1. JSON/JSONL parse
2. exact keyset·자료형
3. ID 중복
4. SceneCard coverage
5. Sequence 누락·중복·span·budget
6. runtime 합
7. Arc·Edge 참조 존재
8. LocalEdge same episode/gap 0
9. 필수 파일 존재

의미를 다시 채점하지 않는다. 결과는 작품별 단일 checkpoint에 기록한다.

```json
{
  "episode_no": 8,
  "direct_reading_completed": true,
  "stage01_03_saved": true,
  "structure_check": "PASS",
  "next": "EP09_Q1"
}
```

QuarterAudit, 다중 validation JSON, 블록 강경검사는 기본 절차가 아니다.

---

## 8. 단일 checkpoint

작품당 하나만 유지한다.

최소:

```text
schema
work_id
provider
source_lock
completed_episodes
current_episode
current_pointer
saved_layers
last_structure_check
stage04_status
next
notes
```

새 대화창은 checkpoint의 `current_pointer`부터 이어간다. 완료 회차를 다시 분석하지 않는다.

---

## 9. Stage04

모든 회차 Stage01~03 저장 후 한 번 수행한다.

1. 모든 PayoffCandidate를 후속 원본과 대조
2. disposition 100%
3. 실제 장거리 연결만 CrossEpisodeEdge 승격
4. FullSeriesArc 작성

권장 disposition:

```text
PROMOTED_CROSS_EDGE
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL
RESOLVED_WITHIN_EPISODE
REJECTED_DUPLICATE
REJECTED_INSUFFICIENT_EVIDENCE
REJECTED_SOURCE_MISMATCH
```

자동 회차 브리지와 규칙적 n→n+2 연결을 금지한다.

---

## 10. 작품 완료검사

전 시즌 완료 후 한 번만 수행한다.

- 전 회차 Stage01~03 존재
- ID·FK 유효
- Scene·Sequence counts 일치
- Candidate disposition 100%
- CrossEpisodeEdge 유효
- FullSeriesArc counts 일치
- 작품 ZIP 생성
- 작품 ZIP Fresh Extraction 1회

다음 상황에서만 포렌식 의미검사를 추가한다.

- 원본 불일치
- 직접독해 누락 의심
- 대량 템플릿 반복
- LocalEdge 자동·과밀 생성
- Provider 결과 충돌
- SourceLock 해시 불일치
- 정본 교체·스키마 마이그레이션
- 사용자 요청

---

## 11. DB 편입과 릴리즈 동결

- 신규 작품만 증분 편입한다.
- 기존 정본 작품을 매번 다시 의미검사하지 않는다.
- GPT·Claude provenance를 보존한다.
- `CANONICAL`은 사용자 승인으로만 사용한다.
- 작품 완료와 새 DB 릴리즈 생성을 분리한다.
- 전체 DB ZIP, 새 Governance 번호, 새 release manifest는 사용자가 명시적으로 요청할 때만 생성한다.
- 문서 변경·validator 변경·작품 추가만으로 릴리즈 번호를 올리지 않는다.

---

## 12. 기본에서 제거된 구규칙

다음은 사고 대응용으로만 보존한다.

- Quarter별 상세 감사
- 회차별 다수 증빙 JSON
- 여러 checkpoint
- 반복 checksum
- 약 8회차 의무 강검사
- 작품별·블록별·전 시즌별 중복 validator
- 회차별 ZIP/Fresh Extraction
- 동일 정보의 validation registry 중복 기록
- 신규 작품마다 전체 DB 새 릴리즈 생성

---

## 13. 금지

- 직접독해 없는 의미 생성
- Python·템플릿 의미 저작
- 여러 회차 동시 의미 생성
- 미완료 파일 완료 선언
- 장면 인접 LocalEdge 자동 연결
- 회차 간 LocalEdge
- 고정 Arc·Edge·Candidate 수량
- 미처리 PayoffCandidate
- 사용자 승인 없는 CANONICAL
- 기본 분석에서 QuarterAudit·블록 강검사 강제
- 사용자 승인 없는 릴리즈 증가
- EXT6 자동 적용

---

## 14. 권위 우선순위

1. `SCHEMA_CONTRACTS_V2.md` — exact schema
2. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 상세 운영 정책
3. 이 문서 — 즉시 실행 요약
4. 작품 SourceLock·checkpoint
5. 과거 playbook·incident 문서

과거 문서와 충돌하면 현재 간소화 정책이 우선한다.
