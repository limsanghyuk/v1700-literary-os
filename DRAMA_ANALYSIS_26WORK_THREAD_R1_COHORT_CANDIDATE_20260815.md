# 26작 Thread Continuity R1 전수 적용 Candidate — 2026-08-15

Status: **COHORT_REVIEW_COMPLETE_ID_ONLY_CANDIDATE_NOT_CANONICAL**

## 범위
- current canonical 26작을 전수 검토했다.
- 고신뢰 `thread_id` ID-only 변경: **18작 / 193 plant-payoff entries / 127 aliases**.
- 의미 유사도 자동 병합은 사용하지 않았다.
- `event`, `cast.desire_or_function`, `info_shift`, `plant_payoff.statement`, `scene_notes.functional_propositions`, evidence/source coordinates는 thread repair를 위해 변경하지 않았다.
- 40% multi-episode / 30% R5 coupling은 잠정 진단선이며 hard correctness gate로 사용하지 않았다.

## 적용 방법
1. Stage04 CrossEpisodeEdge의 `plant_payoff`/`callback` 관계를 우선 evidence로 사용했다.
2. 양 끝 장면이 THICK plant/payoff와 고신뢰로 대응하고 같은 장기 극적 실임이 확인되는 경우만 ID를 결속했다.
3. episode-serial ID가 개입된 명백한 연속 실을 1차 결속했다.
4. 양쪽이 semantic ID인 경우에는 원인→결과 또는 단순 주제 관련성을 배제하고 동일 장기 실로 확인되는 경우만 수동 승인했다.
5. 변경 작품의 PlannerInput R5와 Runtime R8을 future-blind 원칙으로 재생성했다.

## 변경 작품
`101번째프로포즈`, `가을동화`, `강남엄마따라잡기`, `건빵선생과별사탕`, `검사프린세스`, `결혼못하는남자`, `경성스캔들`, `구해줘`, `국희`, `굿캐스팅`, `그저바라보다가`, `난폭한로맨스`, `너의목소리가들려`, `뉴하트`, `닥터챔프`, `더킹투하츠`, `도깨비`, `드림`.

## 변경하지 않은 작품
`개와늑대의시간`, `공주가돌아왔다`, `궁`, `내여자친구는구미호`, `내이름은김삼순`, `녹두꽃`, `대물`, `돌아온일지매`.

`돌아온일지매`는 live Hub의 별도 anchor pilot을 유지하며 이 cohort candidate가 덮어쓰지 않는다.

`개와늑대의시간`은 **ID_ONLY_REPAIR_INSUFFICIENT**로 판정한다. 여러 Stage04 장거리 실이 현재 THICK `plant_payoff`와 장면 단위로 깔끔하게 대응하지 않아, 더 진행하려면 ID 병합이 아니라 원문 직접독해 기반 semantic repair가 필요하다.

## 검증
- Semantic Independence V3 strict: **PASS / 26/26 / blocking 0**
- exact/provenance/source: **PASS**
  - THICK records: **3,883**
  - SOURCE refs checked: **68,659**
  - provenance hash checks: **19,415**
  - errors: **0**
- PlannerInput / Runtime R8: **26작 PASS**
- full parse: **PASS**
  - JSON files: **8,694**
  - JSONL files: **14,280**
  - JSONL records: **441,133**
  - parse errors: **0**

## 진단 지표 해석
고신뢰 결속 후에도 Claude의 잠정 `40%/30%`를 전 작품이 넘지는 않는다. 이는 실패 판정의 근거가 아니다. 정확한 두 ID를 하나로 합치면 고유 thread 수와 multi-episode thread 수가 함께 줄어 비율이 소폭 내려갈 수도 있다. R5 Episode N은 N-1까지만 보므로 target episode에서 실제 재등장한 실을 미리 선택해 carry하는 방식으로 coupling 수치를 맞추는 것은 금지한다.

## Authority boundary
이 후보는 현재 canonical 26작 DB에서 파생된 **Thread-R1 전수감사 후보**이며 current canonical authority를 대체하지 않는다. 별도의 `quality-equalized` candidate와도 자동 결합하지 않는다. 두 candidate는 서로 다른 lineage이므로, 실제 payload를 동일 staging에 재구성하고 전체 검증을 다시 통과하기 전에는 합성 승격하지 않는다.
