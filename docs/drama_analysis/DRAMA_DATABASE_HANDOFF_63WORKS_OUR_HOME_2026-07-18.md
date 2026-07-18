# 「우리집」 편입 63작품 전체 데이터베이스 인계

- Status: `AUTHORITATIVE HANDOFF`
- Date: `2026-07-18`
- Base governance: `SEQCARD_KO_GOVERNANCE_RELEASE_V15_COLLABORATIVE_CANONICAL`
- Governance version incremented: **false**
- Integration mode: `V15_INCREMENTAL_FULL_DATABASE`

## 1. 전체 DB 아티팩트

```text
seqcard_ko_developer_database_63works_61complete_20260718_우리집_integrated.zip
```

- SHA256: `e10fa0fee048ad97a3c6e3cb5f9297399f1d681cfc43f0aaa566620c69cd8706`
- Size: `63,845,629 bytes`
- ZIP entries: `13,029`
- ZIP CRC: `PASS`
- Fresh Extraction: `PASS`
- SHA256 ledger: `12,643 checked / 0 missing / 0 mismatch`

대용량 ZIP은 저장소에 커밋하지 않는다. 전달 채널에서 위 파일명과 SHA256을 대조해 수령한다.

## 2. 외부 최종 검증서

```text
seqcard_ko_63works_61complete_우리집_integrated_final_validation.json
```

- SHA256: `ecdbe2f7b6e5334311529f2b945bb9f1dc99f97cb1afa357fb747d38c78862e7`
- Status: `PASS`

## 3. 전체 DB 집계

| 항목 | 수량 |
|---|---:|
| 작품 | 63 |
| 회차 | 1,166 |
| SceneCard | 73,018 |
| 전 시즌 Stage01~04 완료 | 61 |
| 사용자 승인 정본 | 19 |
| 범위 제한 정본 | 풍문으로들었소 EP01~10 |
| Source hold | 최강칠우 |

## 4. 신규 편입 작품 — 우리집

- Scope: `EP01~EP20 FULL`
- Classification: `CANONICAL_USER_APPROVED`
- Provider: `GPT-5.6 Thinking`
- 원본 직접독해: true
- Python 의미 생성: false
- 전반부 의미검사·보강: `PASS_REINFORCED`
- Stage04: `PASS`

| 계층 | 수량 |
|---|---:|
| SceneCard | 951 |
| SequenceBlueprint | 141 |
| EpisodeArc | 20 |
| CharacterArc | 130 |
| RelationshipArc | 111 |
| LocalEdge | 185 |
| PayoffCandidate | 95 |
| CandidateDisposition | 95 |
| CrossEpisodeEdge | 24 |
| FullSeriesArc | 1 |

CandidateDisposition은 `95/95`, 미처리 후보는 `0`이다.

## 5. 증분 편입 무결성

- 기존 V15 의미 파일 변경: **0**
- 신규 의미 파일: **163**
- 편입 후 의미 파일: **9,394**
- SourceLock registry: `63 works`
- Validation registry: `63 works`
- Encoding validator: `PASS`
- SourceLock validator: `PASS`
- Registry validator: `PASS`
- Database validator: `PASS`
- Release validator: `PASS`

## 6. 개발자 확인 순서

```text
1. FINAL_MANIFEST.json
2. OUR_HOME_INCREMENTAL_INTEGRATION_REPORT.md
3. validation/works/우리집/current.json
4. validation/works/우리집/semantic_quality_current.json
5. seqcard_ko/source_lock/current/우리집.source_lock.v4.json
6. SHA256SUMS.txt
7. python tools/current/validate_release.py --root .
```

## 7. 계보 원칙

이번 패키지는 새 Governance 번호를 만들지 않는다. V15 정본 기반에 「우리집」만 증분 편입한 전체 데이터베이스 스냅샷이다. 작품 추가만으로 릴리즈 번호를 늘리지 않는 현재 운영 정책을 따른다.
