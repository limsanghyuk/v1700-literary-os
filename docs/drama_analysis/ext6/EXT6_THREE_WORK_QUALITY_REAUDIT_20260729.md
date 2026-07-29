# EXT6 three-work quality reaudit — 2026-07-29

## Verdict

The previous PASS decisions for `공주가돌아왔다`, `공주의남자`, and `구르미그린달빛` are revoked. The 9-, 10-, and 11-work integrated databases are also revoked. The trusted database rolls back to `DB87_EXT6_V1_4_8WORKS_WINDOWS_COMPATIBLE_20260729.zip` (`ae79bcd00e91bd7eb6689474acc27fd325ac2aa614b04aa690cc9724839019c2`).

## Findings

### 공주가돌아왔다
- source-line text mismatch: 0
- severe scene-heading/source mismatch: 22 scenes, 89 CastPresence rows
- entity alias collisions: 4
- PHONE_OR_REMOTE without contextual marker: 102/180
- REFERENCED_ONLY: 0; VOICE_ONLY: 0
- all 2,013 SPEAKING rows mechanically assigned PRIMARY
- verdict: FAIL; rebuild required

### 공주의남자
- source-line text mismatch: 0
- severe scene-heading/source mismatch: 5 scenes, 8 CastPresence rows
- entity alias collisions: 2
- PHONE_OR_REMOTE without contextual marker: 28/74
- REFERENCED_ONLY: 0; VOICE_ONLY: 0
- all 3,164 SPEAKING rows mechanically assigned PRIMARY
- verdict: FAIL; rebuild required

### 구르미그린달빛
- source-line text mismatch: 0
- exact-schema enum violations: 1,090
- severe scene-heading/source mismatch: 79 scenes, 312 CastPresence rows
- duplicate evidence groups: 239; duplicated rows: 592
- duplicate source-interval groups: 67; affected scenes: 155
- entity alias collisions: 15
- false entities include `어둡고` and `셋`
- all 2,097 SPEAKING rows mechanically assigned PRIMARY
- verdict: SEVERE FAIL; full EXT6 rebuild required

## Validation gap

The prior validator confirmed that quoted text existed at the declared source line and that baseline paths were not overwritten. It did not test whether the line belonged to the correct logical scene, whether one line or interval was reused across multiple scenes, whether enum values belonged to the authorized schema, whether aliases mapped to one Entity ID, or whether focality and presence mode were semantically classified.

## New mandatory gates

- exact schema enum gate
- non-overlapping scene intervals
- unique scene attribution for each evidence line
- entity alias uniqueness
- focality independent from speaking status
- presence-mode contextual validation
- REFERENCED_ONLY coverage audit
- anchor parity comparison before integration
