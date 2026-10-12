# EV3 Xbox · 학생용 프로젝트

이 저장소는 **학생이 자신의 LEGO EV3(ev3dev / Python 3.5.3)** 로봇 프로그램을 작성하고 VSCode에서 배포하기 위한 공간입니다.

학생은 **`main.py`에 자신의 주행·슈터·센서 알고리즘을 직접 구현**합니다. 완성된 로봇축구 알고리즘을 제공하지 않습니다. Xbox 입력은 교사용 Relay와 EV3의 `xbox_service.py`가 전달하며, 학생은 `from ev3xbox import XboxController, XboxButton`만 사용합니다.

## 사용 순서

1. 이 저장소를 VSCode로 엽니다.
2. `.vscode/ev3-target.example.json`을 `.vscode/ev3-target.json`으로 복사하고 자기 EV3의 `robot_id`와 예비 `host`를 설정합니다. 이 파일은 Git에 업로드하지 않습니다.
3. 최초 1회 `EV3: 최초 연결 설정` 작업으로 SSH 키를 등록합니다. 교사가 EV3의 Xbox 서비스를 설치한 상태여야 합니다.
4. `main.py`를 작성하고 `EV3: 업로드 및 실행` (Ctrl+Shift+B)을 실행합니다.
5. 문제 발생 시 `EV3: 상태 확인` 또는 `EV3: 로그 보기`를 사용합니다.

`tools/ev3_deploy.py`는 학생 프로그램만 정지/배포하며 Xbox 서비스는 중지하지 않습니다. `ev3/ev3xbox.py`는 배포 시 학생 프로그램 폴더에 함께 복사됩니다.

## 폴더

- `main.py`: 학생이 편집하는 프로그램
- `examples/`: 학생 참고용 예제 및 비동기 구조 (알고리즘 정답 아님)
- `ev3/ev3xbox.py`: EV3의 Xbox 입력 라이브러리
- `tools/ev3_deploy.py`: VSCode 업로드/실행/로그/정지 도구
- `docs/python/`: 학생 수업용 ev3dev2 / Python 참고서
- `typings/`: VSCode 코드 완성 도움말

교사용 프로그램 및 EV3 상주 서비스 설치: [qmercury/relay_ev3xbox](https://github.com/qmercury/relay_ev3xbox).

원본 개발 프로젝트: [qmercury/ev3XboxConnect](https://github.com/qmercury/ev3XboxConnect).
