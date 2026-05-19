# V1700 Stage130 제안서 — MultiWork Release

## 1. 제안명

```text
V1700 Stage130 — MultiWork Release
```

## 2. 문제 정의

Stage127~129에서 MultiWork를 안전하게 흡수하기 위한 선행 계층은 구현되었다. 그러나 아직 이 세 계층은 하나의 공식 MultiWork release authority로 봉인되지 않았다. Stage130의 역할은 Stage127 preflight, Stage128 read-only absorption, Stage129 CIM/canon governor를 하나의 clean release로 결합하는 것이다.

## 3. 핵심 판단

MultiWork release는 기능 확장이 아니라 권한 봉인이다. Stage130은 다중 작품 운영 계층을 “안전하게 켤 수 있는 범위”만 열고, 쓰기·원고 공유·자동 canon resolution·Gate26 hard block은 다음 단계 이후로 미룬다.

## 4. 성공 기준

- Stage127~129 evidence가 모두 보존된다.
- MultiWork release matrix가 pass한다.
- read-only shared adapters가 유지된다.
- cross-project write가 차단된다.
- raw manuscript leakage가 0이다.
- canon auto-resolution이 0이다.
- provider-zero와 Node2 boundary가 유지된다.
- repo doctor와 main release gate가 Stage130을 인식한다.
- ZIP 내부 FILELIST/SHA256SUMS가 포함된다.

## 5. 개발자 실행 명령

```bash
python -m compileall src tools
python -m pip install -e .
python -m v1700.cli --help
python tools/run_stage130_multiwork_release.py
python tools/run_stage130_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest -q tests/test_stage127_multiwork_preflight.py tests/test_stage128_read_only_absorption.py tests/test_stage129_multiwork_cim_governor.py tests/test_stage130_multiwork_release.py
```
