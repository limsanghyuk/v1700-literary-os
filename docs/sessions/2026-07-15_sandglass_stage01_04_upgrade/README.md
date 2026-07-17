# 모래시계 Stage01~04 업그레이드 핸드오프

- Date: 2026-07-15
- Status: `CANONICAL_STAGE01_04`
- EXT6: not applied
- Raw source committed to hub: no

## 결과

```text
Episodes: 24
SceneCard: 1,365
EpisodeMeta: 24
SequenceBlueprint: 217
EpisodeArc: 24
CharacterArc: 118
RelationshipArc: 94
LocalEdge: 48
PayoffCandidate: 24
CrossEpisodeEdge: 23
CandidateDisposition: 24
FullSeriesArc: 1
```

## 방법 적용

- 기존 Stage01과 고유 Stage02 의미는 보존하고 exact contract로 정규화했다.
- 회차별 실제 변화가 있는 주연·조연·조직 관계를 폭넓게 CharacterArc·RelationshipArc로 추적했다.
- LocalEdge는 같은 회차·gap 0·구체 인과만 선별해 회차당 3건 이하로 유지했다.
- PayoffCandidate 24건을 전수 처분했고 23건만 CrossEpisodeEdge로 승격했다.
- 이전 화 마지막 장면에서 다음 화 첫 장면으로 가는 자동 브리지는 0건이다.
- Python은 직렬화·결정론적 정규화·검증·패키징에만 사용했다.

## 검증

```text
strong validation: errors 0 / warnings 0
candidate disposition: 24 / 24
automatic episode boundary bridge: 0
ZIP CRC: PASS
internal SHA256: PASS
fresh extraction: PASS
portable validator rerun: PASS
```

## 산출물

독립 작품 패키지:

```text
모래시계_stage01_04_upgraded_full_series_v1.zip
SHA256 1a27669d051f8cbd2c54dd222178ae9db35229912ea091a8493fa8487091a2ca
internal files 229
```

통합 데이터베이스:

```text
seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_theking_newheart_killme_whitetower_mawang_skycastle_gung_kain_sign_sandglass_v1.zip
SHA256 f79e1962348216197ccf9687a5881c99621f42ad0693ccfc6ad580aba69c521e
internal files 8,151
```

## 누적 상태

```text
works: 49
episodes: 938
SceneCard: 58,945
Stage01~04 complete: 44
remaining: 5
CANONICAL promoted works: 14
```

남은 작품:

```text
공주의남자
녹두꽃
역전의여왕
최강칠우 — SOURCE_HOLD, 실제 EP03 필요
대장금 — 마지막 순서, 8회차 블록
```

## 다음 진입점

`공주의남자` 또는 `녹두꽃` 중 원본·기존 Stage01/02 preflight가 더 안정적인 작품을 우선한다. `역전의여왕`은 Stage02 재저작을 회차 블록으로 계획하고, `대장금`은 마지막에 수행한다.
