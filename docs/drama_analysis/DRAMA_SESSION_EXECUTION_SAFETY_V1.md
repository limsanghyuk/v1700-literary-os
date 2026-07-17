# 드라마 세션·실행 안전 규칙 v1

- Document ID: `DRAMA-SESSION-EXECUTION-SAFETY-V1`
- Status: `AUTHORITATIVE_CANDIDATE`
- Incident basis: 돌아온 일지매 EP20 실행 중단, 2026-07-14

## 1. 조사 결론

EP20 중단의 주원인은 디스크나 런타임 RAM 부족이 아니다.

조사 시점 환경:

```text
RAM total: 4.0 GiB
RAM available: 약 3.2 GiB
/mnt/data 사용량: 정리 전 약 89 MB, 정리 후 약 80 MB
filesystem 사용률: 약 1%
활성 돌아온일지매 분석 루트: 약 3.4 MB
```

따라서 중단은 다음의 결합으로 판정한다.

```text
긴 단일 응답
+ 다수 회차 직접독해
+ 대량 JSONL 저작·검증·패키징
+ 누적 대화 컨텍스트
+ 회차 영속화 이전 진행 보고
→ 실행/컨텍스트 한도 초과
```

## 2. 세 가지 메모리 구분

### A. 작업공간 저장소

`/mnt/data`의 파일·ZIP·임시 추출물. 직접 정리 가능하다.

### B. 런타임 메모리

Python/container RAM. 현재 사건에서는 부족하지 않았다.

### C. 대화·모델 컨텍스트

긴 대화 기록, 도구 결과, 중간 산출물 설명. 사용자가 말하는 세션 한도의 핵심 위험이다. assistant가 플랫폼의 과거 대화 컨텍스트를 직접 삭제할 수는 없으므로, 권위 문서와 체크포인트로 의존성을 외부화하고 새 실행은 최소 컨텍스트로 재진입해야 한다.

## 3. 작업공간 정리 정책

보존:

- 원본 archive
- 활성 분석 루트
- 최신 검증된 개발자 핸드오프 ZIP/SHA
- 최신 회차/블록 체크포인트
- SourceLock과 correction ledger

삭제 가능:

- ZIP 생성용 중복 staging directory
- 재생성 가능한 scene export
- 동일 범위의 superseded handoff ZIP
- 임시 debug dump
- 검증 완료 후의 중간 조립 디렉터리

삭제 금지:

- 원본
- 유일한 검증본
- lineage 증거
- 실패 원인 보고서
- supersession 관계를 증명하는 checksum

## 4. 트랜잭션 경계

앞으로 한 회차를 하나의 원자 트랜잭션으로 처리한다.

```text
EPxx SourceLock 확인
→ Q1 저작·검증·저장
→ Q2 저작·검증·저장
→ Q3 저작·검증·저장
→ Q4 저작·검증·저장
→ Stage02/03/EXT6 통합
→ 강한 게이트
→ 회차 체크포인트 ZIP
→ SourceLock next 갱신
→ 진행 보고
```

진행 보고는 영속화 후에만 한다.

## 5. 실행 범위 제한

```text
한 실행의 안전 범위 = 1 episode
한 대화 턴의 최대 목표 = 1 episode complete checkpoint
```

2회 이상을 계획할 수는 있지만, 한 실행에서 연속 저작하지 않는다. Stage04도 전체 시즌 독해와 후보 원장이 준비된 별도 실행에서 수행한다.

## 6. 중단 복구 규칙

중단 후 다음을 검사한다.

1. SourceLock.current_completed_episodes
2. SourceLock.next
3. 해당 회차의 QuarterAudit 4건
4. Stage01~03/EXT6 필수 파일 존재
5. validation PASS
6. checkpoint checksum

대화에서 “분석했다”는 진행 문장이 있어도 파일·검증·체크포인트가 없으면 미완료로 판정한다.

## 7. 컨텍스트 경량화

각 재시작 시 필요한 정보만 로드한다.

```text
- 권위 인덱스와 exact schema
- 직전 SourceLock
- 직전 회차 checkpoint manifest
- 현재 회차 원본
- 작품 EntityBridge
- 작품 누적 PayoffCandidate index
```

이전 회차의 전체 원문·전체 대화·전체 로그를 매번 컨텍스트에 재주입하지 않는다.

## 8. 자동화 전환 방지

세션 한도를 피한다는 이유로 의미 저작을 Python/템플릿에 넘기지 않는다. 범위를 줄이고 실행을 나눈다.

```text
허용: 저장·검증·재계산·패키징 자동화
금지: 장면 의미·시퀀스 의미·인물/관계/인과 의미 자동 생성
```

## 9. 중단 판정 enum

```text
INTERRUPTED_BEFORE_PERSISTENCE
PARTIAL_QUARTER_UNVERIFIED
EPISODE_FILES_PRESENT_VALIDATION_PENDING
EPISODE_CHECKPOINT_LOCKED
SAFE_TO_ADVANCE
```

EP20 사건은 `INTERRUPTED_BEFORE_PERSISTENCE`로 판정한다.
