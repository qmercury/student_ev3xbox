# EV3 Xbox · 학생용 프로젝트

**문서 목록:** [docs/README.md](docs/README.md) · **전체 개발 현황:** [원본 로드맵](https://github.com/qmercury/ev3XboxConnect/blob/main/docs/NEXT_STEPS.md)

이 저장소는 **학생이 자신의 LEGO EV3(ev3dev / Python 3.5.3)** 로봇 프로그램을 작성하고 VSCode에서 배포하기 위한 공간입니다.

학생은 **`main.py`에 자신의 주행·슈터·센서 알고리즘을 직접 구현**합니다. 완성된 로봇축구 알고리즘을 제공하지 않습니다. Xbox 입력은 교사용 Relay와 EV3의 `xbox_service.py`가 전달하며, 학생은 `from ev3xbox import XboxController, XboxButton`만 사용합니다.

## 처음 다운로드: 터미널에서 GitHub 저장소 복제하기

**한 번만** `git clone`을 실행하면 됩니다. 같은 노트북에서 이미 저장소를 받았다면 다시 복제하지 말고 아래 **업데이트** 명령을 사용하세요. `git clone`은 GitHub 소스 파일을 노트북에 복사하는 명령이며, EV3에 프로그램을 업로드하는 명령은 아닙니다.

**사전 준비:** [Git](https://git-scm.com/downloads), [VSCode](https://code.visualstudio.com/), 노트북용 Python 3가 필요합니다. Windows는 PowerShell, Mac은 터미널(zsh)을 사용합니다. 처음 내려받을 때는 인터넷에 연결되어 있어야 합니다.

### Mac 터미널 — 아래 블록 전체를 복사해서 붙여넣기

```bash
mkdir -p ~/Documents/EV3_Projects
cd ~/Documents/EV3_Projects
git clone https://github.com/qmercury/student_ev3xbox.git
cd student_ev3xbox
cp .vscode/ev3-target.example.json .vscode/ev3-target.json
```

- `mkdir -p`: 문서 폴더 안에 프로젝트 저장 장소를 만듭니다.
- `cd`: 작업할 폴더로 이동합니다.
- `git clone`: 학생용 GitHub 저장소를 다운로드합니다.
- `cp`: 학생 개인용 EV3 연결 설정을 예제에서 복사해 만듭니다.

### Windows PowerShell — 아래 블록 전체를 복사해서 붙여넣기

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\Documents\EV3_Projects" | Out-Null
Set-Location "$HOME\Documents\EV3_Projects"
git clone https://github.com/qmercury/student_ev3xbox.git
Set-Location .\student_ev3xbox
Copy-Item .\.vscode\ev3-target.example.json .\.vscode\ev3-target.json
```

- `New-Item`: 프로젝트 폴더를 만듭니다.
- `Set-Location`: 해당 폴더로 이동합니다.
- `git clone`: 학생용 GitHub 저장소를 다운로드합니다.
- `Copy-Item`: 학생 개인용 EV3 연결 설정을 복사해 만듭니다.

**복제 후 VSCode로 열기:** 터미널에서 이 저장소 폴더 안에 있는 상태로 `code .`를 실행하거나, VSCode의 **파일 → 폴더 열기**에서 `student_ev3xbox` 폴더를 선택합니다. `code` 명령을 인식하지 못하면 GUI에서 폴더를 열면 됩니다. Mac에서는 VSCode 명령 팔레트의 **Shell Command: Install 'code' command in PATH**를 사용할 수도 있습니다.

**처음 사용할 때:** `.vscode/ev3-target.json`에서 자기 EV3의 `robot_id`와 `host`를 확인하고, VSCode의 **터미널 → 작업 실행 → EV3: 최초 연결 설정**을 한 번 실행합니다. 이후 `main.py`를 작성하고 **EV3: 업로드 및 실행**(기본 빌드 작업)을 사용합니다. 학생 연결 설정 파일은 GitHub로 업로드되지 않습니다.

### 이미 복제했다면: 최신 코드 업데이트

이미 복제한 `student_ev3xbox` 폴더에서 아래 명령 **한 줄만** 실행합니다. `git clone`을 다시 실행할 필요가 없습니다.

```bash
git pull --ff-only
```

`git pull`은 GitHub의 새 코드를 가져오며, 개인용 `.vscode/ev3-target.json`은 Git 관리 대상이 아니므로 기본적으로 유지됩니다. 학생이 `main.py`를 직접 수정한 상태라면 충돌을 피하기 위해 중요한 코드를 먼저 보관하세요. 폴더가 이미 존재한다는 오류가 나면 중복 복제를 하지 말고 기존 폴더에서 작업합니다.

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
  - LCD 해상도(178×128)에 맞는 **큰 글꼴**로 표시합니다. `brickrun`이 실행 중 기본 메뉴 대신 학생 프로그램의 화면을 유지하며, 상태 변경 시에만 새로 그립니다.
- `STOPPED`: 정상 종료 또는 `EV3: 정지`로 종료
- `ERROR`: 처리되지 않은 Python 오류로 종료

학생이 LCD를 직접 사용하는 프로젝트라면 개인 설정 `.vscode/ev3-target.json`에 `"lcd_status": false`를 설정하면 자동 화면 표시만 비활성화됩니다. 자동 표시를 끄더라도 업로드/실행/종료 및 로그는 그대로 작동합니다. EV3의 기본 화면 관리 프로그램이 LCD를 다시 그리거나 접근 권한이 제한된 경우에는 상태 화면이 보이지 않을 수 있으며, 이때 학생 코드는 계속 실행됩니다.

### 학생별 LCD 문구와 LED 설정

각 학생은 **.vscode/ev3-target.json**을 직접 편집할 수 있습니다. 이 파일은 Git에 올라가지 않습니다. 기존 Robot ID, host, SSH 정보는 그대로 두고 아래 항목을 추가하거나 수정하세요.

```json
{
  "lcd_status": true,
  "lcd_title": "ROBOT SOCCER",
  "lcd_program": "EV3-01",
  "lcd_starting_text": "STARTING",
  "lcd_running_text": "PLAYING",
  "lcd_stopped_text": "STOPPED",
  "lcd_error_text": "ERROR",
  "led_color": "ORANGE",
  "led_effect": "BLINK"
}
```

위 JSON은 **변경 가능한 부분만 보여주는 예시**이므로, 기존 파일 전체를 덮어쓰지 마세요. 마지막 항목 앞뒤의 쉼표에 주의하세요.

- `lcd_title`: 상단 제목(최대 16자)
- `lcd_program`: 하단 로봇/파일 이름(최대 18자)
- `lcd_*_text`: 시작/실행/종료/오류 상태 화면의 중앙 문구(각 최대 10자)
- 화면 글자는 기본 EV3 비트맵 폰트 제약으로 **영문·숫자·기호(ASCII)만** 지원합니다.
- `led_color`: `DEFAULT`, `RED`, `GREEN`, `AMBER`, `ORANGE`, `YELLOW`
- `led_effect`: `DEFAULT`(기존 brickrun 녹색 점멸), `BLINK`(약 0.5초 간격 점멸), `SOLID`(계속 켜짐), `OFF`(꺼짐)
- `led_color`만 사용자 색상으로 지정하면 깜박임(`BLINK`)이 기본입니다. `led_effect`만 변경하면 녹색이 기본입니다.
- `led_color`와 `led_effect`가 모두 `DEFAULT`이면 **기존 brickrun 녹색 깜박임**을 유지합니다. LED 설정은 실행 중에만 적용되며, 종료 시 brickrun이 기본 LED 상태를 복구합니다.
- 학생이 직접 LED를 제어하는 코드를 작성한다면, 자동 LED 동작은 `DEFAULT`로 설정하세요.

설정을 변경한 뒤 `Ctrl + Shift + B`로 **재업로드**해야 EV3에 반영됩니다. `EV3: 상태 확인`은 설정 변경을 적용하지 않습니다. Xbox Relay는 재시작할 필요가 없습니다. LED 접근에 실패하더라도 학생 Python 프로그램 실행은 계속됩니다.

<!-- brickrun note: it controls EV3 LCD ownership, while student_runner.py reports STARTING/RUNNING/STOPPED/ERROR. -->
