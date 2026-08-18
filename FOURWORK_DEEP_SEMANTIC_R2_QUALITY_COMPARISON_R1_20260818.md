# 4작 Deep Semantic R2 품질 비교 및 편입 판정

## 판정

**PASS — 현재 38작 정본에 선택 편입 가능.**

### 구조 불변성

- 대상 4작 Stage01~04 파일: 492개 검사 / mismatch 0
- Boundary: 38/38 PASS, Stage02=6357, THICK=6357, membership mismatch=0, seq_id alias diagnostic=137
- 비대상 34작 THICK/R5/R8/EpisodePlan: 2624개 파일 비교 / mismatch 0

### 대상 4작 품질

| 작품 | THICK | SOURCE refs | hash | depth old → R2 |
|---|---:|---:|---:|---:|
| 개인의취향 | 218 | 2363 | 1090 | 0.9599 → 0.9599 |
| 수호천사 | 126 | 1902 | 630 | 0.7874 → 0.8333 |
| 미안하다사랑한다 | 226 | 3135 | 1130 | 0.8029 → 0.8252 |
| 미생 | 217 | 2266 | 1085 | 0.8329 → 0.8233 |

### 전역 게이트

- `exact_38work.json`: **PASS**
- `semantic_v3_38work.json`: **PASS**
- `owner_38work.json`: **PASS**
- `depth_38work.json`: **PASS**
- `thread_38work.json`: **PASS**
- `subplot_38work.json`: **PASS**
- `planner_runtime_38work.json`: **PASS**
- `artifact_hash_38work.json`: **PASS**
- `deep_semantic_38work.json`: **PASS**
- `stage01_04_equalization.json`: **PASS**

### EpisodeSynopsisPlan

- v0.3-r1 schema: 714/714 / errors 0
- 전수 self-check에서 `미안하다사랑한다 EP16`의 inherited debt 1건 누락을 발견해 SOURCE-grounded final coda를 기준으로 `MISA_MUHYEOK_MINJU_REVENGE_SEDUCTION`를 `paid`로 결산했다.
- repair 후 self-check: **HARD 0**. REVIEW/WARN은 corpus prior 진단으로 비차단.

### 편입 범위

- Stage01~04: 변경하지 않음.
- 대상 4작 THICK semantic prose: R2로 교체.
- 대상 4작 EpisodePlan: R2 semantic delta를 v0.3-r1에 무손실 이식.
- 대상 4작 R5/R8: R2 THICK에서 재생성된 판본으로 교체.
- 다른 세션의 39THICK 권위/CT-13 상태는 가져오지 않음.
- 현재 CT-13 formal verdict `UNDECLARED`와 autonomous-control `EXPERIMENTAL_HOLD`를 유지.
