# 수호천사 편입 64작품 전체 DB 개발자 인계

- 상태: `CANONICAL USER-APPROVED / WINDOWS-COMPATIBLE HANDOFF`
- 기준일: `2026-07-18`
- Governance base: `V15 Collaborative Canonical`
- Governance 번호 증가: `false`
- 최신 편입 작품: `수호천사 EP01~16`

## 1. 분석 실행 방식

수호천사는 다음 효율화 절차로 완성했다.

```text
전체 원본·회차 경계 선확정
→ EP01부터 순서대로 직접독해·Stage01~03 직접 저작
→ 중간 블록 ZIP·Fresh Extraction 생략
→ EP01~08 전반부 의미검사·보강 1회
→ 교정 규칙을 EP09~16에 적용
→ 전 시즌 의미검사 1회
→ Stage04
→ 개별 작품 ZIP 1회
→ 전체 DB 증분 편입·호환 ZIP 1회
```

이 전반부 검사는 과거의 약 8회차 반복 강검사와 다르다. 작품당 전체의 약 50% 지점에서 한 번만 실행하며, 후반부 저작 오류를 예방하는 의미 캘리브레이션이다.

## 2. 수호천사 정본

- 회차: 16
- SceneCard: 1,060
- SequenceBlueprint: 127
- EpisodeArc: 16
- CharacterArc: 90
- RelationshipArc: 87
- LocalEdge: 112
- PayoffCandidate: 87
- CandidateDisposition: 87 / 100%
- CrossEpisodeEdge: 24
- FullSeriesArc: 1
- EXT6: disabled

의미 품질:

- EP01~08 half-series semantic audit: `PASS`
- 전반부 reinforcement: `COMPLETE`
- EP01~16 full-series semantic audit: `PASS`
- Stage04: `PASS`
- classification: `CANONICAL_USER_APPROVED`

### 개별 작품 아티팩트

`suho_chunsa_EP01_16_stage01_04_windows_compatible.zip`

SHA256:

```text
dea8dfd70172e8dcf0f8f04b2d65960b71bad4d3784b837948b8cfc30e57dfe4
```

검증:

- ZIP CRC PASS
- system unzip test PASS
- Fresh Extraction PASS
- SHA ledger 153 / missing 0 / mismatch 0
- UTF-8 filename flags 151 / 151
- max internal path 61 chars

## 3. 64작품 전체 DB

- 작품: 64
- 회차: 1,182
- SceneCard: 74,078
- 전 시즌 Stage01~04 완료: 62
- 사용자 승인 정본: 20
- 범위 제한 정본: `풍문으로들었소 EP01~10`
- Source hold: `최강칠우`
- 기존 63작품 의미 파일 변경: 0

### 전체 DB 아티팩트

`seqcard_ko_db_64works_62complete_suho_integrated_windows_compatible.zip`

SHA256:

```text
e8d2ac7e6954a43ba649ad128a9ce6900e446365bb3f7e537d4943405c5e9198
```

패키지 규격:

- archive root: `db64/`
- compression: standard ZIP Deflate
- encryption: none
- split archive: false
- UTF-8 filename flags: 12,512 / 12,512
- max internal path: 162 chars / 204 UTF-8 bytes
- entries: 12,810

최종 검증:

- ZIP CRC PASS
- system `unzip -t` PASS
- Fresh Extraction PASS
- SHA ledger 12,804 / missing 0 / mismatch 0
- encoding validator PASS
- SourceLock validator PASS
- registry validator PASS
- database validator PASS
- release validator PASS

## 4. 이전 63작품 ZIP 해제 실패 진단

문제 파일:

`seqcard_ko_developer_database_63works_61complete_20260718_우리집_integrated.zip`

진단:

- 압축 데이터 CRC 자체는 PASS였다.
- 한글 경로 엔트리 13,029개에서 UTF-8 filename flag가 0개였다.
- 최장 내부 경로는 278자였다.
- 따라서 Windows Explorer 기본 해제기에서 한글 파일명 손상 또는 경로 길이 초과로 해제가 실패할 수 있었다.

수정:

- 실제 Unicode 파일명을 다시 사용
- 모든 비ASCII 이름에 UTF-8 flag 적용
- archive root를 짧은 ASCII `db64/`로 변경
- 최장 경로를 278자에서 162자로 축소
- Deflate·무암호·비분할 ZIP 사용
- 시스템 해제와 전체 Fresh Extraction을 별도로 실행

이전 ZIP은 새 전체 DB ZIP으로 대체한다.

## 5. 개발자 사용 순서

1. ZIP을 해제한다.
2. `db64/FINAL_MANIFEST.json`을 확인한다.
3. `db64/SUHO_CHUNSA_INCREMENTAL_INTEGRATION_REPORT.md`를 읽는다.
4. `db64/validation/works/수호천사/current.json`과 `semantic_quality_current.json`을 확인한다.
5. 필요하면 `python tools/current/validate_release.py --root .`를 실행한다.
6. `SHA256SUMS.txt`를 검증한다.

대용량 ZIP과 원본 대본은 GitHub 저장소에 커밋하지 않는다. 허브에는 아티팩트명·SHA256·counts·lineage·검증 결과만 유지한다.
