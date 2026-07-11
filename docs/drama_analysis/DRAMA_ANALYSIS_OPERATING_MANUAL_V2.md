# 드라마 Stage01~04 분석 운영 설명서 v2

Document ID: GPT-DRAMA-OPERATING-MANUAL-V2  
Status: AUTHORITATIVE  
Updated: 2026-07-12  
Scope: 한국드라마04 및 동일 구조의 장기 드라마 원본

## 0. 목적

이 문서는 새 대화창에서 과거 대화 내용을 보지 못하더라도, 원본 드라마 1편을 선정하여 Stage01~04 전 시즌 분석을 즉시 시작하고 동일한 품질·규격·검증 방식으로 완결하기 위한 실행 설명서다.

핵심 목표는 단순한 JSON 생산이 아니다.

```text
원문 직접독해
→ 장면별 고유 의미 저작
→ 시퀀스 구조화
→ 회차별 인물·관계·인과 렛저
→ 전 회차 검증 기반 장거리 fan-in
→ 실제 실행형 검증과 배포 증빙
```

## 1. 비타협 원칙

### 1.1 직접독해

모든 의미 필드는 원문 또는 검증된 하위 Stage를 직접 읽고 판단해 작성한다.

```text
형식 복제 ≠ 분석
메타데이터 파생 ≠ 독해
회차 요약 복사 ≠ 인물 분석
키워드 추출 ≠ 의미 저작
반복 문형 치환 ≠ 고유 저작
```

### 1.2 근거 계보

```text
원본 → SourceLock → Stage01 → Stage02 → Stage03 → Stage04
```

상위 Stage는 하위 Stage에 실재하지 않는 장면·인물·CORE·시퀀스를 만들 수 없다.

### 1.3 fail-closed

검증에서 한 건이라도 오류가 나오면 다음 단계로 넘어가지 않는다. 사람용 보고서가 PASS여도 실제 데이터가 FAIL이면 최종 판정은 FAIL이다.

### 1.4 사용자 승인 전 CANONICAL 금지

강한 게이트를 통과한 결과는 `PASS_CANDIDATE`다. 사용자 또는 지정 리뷰어가 승인한 뒤에만 `CANONICAL`로 승격한다.

## 2. 작업 단위

### 2.1 의미 저작 최소 단위: quarter

한 회차를 장면 수 기준으로 최대한 균등하게 네 구간으로 나눈다.

```text
Q1 → Q2 → Q3 → Q4
```

Quarter는 극적 4막을 뜻하지 않는다. 집중력 유지와 자동화 전환 방지를 위한 독해 단위다. EpisodeArc의 act_structure는 실제 시퀀스 전환에 따라 별도로 작성한다.

### 2.2 잠금 단위: episode

각 회차는 Q1~Q4를 순서대로 완료한 뒤 Stage01~03 통합 게이트를 통과해야 잠긴다.

```text
EP01 Q1 PASS
→ Q2 PASS
→ Q3 PASS
→ Q4 PASS
→ EP01 통합 PASS
→ EP02 Q1
```

Q1이 실패하면 Q2로 넘어가지 않는다.

### 2.3 기본 사용자 제출 단위: half-season

현재 대규모 분석의 기본 제출 방식은 전 시즌을 두 부분으로 나누는 것이다.

```text
전반부: EP01~중간회차
후반부: 다음 회차~최종회
```

중요: 반시즌을 한 번에 의미 생성하지 않는다. 내부에서는 회차별 Q1→Q4 잠금을 계속 유지한다. 내부 회차 PASS는 사용자에게 완료로 보고하고 중단할 지점이 아니다.

### 2.4 안전 축소 단위: 2 episodes

다음 조건이면 제출 범위를 2회차로 줄인다.

- 원본 scene marker가 심하게 깨짐
- 한 회차가 100장면을 크게 초과
- quarter gate에서 반복 문형·참조 오류가 누적
- 현재 세션의 안정적 직접독해 지속이 어렵다고 판단
- 사용자가 2회차 단위를 명시

축소하더라도 내부 실행은 회차별 4등분이다.

## 3. 작품 선정

한국드라마04에서 이미 완료한 작품을 제외하고 다음 기준으로 1편을 선정한다.

1. 전체 회차 파일이 존재하는가
2. 원본 텍스트 인코딩을 안정적으로 복원할 수 있는가
3. scene marker 또는 장면 블록 경계를 재현할 수 있는가
4. 전반부·후반부 장면 수가 과도하게 불균형하지 않은가
5. 기존 분석 장르 편향을 보완하는가
6. Claude 코퍼스에 동일 작품이 있어 직접 비교가 가능한가
7. 기존 GPT 패키지와 중복되지 않는가

선정 보고에는 작품명, 회차 수, 총 장면 수, 전·후반 장면 수, 경계 정책, 선정 이유를 기록한다.

## 4. 원본 입력과 SourceLock

### 4.1 원본 해제

- 외부 ZIP 안에 작품 ZIP이 있으면 중첩 ZIP을 해제한다.
- 한글 파일명 깨짐은 CP437→CP949 등 실제 인코딩을 확인해 복구한다.
- 텍스트는 UTF-8 정규화본으로 읽되 원본 bytes SHA256을 보존한다.
- 원문 전문은 최종 분석 패키지에 넣지 않는다.

### 4.2 장면 경계 정책

#### 원본 scene marker가 있는 경우

`S#N`, `#N`, `씬 N` 등의 등장 순서를 canonical ordinal로 사용한다.

```text
scene_no = 원문에서 장면 마커가 나타난 순서의 1-based ordinal
source_marker_no = 원본에 적힌 번호
```

원본 번호가 중복·결번·역순·보조번호를 포함해도 source marker는 그대로 보존하고 canonical scene_no는 연속 ordinal로 분리한다.

#### scene marker가 없는 경우

빈 줄로 분리된 의미 블록, 장소/시간 표제, 대사 묶음 등 작품별 재현 가능한 경계 규칙을 SourceLock에 명시한다. 첫 원문 행 또는 정규화 heading을 provenance로 보존한다.

### 4.3 SourceLock 필수 정보

- schema/version
- work_id
- 원본 archive 이름과 SHA256
- 회차 파일명·인코딩·bytes SHA256
- 회차별 canonical scene count
- source marker 중복·결번·역순
- canonical ordinal 정책
- 장면별 heading hash 또는 normalized scene hash
- 전반부·후반부 범위와 장면 수
- `direct_reading_required: true`
- `python_semantic_generation: false`
- `raw_script_exported: false`
- 현재 완료 범위와 next pointer

SourceLock이 통과하지 않으면 Stage01을 시작하지 않는다.

## 5. Quarter 실행 루프

각 quarter마다 다음 순서를 지킨다.

```text
1. 해당 장면 원문 직접독해
2. 장면별 Stage01 SceneCard 고유 저작
3. quarter 내부의 부분 시퀀스 경계 메모
4. title/intent 중복·placeholder 검사
5. source scene hash 대응 검사
6. QuarterAudit 기록
7. 실패 장면 재독해·보강
8. LOCKED_PASS 후 다음 quarter
```

QuarterAudit은 승인용 형식이 아니라 독해 순서와 자동화 비개입을 증명하는 원장이다.

## 6. Stage01 — SceneCard

Stage01은 전체 분석의 SSOT다. 각 장면에서 최소 다음 질문에 답해야 한다.

1. 실제로 무슨 행동이 일어났는가
2. 누가 무엇을 말하거나 숨기거나 피했는가
3. 어떤 정보·오해·관계 조건이 변했는가
4. 인물이 무엇을 선택·거부·유예했는가
5. 회차 구조에서 이 장면의 기능은 무엇인가
6. 다음 장면·시퀀스를 밀어내는 구체 원인은 무엇인가

최종 저장 스키마는 9키 SceneCard다. 상세 질문은 사고 도구이며, 여섯 문장을 기계적으로 필드화하거나 같은 사건을 반복해 쓰라는 뜻이 아니다.

### 좋은 intent_gist

- 장면의 구체적 행동
- 인물의 전략 또는 선택
- 정보·가치 이동
- 회차 구조에서의 기능

을 짧은 고유 문장에 압축한다.

### 실패 예

- 원문 단어를 `·`로 이어 붙인 키워드 조각
- `[EP03-S17: ...]` 같은 참조 표식 잔류
- 모든 장면이 “관계의 거리를 조정한다”로 끝남
- CORE 값만 바뀌는 동일 골격
- 존재하지 않는 장면 또는 인물

## 7. Stage02 — SequenceBlueprint

Q1~Q4가 끝나면 회차 전체 장면을 goal–obstacle–turn 단위로 재분절한다.

시퀀스는 다음 질문에 답한다.

- 이 구간에서 POV 인물이 얻으려는 것은 무엇인가
- 무엇이 방해하는가
- 시작과 끝의 가치 상태가 어떻게 달라지는가
- 변화의 유형과 상위 turn class는 무엇인가
- 어떤 장소·인물·CORE가 실제로 포함되는가

### 분절 원칙

- 장면 수 균등분할 금지
- 목표가 바뀌면 새 시퀀스
- 장애의 성격이 바뀌면 새 시퀀스
- 정보 공개로 가치 방향이 뒤집히면 새 시퀀스
- 장소만 바뀌어도 동일 목표가 계속되면 하나의 시퀀스일 수 있음
- intercut은 동일 극적 목표라면 함께 묶을 수 있음

회차의 모든 장면은 정확히 한 시퀀스에만 포함한다.

## 8. Stage03 — 회차 렛저

Stage03은 metadata-derived 자동 파생이 아니다. Stage01·02를 다시 읽고 회차별로 저작한다.

### 8.1 EpisodeArc

회차의 극적 질문, 실제 시퀀스 전환에 따른 act_structure, entry/exit state, 핵심 turning point, 중심 갈등축, 회차 기능을 기록한다.

### 8.2 CharacterArc

단위는 `인물 × 실제 등장 회차`다.

- 단순 등장만으로 만들지 않는다.
- 상태 변화 또는 유의미한 선택이 있어야 한다.
- trigger_scene_no에 해당 인물이 실제 등장해야 한다.
- 같은 사건이라도 각 인물의 state_delta와 evidence는 달라야 한다.

### 8.3 RelationshipArc

단위는 `관계쌍 × 실제 상호작용 회차`다.

- trigger_scene_no에 두 인물이 실제로 함께 등장하거나 직접 통화·교신해야 한다.
- 동일 관계를 A–B와 B–A로 중복 작성하지 않는다.
- 관계의 현재 상태와 이번 회차 변화량을 분리한다.

### 8.4 LocalEdge

동일 회차 안의 실제 인과만 저장한다.

```text
src_episode_no == tgt_episode_no
gap_episodes == 0
edge_type == causal
```

원인 장면이 결과 장면을 구체적으로 발생시켜야 한다. 단순 번호 인접성, 시퀀스 순서, 유사 주제는 인과가 아니다.

### 8.5 PayoffCandidate

후속 회차에서 검증할 장거리 후보를 저장한다.

- plant_payoff
- callback
- subplot_counterpoint
- resolved_here

후속 장면을 아직 읽지 않았다면 CrossEpisodeEdge를 확정하지 않는다.

## 9. 반시즌 통합

전반부 또는 후반부가 끝나면 개별 회차 PASS를 단순 합산하지 않고 하나의 통합 검증기로 전수 검사한다.

- 전체 SourceLock 장면 수와 Stage01 수 일치
- 모든 heading/hash 대응
- 회차별 Stage02 partition
- 회차별 runtime_share 합계
- 전체 ID 고유성
- CharacterArc·RelationshipArc trigger 참여자
- LocalEdge target CORE
- PayoffCandidate 참조
- QuarterAudit 전수 존재
- 반복 골격·placeholder·Python 의미 생성 흔적

통합 게이트가 실패하면 원인이 있는 회차로 돌아가 수정하고 다시 전체를 검사한다.

## 10. Stage04 — 전 시즌 fan-in

Stage04는 전 회차 Stage01~03이 잠긴 뒤에만 진행한다.

```text
모든 PayoffCandidate 전수 검토
→ 후속 실제 장면 확인
→ source와 target 의미 대조
→ 승격 / 재분류 / 회차 내 해소 / 중복 / 기각
→ disposition ledger 기록
→ 확정된 연결만 CrossEpisodeEdge 생성
```

### 허용 CrossEpisodeEdge

- callback
- plant_payoff
- subplot_counterpoint

장거리 causal을 별도 허용해야 하는 프로젝트라면 validator 계약을 먼저 버전업해야 한다. 현재 기본 규칙에서는 회차 간 일반 인과를 자동 브리지로 만들지 않는다.

### 금지

- 이전 화 마지막 장면 → 다음 화 첫 장면 자동 연결
- `gap=1`이라는 이유만으로 local edge 생성
- 동일 설명을 여러 후보에 복사
- source/target 장면을 직접 확인하지 않은 승격

## 11. FullSeriesArc

Stage04와 함께 작품 전체를 다시 종합한다.

- logline
- central dramatic question
- theme statement
- protagonist 구조와 시즌 arc
- antagonist 구조
- 실제 movement 기반 season_structure
- macro turning points
- resolution
- open ending 여부
- tone
- 남는 갈등
- 전체 core distribution

회차 번호를 기계적으로 4분기화하지 않는다. 실제 시퀀스·인물·복선의 매크로 전환에 맞춰 movement를 구성한다.

## 12. Python 경계

### 허용

- ZIP 해제와 인코딩 복구
- scene marker 탐지
- 장면 ordinal 생성
- 해시 계산
- Q 범위 산정
- JSON/JSONL 직렬화
- 스키마·타입·coverage 검사
- 참조·ID·중복 검사
- 반복 골격·placeholder 탐지
- manifest·SHA256·ZIP 생성
- 실제 validator 실행

### 금지

- title·intent_gist 생성
- CORE 의미 판정
- Sequence goal·obstacle·value_shift 생성
- EpisodeArc·CharacterArc·RelationshipArc 생성
- LocalEdge note 또는 PayoffCandidate 생성
- CrossEpisodeEdge 승격 판단
- FullSeriesArc 의미 생성

다음과 같은 함수 또는 동등 기능이 나타나면 즉시 실패로 본다.

```text
make_card
keywords
theme
auto_forward_hook
derive_information_delta
generate_character_arc
generate_payoff
```

Python 파일이 패키지에 있다는 사실만으로 실패하는 것은 아니다. 의미 생성 함수가 있는지, 실행 경로가 의미 필드를 작성했는지가 핵심이다. 배포 패키지는 휴대형 validator만 포함하는 것이 바람직하다.

## 13. 중단·세션 한도 방지

### 과거 실패 원인

- 내부 회차 체크포인트를 사용자 제출 완료로 오인
- 범위가 커지자 직접독해보다 ZIP 완성을 우선
- 회차별 서로 다른 약한 validator 사용
- 사후 검증으로 오염이 여러 회차에 확산

### 예방 규칙

1. 사용자와 약속한 제출 범위를 handoff와 SourceLock에 명시한다.
2. 내부 회차 PASS에서는 최종 보고를 하지 않는다.
3. 모든 회차가 동일한 quarter/episode gate를 사용한다.
4. 반시즌 종료 시 하나의 통합 validator로 역감사한다.
5. 작업 중단 시 마지막 `LOCKED_PASS`와 `next`를 저장한다.
6. 새 세션은 PASS JSON이 아니라 실제 파일과 validator를 다시 읽는다.

## 14. 패키지 구조

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
  evidence/
  authoring_ledgers/
  provenance/
  lineage/
  validation/
  reports/
  FINAL_MANIFEST.json
  SHA256SUMS.txt
```

작품과 단계에 따라 일부 보조 폴더는 생략할 수 있으나, 핵심 계층과 실제 validator·SHA manifest는 필수다.

## 15. 최소 개발자 보고

```text
작품: <work>
범위: EP01~EPXX / Stage01~04
SceneCard / Sequence / Character / Relationship / Local / Payoff / Cross 수량
판정: PASS_CANDIDATE...
errors: 0 / warnings: 0
ZIP SHA256
다음: <next>
```

세부 보강 내역은 report와 ledger에 저장한다.

## 16. 새 세션 재개 문장

새 대화창에서는 다음 지시로 즉시 재개할 수 있다.

```text
개발자 허브의 docs/drama_analysis/README.md와 연결된 v2 문서를 전부 읽어라.
WORK_STATUS에서 완료 작품을 제외하고 한국드라마04의 다음 작품 1편을 선정하라.
SourceLock v2와 반시즌 계획을 만든 뒤 EP01 Q1부터 직접독해를 시작하라.
내부 회차 체크포인트에서 멈추거나 완료 보고하지 말고 약속된 반시즌 범위를 완성하라.
```
