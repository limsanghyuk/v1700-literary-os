# Drama Analysis — New Session Bootstrap V9

새 드라마 분석을 시작할 때 과거 세션 전체를 다시 학습하지 않는다. 먼저 live Hub `main`을 읽는다.

## 필독 순서
1. `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`
2. `CURRENT_AUTHORITY_POINTER.json`과 그 authority manifest/schema registry
3. integrated pointer가 지정하는 current overlay
4. `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json`
5. integrated pointer가 지정하는 current method
6. `DRAMA_ANALYSIS_THREAD_CONTINUITY_POLICY_R1_20260815.md`
7. 중단 재개 시 current work_state/checkpoint/guard

정적 ZIP·번들과 live Hub가 다르면 **live Hub가 우선**이다. 다른 GPT/Claude 세션의 최신 승격을 과거 snapshot으로 되돌리지 않는다.

## 의미 저작
원본 대본과 SourceLock이 최상위 의미 권위다. 모델이 원문을 직접 순차 독해하고 의미를 저작한다. Python은 추출·정규화·해시·직렬화·검증·비교·조립·패키징만 수행한다.

Stage01~04는 한 회차 전체가 의미 저작 단위이며 Q1→Q4는 attention checkpoint다. 기존 PASS Stage01~04 작품에 THICK를 추가할 때 SequenceBlueprint는 경계만 사용하고 원문을 다시 읽어 THICK를 독립 저작한다.

## Thread Continuity R1
새 thread_id는 실제 새 PLANT/HOOK에서만 발급한다. 동일 실의 CONTINUE/ESCALATION/CALLBACK/REACTIVATION/REVERSAL/PAYOFF는 기존 ID를 재사용한다. 40%/30%는 diagnostic이며 hard gate가 아니다. 점수를 위한 merge는 금지한다. thread_id가 바뀌면 R5/R8을 재생성한다.

## Block-Atomic V2
- 최대 8회 연속 Block.
- **응답당 고정 Sequence 제한 없음. 3 Sequence hard cap 폐기.**
- Sequence별 atomic checkpoint 필수.
- episode checkpoint, block strong gate 필수.
- late/background writer 금지.

## 현재 snapshot
- Stage01~04 schema authority: V10.1
- THICK: `DB98_THICK_26WORK_QUALITY_THREAD_R1_CANONICAL_AUTHORITY_20260815_V1`
- Planner/Runtime: `DB98_PLANNER_RUNTIME_26WORK_QUALITY_THREAD_R1_PROFILE_V1_1_AUTHORITY_20260815_V1`
- 26 works / 3,883 THICK / 470 R5 / 470 R8 / 29,628 runtime scenes
- Full DB: `DB98_98WORK_STAGE04_26THICK_QUALITY_THREAD_R1_CLEAN_V9_FINAL_20260815.zip`
- DB SHA256: `0c205207bad085f31b002fe6bb06b65123baec578649cc0c337ec6cfb268014f`
