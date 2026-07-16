# 2026-07-16 드라마 DB 클린 트리·개와늑대의시간 ARC13 보강

- Status: `PASS_CANDIDATE_DEVELOPER_RELEASE`
- Branch: `docs/drama-analysis-authority-v3-20260714`
- Scope: 원본 복원, 디렉터리 정규화, 중복 SourceLock 통합, 불필요 core 파일 외부화, 개와늑대의시간 EpisodeArc 보강, 전체 패키지 검증

## 개발자 아티팩트

```text
seqcard_ko_developer_release_51works_50complete_wolf_arc13_v6.zip
SHA256 678ce8313357319000b30109cd961aaa6309cee5d0f1221bcdb47f7769bf198a
size 48,829,456 bytes
ZIP entries 9,842
```

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 파일명·SHA·수량·검증·lineage·handoff만 기록한다.

## 데이터베이스 상태

```text
works 51
episodes 970
SceneCard 60,875
Stage01~04 complete 50
remaining 1
remaining work 최강칠우
remaining status SOURCE_HOLD_EXPERIMENTAL
```

## 디렉터리 정리

```text
seqcard_ko/       의미 데이터·규격 문서
original_extracted/{작품명}/  작품별 UTF-8 TXT 원본
tools/            실행 검증기
validation/       검증 결과와 휴대형 검증기
source_lock/      seqcard_ko/source_lock 단일 표준 경로
upgrade_audit/    이전 판본·감사·계보
provenance/       원본 압축·변환 이력
```

검증 결과:

```text
core seqcard_ko Python files 0
original_extracted root TXT 0
original work folders 51
source_lock roots 1
quarantine in core false
EXT6/HXT6 preserved true
```

`_quarantine`, 루트 `docs`, 루트 `quarter_audits`, 독립 `source_alignment`, 중복 `source_lock`은 정본 core에서 제거·이동·통합했다. EXT6/HXT6 관련 `_ext6_audit`은 보존한다.

## 개와늑대의시간 EpisodeArc 보강

기존 16회 EpisodeArc는 숫자행 경계만 가진 레거시 형식이었다. 숫자행을 현행 JSON처럼 기계 확장하지 않고, 회차별 원본 TXT·SceneCard·SequenceBlueprint를 대조하여 의미 필드를 직접 저작했다.

```text
episodes 16
scenes 880
sequences 143
EpisodeArc exact ARC13 16/16
legacy numeric remaining in canonical 0
legacy numeric preserved for lineage 16
SourceLock files 16
Python semantic generation false
errors 0
warnings 0
```

정본 경로:

```text
seqcard_ko/authored_arc/개와늑대의시간_01.episodearc.json
...
seqcard_ko/authored_arc/개와늑대의시간_16.episodearc.json
```

계보 보존:

```text
upgrade_audit/개와늑대의시간/episodearc_legacy_numeric/
upgrade_audit/개와늑대의시간/개와늑대의시간_episodearc_arc13_migration_report.json
```

SourceLock:

```text
seqcard_ko/source_lock/개와늑대의시간_SOURCE_LOCK_V3.json
```

## 전체 검증

```text
all JSON parsed 2,808 files
all JSONL parsed 5,893 files
all EpisodeArc JSON parse PASS
all EpisodeArc ARC13 keyset PASS
SHA256 ledger 9,738 files / mismatch 0
ZIP CRC PASS
fresh extraction PASS
portable validator PASS
errors 0 / warnings 0
```

## 방법론 추가

이번 분석에서 검증된 다음 운영 지식을 허브 문서로 추가했다.

```text
docs/drama_analysis/DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md
```

핵심은 정상 자산 재사용, 원본 최종 증거, 장면 6질문 독해, Goal/Obstacle/Turn 시퀀스 판정, Stage03 회차별 수직 처리, 회차 경량·블록 강검증·전 시즌 검증 분리, 장편 토큰 관리, SourceLock 이중 해시, 사후 QuarterAudit 금지, 중단 복구 상태 분리다.

## 권한 상태

- 이번 릴리스는 `PASS_CANDIDATE`다.
- 사용자 명시 승인 없는 CANONICAL 승격은 수행하지 않았다.
- 기존 CANONICAL 14작품은 변경하지 않았다.
