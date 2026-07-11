# 드라마 분석 검증·배포 프로토콜 v2

Document ID: GPT-DRAMA-VALIDATION-RELEASE-V2  
Status: AUTHORITATIVE  
Updated: 2026-07-12

## 1. 검증 철학

분석 품질을 하나의 평균 점수로 합치지 않는다.

```text
A축: Source Fidelity — 원본에 실제로 근거하는가
B축: Structural Integrity — 스키마·참조·불변식이 맞는가
C축: Functional Utility — 검색·그래프·창작 지원에 실제 유용한가
```

A/B/C는 각각 독립 판정한다. A가 실패했는데 B와 C 평균으로 PASS시킬 수 없다.

## 2. 권위 순서

```text
실제 데이터
> 실행형 validator 결과
> SHA/CRC/참조 감사
> 사람이 작성한 보고서
> 이전 PASS 선언
```

보고서와 validator가 모순되면 FAIL이다.

## 3. Gate 0 — Source Intake

Stage01 시작 전 검사:

- 전체 회차 파일 존재
- 인코딩 복원 가능
- 회차 파일 SHA256
- scene boundary 정책 재현 가능
- canonical ordinal 연속
- source marker 중복·결번·역순 기록
- 회차별 scene count
- 전반부·후반부 장면 수
- raw script 비배포 정책

판정:

```text
SOURCE_LOCKED_READY_FOR_EP01_Q1
```

실패 시 분석 시작 금지.

## 4. Quarter Gate

각 Q가 다음 Q로 넘어가기 위한 조건:

```json
{
  "scene_coverage": "PASS",
  "source_hash_match": true,
  "exact_9_key_schema": true,
  "invalid_core_count": 0,
  "placeholder_count": 0,
  "duplicate_title_count": 0,
  "duplicate_intent_count": 0,
  "visible_reference_template_hits": 0,
  "keyword_artifact_hits": 0,
  "python_semantic_generation": false,
  "direct_reading_completed": true,
  "decision": "LOCKED_PASS"
}
```

중복 검사에서 제목·intent의 정당한 반복이 확인되면 별도 ledger로 예외를 설명할 수 있으나, 기본값은 0이다.

## 5. Episode Gate

Q1~Q4 완료 후 회차 전체를 검사한다.

### Stage01

- 장면 수 일치
- scene_no 1..N
- SourceLock heading/hash 대응
- 정확한 9키
- CORE16
- title/intent 완전 중복 0

### Stage02

- 정확한 18키
- seq_id·work_id·episode_no·seq_index
- I-COVER/I-PARTITION/I-COUNT
- scene_span·scene_budget
- value_shift `from/to`
- turn_type registry
- turn_class 파생
- core_mix 장면 근거
- runtime_share 합계 1.0
- density >= 0.11

### Stage03

- EpisodeArc 13키
- act sequence tiling
- structured turning_point
- CharacterArc trigger 인물 등장
- RelationshipArc 양쪽 인물 등장
- LocalEdge 동일 회차·gap0·target CORE
- PayoffCandidate 참조·enum

판정 예:

```text
PASS_CANDIDATE_EP07
```

내부 회차 PASS는 사용자 제출 완료가 아니다.

## 6. Half-Season Gate

전반부 또는 후반부 전체를 하나의 validator로 다시 검사한다.

필수:

- 회차 파일 전수 존재
- 합계 scene count == SourceLock half count
- 장면 heading/hash 전수 대응
- 회차별 Stage02 불변식
- ID 전역 고유성
- Character/Relationship trigger 전수
- LocalEdge 전수
- QuarterAudit 전수
- repeated skeleton 전수
- package path와 report 범위 일치

개별 회차 validator가 서로 다른 규칙을 사용해서는 안 된다. 통합 gate가 개별 PASS보다 우선한다.

## 7. Full-Series Gate

전·후반부와 Stage04를 결합한 뒤 검사한다.

### 전체 수량

- episodes_total
- scenes_total
- sequences_total
- EpisodeArc count
- CharacterArc count
- RelationshipArc count
- LocalEdge count
- PayoffCandidate count
- CrossEpisodeEdge count
- candidate disposition count

### Stage04

- 모든 PayoffCandidate가 disposition됨
- 미처리 후보 0
- promoted edge와 CrossEpisodeEdge 1:1 대응
- source/target episode·scene 실재
- target episode > source episode
- gap 산술
- edge_type 허용 enum
- target label 실제 CORE
- 중복 edge 없음
- 자동 인접 회차 bridge 없음

### FullSeriesArc

- 정확한 17키
- 실제 count 일치
- movement span 합리성
- macro turning point 참조
- series_core_dist 실제 합계

판정:

```text
PASS_CANDIDATE_FULL_SERIES_STAGE01_04
```

## 8. 반게이밍 검사

형식 검증과 같은 수준으로 강제한다.

### 8.1 미치환 변수

검출 예:

```text
{char}
{topic}
${scene}
TBD
TODO
metadata-derived
```

의미 필드에 한 건이라도 있으면 FAIL.

### 8.2 visible reference residue

```text
[EP07-S01: ...]
scene=17 / ref=...
```

분석문 내부에 생성용 참조가 남으면 FAIL.

### 8.3 keyword artifact

```text
물고기·마리가·넓은
아버지, 일어나, 발이, 이게
```

원문 단어 조각을 문장 대신 넣은 흔적은 FAIL.

### 8.4 field copy

- title이 intent에 그대로 삽입
- scene_action이 information/decision/function에 반복
- CharacterArc evidence가 여러 인물에 동일
- RelationshipArc evidence가 여러 관계쌍에 동일

### 8.5 skeleton repeat

CORE·인물명·장소명 등을 마스킹한 뒤 동일 골격을 센다. 한 고정 골격이 전체의 15%를 넘으면 기본 FAIL. 회차 규모가 작아 통계가 왜곡되면 사람 감사와 예외 ledger가 필요하다.

### 8.6 mechanical phase map

모든 인물·관계가 동일한 setup/expansion/reversal/closure 회차 구간을 공유하면 자동 파생 의심으로 FAIL.

### 8.7 Python authoring trace

다음 기능을 수행하는 코드 또는 로그가 있으면 FAIL.

```text
keywords → theme → make_card
metadata → character arc generation
sequence successor → local edge template
last scene → next episode first scene auto bridge
```

## 9. Source Fidelity 감사

구조 PASS만으로 A축을 보장할 수 없다.

샘플이 아니라 가능한 경우 전수 확인:

- heading이 원본 장면과 일치
- intent가 실제 행동·인물·정보를 반영
- trigger scene에 인물 등장
- source/target edge 의미가 실제 인과·회수
- FullSeriesArc turning point가 실제 회차 사건

원문 전문을 배포 패키지에 넣지 않아도 SourceLock hash와 별도 로컬 원본으로 감사 가능해야 한다.

## 10. 실제 validator 규칙

### 금지: stub validator

다음은 validator가 아니다.

```python
report = json.load(open("FINAL_VALIDATION_REPORT.json"))
print(report["decision"])
```

validator는 산출물 파일을 직접 열어 키·타입·참조·불변식을 재계산해야 한다.

### 휴대성

- 절대 경로 금지
- package root 기준 상대 경로
- 별도 환경 변수 없이 실행 가능
- 결과 JSON을 새로 생성
- 실패 시 non-zero exit

권장 실행:

```bash
python validation/verify_final.py
```

## 11. Artifact Integrity

최종 ZIP 생성 후 반드시 별도 디렉터리에 새로 풀어 검사한다.

1. ZIP CRC
2. `SHA256SUMS.txt` 전수
3. 새 경로에서 validator 재실행
4. raw source-like 파일 부재
5. manifest count와 실제 파일 count
6. validator 결과와 README/report 일치

`SHA256SUMS.txt` 자체는 raw source TXT가 아니다. raw 검사에서 manifest를 오인하지 않도록 한다.

## 12. Functional Holdout

그래프 계층의 C축 유용성을 검증한다.

권장 방식:

```text
수동 작성한 질문 task
+ 분리된 answer key
+ baseline retrieval
+ graph-assisted retrieval
+ Recall@5 또는 target evidence hit 비교
```

### 판정 예

```text
PASS_LIMITED_HOLDOUT_NONBLINDED
```

이 판정은 다음 한계를 명시한다.

- 같은 프로젝트에서 task/answer를 작성
- 외부 인간 블라인드 평가 아님
- 작품 수 제한
- 검색기·토크나이저 편향 가능

따라서 holdout PASS를 전체 의미 품질의 독립 보증으로 과장하지 않는다.

## 13. 상태 전이

```text
DRAFT
  ↓ quarter/episode gate
CANDIDATE
  ↓ scope strong gate
PASS_CANDIDATE
  ↓ 사용자 또는 지정 리뷰어 승인
CANONICAL
```

오염 시:

```text
DRAFT/CANDIDATE/PASS_CANDIDATE
  → QUARANTINE
  → repair/re-author
  → 새로운 version
```

교체 시:

```text
old version → SUPERSEDED
new version → PASS_CANDIDATE
```

## 14. Quarantine·Supersession

실패본을 조용히 덮어쓰지 않는다.

보존:

- 실패 validation
- 원인 분석
- source map/hash
- 수정 ledger
- old→new mapping
- 의미 변경 여부

폐기 또는 Stage03 입력 금지:

- 자동 생성 의미 필드
- 허위 PASS report
- 미검증 Stage04
- source mismatch record

## 15. 추가 분석 계층 승인

신규 계층은 다음 절차 없이 전체 코퍼스에 도입하지 않는다.

```text
제안
→ 앵커 1작
→ baseline 대비 ablation
→ 기능·정확도·비용 측정
→ 독립 검증
→ schema version 부여
→ 전체 적용 승인
```

평가 질문:

- 기존 Stage01~04로 표현 불가능한가
- 실제 창작·검색 성능을 높이는가
- 원본 근거를 추적할 수 있는가
- 게이밍을 자동 탐지할 수 있는가
- 재저작 비용이 가치보다 작은가

## 16. 릴리스 체크리스트

```text
[ ] SourceLock PASS
[ ] 모든 quarter LOCKED_PASS
[ ] 모든 episode PASS
[ ] half-season gate PASS
[ ] Stage04 candidate disposition 100%
[ ] full-series gate errors 0
[ ] warnings 0 또는 승인된 warning ledger
[ ] real validator
[ ] ZIP CRC PASS
[ ] SHA256 전수 PASS
[ ] fresh extraction re-run PASS
[ ] raw source 미포함
[ ] Python semantic generation false
[ ] report/validation 일치
[ ] package SHA256 기록
[ ] 상태 PASS_CANDIDATE
[ ] canonical_allowed false until approval
```
