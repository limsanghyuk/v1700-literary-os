# 드라마 분석 결과 요약·아티팩트 정책

Updated: 2026-07-13  
Status: **AUTHORITATIVE RESULT INDEX**

이 디렉터리는 Stage01~04 최종 결과의 상위 종합과 검증 가능한 패키지 식별 정보를 보존한다.

## 현재 권위 자료

- 상위 `WORK_CATALOG_2026-07-12.md`
- 상위 `WORK_STATUS_2026-07-12.json`
- 상위 `CURRENT_AUTHORITY_SNAPSHOT_2026-07-13.md`
- `AUTHORITATIVE_7_WORK_RESULT_INDEX_2026-07-13.md`
- 작품별 최종 ZIP 파일명·SHA256·레코드 수·validation 결정

`FULL_SERIES_SYNTHESIS_5_WORKS_2026-07-12.md`는 최초 5작품의 의미 종합을 보존한 **historical subset**이다. 현재 작품 수·패키지·다음 진입점의 권위 자료로 사용하지 않는다.

## authoritative v3 패키지

```text
p101_stage01_04_authoritative_final_v3.zip
kmn_stage01_04_authoritative_final_v3.zip
princess_stage01_04_authoritative_final_v3.zip
cityhunter_stage01_04_authoritative_final_v3.zip
gumiho_stage01_04_authoritative_final_v3.zip
goodperson_stage01_04_authoritative_final_v3.zip
paradise_stage01_04_authoritative_final_v3.zip
```

정확한 SHA256은 `WORK_CATALOG_2026-07-12.md`와 `WORK_STATUS_2026-07-12.json`을 따른다.

## 누적 상태

```text
7작품
115회
7,518 SceneCard
1,043 SequenceBlueprint
115 EpisodeArc
787 CharacterArc
757 RelationshipArc
1,634 LocalEdge
580 PayoffCandidate
301 CrossEpisodeEdge
460 QuarterAudit
7 FullSeriesArc
```

## 대용량 패키지 정책

장면별 JSONL 전체와 validator를 포함한 최종 ZIP은 대화 세션 또는 별도 artifact storage로 전달하며 문서 저장소에 binary를 중복 커밋하지 않는다. 파일명이 같아도 SHA가 다르면 동일 아티팩트로 취급하지 않는다.

## 재수용 절차

```text
package receive
→ catalog SHA256 match
→ ZIP CRC
→ fresh extraction
→ SHA256SUMS verify
→ real validator rerun
→ record count recalc
→ lineage/supersession check
→ PASS_CANDIDATE ingestion
```

## 분석 재사용

상위 synthesis나 카탈로그만으로 SceneCard·CharacterArc·Edge를 대체하지 않는다. 창작·검색·평가에서 특정 근거를 사용할 때는 원 패키지의 장면·시퀀스·엣지로 내려가 확인한다.
