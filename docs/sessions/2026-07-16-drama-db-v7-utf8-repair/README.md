# 2026-07-16 드라마 DB V7 UTF-8 경로·문자열 복구

- Status: `PASS_CANDIDATE_DEVELOPER_RELEASE_V7`
- Branch: `docs/drama-analysis-authority-v3-20260714`
- Supersedes: `seqcard_ko_developer_release_51works_50complete_wolf_arc13_v6.zip`

## 원인

V6 ZIP 생성 과정에서 UTF-8 한글 경로 바이트가 CP437 문자열로 오해석된 채 기록되어, Windows 및 Python ZIP 해제 환경에서 `authored` 파일명이 깨졌다. 분석 데이터가 삭제된 것은 아니었지만 파일명이 훼손돼 일부 파일만 존재하는 것처럼 보였다.

## 복구 아티팩트

```text
artifact: seqcard_ko_developer_release_51works_50complete_utf8_repaired_v7.zip
SHA256: 8a27d901d7122a1d9aebcadde459864adffd56c31553931327652744662e851f
size: 48,488,346 bytes
ZIP entries: 9,743
```

## 전수 검사

```text
works: 51
episodes: 970
SceneCard: 60,875
authored flat files: 1,994
all analysis-layer files: 7,790
analysis files missing vs V6: 0
EpisodeArc files: 970
invalid UTF-8 text files: 0
U+FFFD replacement-character files: 0
mojibake filenames: 0
non-ASCII ZIP paths without UTF-8 flag: 0
JSON/JSONL parse errors: 0
ZIP CRC: PASS
fresh extraction: PASS
SHA256 ledger: 9,742 / mismatch 0
```

V4에서 V5/V6으로 감소한 11개 파일은 분석 데이터가 아니라 build script, dump, temporary validation, cache 파일이었다. V7 분석 계층은 V6과 7,790 대 7,790으로 동일하며, 변경된 분석 파일 3개는 U+FFFD 문자만 안전하게 교정한 SceneCard다.

## 인코딩 정규화

- CP949 원본 TXT 73개를 UTF-8 canonical storage로 변환했다.
- 원본 바이트 SHA는 provenance에 보존하고 canonical UTF-8 SHA를 별도 기록했다.
- SourceLock의 canonical storage binding을 실제 UTF-8 저장본 해시로 재결속했다.
- 안전한 문자열 교정 7건을 수행했다.

## 개발자 확인 경로

```text
seqcard_ko/AUTHORED_WORK_INDEX_V7.json
validation/string_and_authored_completeness_validation_v7.json
validation/analysis_layer_no_deletion_audit_v7.json
provenance/encoding_normalization/encoding_normalization_ledger_v7.json
```

## 권한 상태

- V7은 `PASS_CANDIDATE`다.
- 사용자 명시 승인 없는 CANONICAL 승격은 수행하지 않았다.
- 기존 CANONICAL 14작품은 변경하지 않았다.
