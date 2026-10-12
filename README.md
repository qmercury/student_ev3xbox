# EV3 Xbox · 학생용 프로젝트

이 저장소는 **학생이 자신의 LEGO EV3(ev3dev / Python 3.5.3)** 로봇 프로그램을 작성하고 VSCode에서 배포하기 위한 공간입니다.

학생은 **`main.py`에 자신의 주행·슈터·센서 알고리즘을 직접 구현**합니다. 완성된 로봇축구 알고리즘을 제공하지 않습니다. Xbox 입력은 교사용 Relay와 EV3의 `xbox_service.py`가 전달하며, 학생은 `from ev3xbox import XboxController, XboxButton`만 사용합니다.

## 사용 순서

1. 이 저장소를 VSCode로 엽니다.
2. `.vscode/ev3-target.example.json`을 `.vscode/ev3-target.json`으로 복사하고 자기 EV3의 `robot_id`와 예비 `host`를 설정합니다. 이 파일은 Git에 업로드하지 않습니다.
3. 최초 1회 `EV3: 최초 연결 설정` 작업으로 SSH 키를 등록합니다. 교사가 EV3의 Xbox 서비스를 설치한 상태여야 합니다.
4. `main.py`를 작성하고 `EV3: 업로드 및 실행` (Ctrl+Shift+B)을 실행합니다.
   - EV3 LCD에 `STARTING` → `RUNNING`이 표시됩니다. 종료 시 `STOPPED`, 예외 발생 시 `ERROR`가 표시됩니다.
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

## EV3 본체 실행 상태 화면

업로드 도구는 `ev3/student_runner.py`를 EV3에 복사하여 `main.py`와 같은 Python 프로세스에서 실행합니다. 학생은 `main.py`에 상태 화면 코드를 작성할 필요가 없습니다.

- `STARTING`: Python 코드 실행 시작 중
- `RUNNING`: Python 코드가 실행 중이라는 표시 (Xbox 연결/모터 준비 완료를 보장하지 않음)
  - LCD 해상도(178×128)에 맞는 **큰 글꼴**로 표시하고, 실행 중 화면이 다른 프로그램에 의해 덮여도 약 **0.6초 간격으로 복원**합니다.
- `STOPPED`: 정상 종료 또는 `EV3: 정지`로 종료
- `ERROR`: 처리되지 않은 Python 오류로 종료

학생이 LCD를 직접 사용하는 프로젝트라면 개인 설정 `.vscode/ev3-target.json`에 `"lcd_status": false`를 설정하면 자동 화면 표시만 비활성화됩니다. 자동 표시를 끄더라도 업로드/실행/종료 및 로그는 그대로 작동합니다. EV3의 기본 화면 관리 프로그램이 LCD를 다시 그리거나 접근 권한이 제한된 경우에는 상태 화면이 보이지 않을 수 있으며, 이때 학생 코드는 계속 실행됩니다.
