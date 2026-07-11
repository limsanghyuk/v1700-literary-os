# 드라마 분석 결과 요약·아티팩트 정책

이 디렉터리는 Stage01~04 최종 결과의 상위 종합과 검증 가능한 패키지 식별 정보를 보존한다.

## 포함

- `FULL_SERIES_SYNTHESIS_5_WORKS_2026-07-12.md`
- 상위 `WORK_CATALOG_2026-07-12.md`
- 상위 `WORK_STATUS_2026-07-12.json`
- 작품별 최종 ZIP 파일명·SHA256·레코드 수·validation 결정

## 대용량 패키지

장면별 JSONL 전체와 validator를 포함한 최종 ZIP은 대화 세션 산출물로 전달됐으며, 이 문서 PR에는 binary를 중복 커밋하지 않는다. binary를 다시 전달받거나 별도 artifact storage에 적재할 때 SHA256을 기준으로 동일성을 확인한다.

기록된 패키지:

```text
p101_stage01_04_repaired_final_v2(1).zip
kmn_stage01_04_source_repaired_final_v2(1).zip
princess_stage01_04_full_series_repaired_final_v2(1).zip
cityhunter_stage01_04_full_series_final_v1.zip
gumiho_stage01_04_full_series_final_v1.zip
```

## 재수용 절차

```text
package receive
→ SHA256 match
→ ZIP CRC
→ fresh extraction
→ SHA256SUMS verify
→ real validator rerun
→ record count recalc
→ PASS_CANDIDATE ingestion
```

파일명이 같아도 SHA가 다르면 동일 아티팩트로 취급하지 않는다.

## 분석 재사용

상위 synthesis만으로 SceneCard·CharacterArc·Edge를 대체하지 않는다. 창작·검색·평가에서 특정 근거를 사용할 때는 원 패키지의 장면·시퀀스·엣지로 내려가 확인한다.
