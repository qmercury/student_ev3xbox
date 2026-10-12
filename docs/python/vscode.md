# VSCode에서 EV3 프로그램 작성하고 실행하기

학생은 VSCode에서 `main.py`를 작성하고 자기 EV3에 업로드해서 실행합니다.

Relay 프로그램은 Xbox 입력을 EV3로 전달하고, 학생 프로그램은 VSCode에서 별도로 관리합니다. 한 학생 노트북이 Relay와 VSCode를 함께 실행할 수도 있습니다.

```text
학생 노트북
VSCode
   ↓
main.py
   ↓
Ctrl + Shift + B
   ↓ SSH / SCP
자기 EV3
   ↓
Python 3 + python-ev3dev2
   ↓
학생 프로그램 실행
```

Xbox를 사용하는 경우에는 배포 도구가 이 프로젝트의 `ev3xbox.py`도 같이 EV3에 복사합니다.

`xbox_service.py`는 학생 프로그램과 별도로 EV3에서 항상 실행됩니다.

### EV3 본체에 실행 상태 표시

새 버전은 학생 코드와 함께 `student_runner.py`를 업로드합니다. 실행하면 EV3 LCD에 `STARTING` → `RUNNING`을 표시하고, 종료하면 `STOPPED`, 오류로 종료하면 `ERROR`를 표시합니다. `brickrun -r`을 통해 학생 프로그램 실행 중 EV3 기본 메뉴(Brickman) 대신 해당 프로그램의 화면을 유지하며, LCD는 상태가 변경될 때만 갱신합니다. `RUNNING`은 Python 코드가 실행 중임을 뜻하며 Xbox 입력 수신 및 모터 초기화까지 확인했다는 뜻은 아닙니다.

자동 표시가 학생 코드의 직접적인 LCD 사용을 방해한다면 `.vscode/ev3-target.json`에서 `"lcd_status": false`로 설정하세요. LCD 출력 실패는 학생 Python 프로그램의 실행을 방해하지 않도록 처리합니다.

**처음 복제할 때는** [student_ev3xbox README의 Mac/Windows 복제 명령](../../README.md#처음-다운로드-터미널에서-github-저장소-복제하기)을 먼저 실행하세요. `main.py`는 저장소 루트에 있으며, 예제 JSON에서 개인 설정 파일을 만든 뒤 자신의 Robot ID를 설정합니다.

학생별 `.vscode/ev3-target.json`의 `lcd_title`, `lcd_program`, `lcd_starting_text`, `lcd_running_text`, `lcd_stopped_text`, `lcd_error_text`, `led_color`, `led_effect` 값을 수정하여 글씨와 버튼 LED를 변경할 수 있습니다. 자세한 설정과 예시는 프로젝트 [README.md](../../README.md)를 참고하세요. 변경 사항은 다음 업로드 시 적용됩니다.


---

# 1. 학생이 수정하는 파일

기본적으로 학생이 작성하는 파일은:

```text
main.py
```

입니다.

처음 파일에는 자주 사용하는 import만 들어 있습니다.

예:

```python
import asyncio
from time import sleep

from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, MoveSteering, MoveJoystick, MoveDifferential, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, SpeedRPM, SpeedRPS, SpeedDPS
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.display import Display
from ev3dev2.console import Console
from ev3xbox import XboxButton, XboxController
```

학생은 그 아래에서 직접:

```text
장치 선언
변수 선언
함수 작성
async 함수 작성
main 작성
실행 코드 작성
```

을 합니다.

모든 import를 반드시 사용할 필요는 없습니다.

---

# 2. EV3 연결 설정

각 학생 노트북에는 자기 EV3의 접속 정보를 저장합니다.

예제 파일:

```text
.vscode/ev3-target.example.json
```

을 복사해서:

```text
.vscode/ev3-target.json
```

을 만듭니다.

기본 예:

```json
{
  "host": "192.168.77.2",
  "user": "robot",
  "port": 22,
  "robot_id": "EV3-01",
  "remote_dir": "/home/robot/ev3-student",
  "main_file": "main.py",
  "python": "python3",
  "connect_timeout": 5,
  "sync_library": true,
  "lcd_status": true,
  "lcd_title": "STUDENT",
  "lcd_program": "main.py",
  "lcd_starting_text": "STARTING",
  "lcd_running_text": "RUNNING",
  "lcd_stopped_text": "STOPPED",
  "lcd_error_text": "ERROR",
  "led_color": "DEFAULT",
  "led_effect": "DEFAULT"
}
```

중요한 값은:

```text
robot_id
→ 자기 EV3의 고유 ID

host
→ 최초 설정 또는 자동 검색 실패 시 사용할 예비 IP
```

입니다.

Xbox 서비스가 설치되어 있고 `robot_id`가 설정된 뒤에는 배포 도구가 현재 EV3 IP를 자동으로 찾습니다. DHCP로 IP가 바뀌어도 학생이 매번 `host`를 고칠 필요가 없도록 하는 방향입니다.

학생별 `.vscode/ev3-target.json`은 각자 생성합니다. 이 파일은 Git에 올리지 않습니다.

---

# 3. 최초 연결 설정

처음 한 번은 SSH 키를 EV3에 등록합니다.

VSCode에서:

```text
Terminal
→ Run Task
→ EV3: 최초 연결 설정
```

을 선택합니다.

처음에는 EV3의 `robot` 계정 암호를 한 번 물어볼 수 있습니다.

성공하면 대략:

```text
SSH_KEY=INSTALLED
SSH_KEY=OK
Pairing complete
```

와 같은 메시지가 표시됩니다.

이후에는 매번 암호를 입력하지 않고 업로드할 수 있습니다.

---

# 4. 작성 → 업로드 → 실행

학생이 `main.py`를 수정한 뒤:

```text
Ctrl + Shift + B
```

를 누릅니다.

기본 build task:

```text
EV3: 업로드 및 실행
```

이 실행됩니다.

배포 도구는 다음 순서로 동작합니다.

```text
1. EV3 SSH 연결 확인
2. 이전 학생 프로그램 정지
3. 학생용 폴더 준비
4. main.py 업로드
5. ev3xbox.py 업로드
6. 새 학생 프로그램 실행
```

중요:

```text
이 과정은 학생 프로그램만 관리합니다.
xbox_service.py는 중지하지 않습니다.
```

---

# 5. 실행 결과 보기

정상적으로 계속 실행되는 프로그램이면:

```text
STUDENT_PROGRAM=RUNNING
```

이 표시됩니다.

프로그램이 바로 끝났다면:

```text
STUDENT_PROGRAM=FINISHED
```

이 표시될 수 있습니다.

Python 오류가 발생해서 바로 종료되면:

```text
STUDENT_PROGRAM=ERROR
Traceback ...
```

형태로 오류가 표시됩니다.

이때 Traceback의 마지막 부분을 먼저 봅니다.

예:

```text
NameError
TypeError
AttributeError
SyntaxError
```

그리고 표시된 `main.py` 줄 번호를 확인합니다.

---

# 6. 상태 확인

현재 EV3 연결 상태를 확인하려면:

```text
Terminal
→ Run Task
→ EV3: 상태 확인
```

을 실행합니다.

정상 예:

```text
SSH=OK
PYTHON=Python 3.x.x
XBOX_SERVICE=RUNNING
STUDENT_PROGRAM=RUNNING pid=...
```

각 항목 의미:

| 표시 | 의미 |
|---|---|
| `SSH=OK` | 학생 노트북에서 EV3 접속 가능 |
| `PYTHON=...` | EV3의 Python 실행 가능 |
| `XBOX_SERVICE=RUNNING` | 교사 Xbox 입력을 받는 EV3 서비스 실행 중 |
| `STUDENT_PROGRAM=RUNNING` | 학생 프로그램 실행 중 |
| `STUDENT_PROGRAM=NOT_RUNNING` | 학생 프로그램이 실행 중이 아님 |

Xbox를 사용하지 않는 수업이라면 학생 프로그램 자체는 `XBOX_SERVICE`와 관계없이 작성할 수 있습니다.

---

# 7. 학생 프로그램 정지

VSCode에서:

```text
Terminal
→ Run Task
→ EV3: 정지
```

을 실행합니다.

배포 도구는:

```text
학생 Python 프로그램 종료
        ↓
EV3 tacho motor 정지 시도
```

를 수행합니다.

중요:

```text
교사용 xbox_service.py는 건드리지 않습니다.
```

따라서 한 학생이 자기 코드를 정지해도 Xbox 전달 서비스 자체를 다시 설치하거나 시작할 필요는 없습니다.

---

# 8. 로그 보기

학생 프로그램의 `print()`와 오류는 EV3의:

```text
/home/robot/ev3-student/student.log
```

에 저장됩니다.

최근 로그를 보려면:

```text
Terminal
→ Run Task
→ EV3: 로그 보기
```

를 선택합니다.

기본적으로 최근 100줄을 보여줍니다.

예:

```python
print("ready")
print(controller.joystick_left())
```

학생 코드의 출력이 로그에 남습니다.

## 로그 실시간 보기

프로그램이 실행되는 동안 출력이 계속 바뀌는 것을 보고 싶으면:

```text
Terminal
→ Run Task
→ EV3: 로그 실시간 보기
```

를 사용합니다.

중지하려면 터미널에서:

```text
Ctrl + C
```

를 누릅니다.

이 Ctrl+C는 **로그 보기 명령만 종료**합니다. 학생 프로그램을 정지하려면 `EV3: 정지` task를 사용합니다.

---

# 9. F5

`F5`도 현재 저장소에서는:

```text
EV3: 업로드 및 실행
```

용도로 설정되어 있습니다.

즉:

```text
Ctrl + Shift + B
또는
F5
```

로 EV3에 코드를 배포할 수 있습니다.

여기서 F5는 PC에서 `main.py`를 로컬 실행하는 것이 아니라 `tools/ev3_deploy.py`를 실행해 EV3로 배포하는 동작입니다.

---

# 10. 자동완성과 빨간 줄

학생 PC에는 EV3용 `python-ev3dev2`를 직접 설치하지 않아도 됩니다.

VSCode 설정:

```json
{
  "python.analysis.extraPaths": [
    "./ev3"
  ],
  "python.analysis.stubPath": "./typings",
  "python.analysis.typeCheckingMode": "basic"
}
```

저장소의:

```text
typings/ev3dev2
```

가 VSCode/Pylance에 클래스, 메서드, 속성 정보를 알려줍니다.

실제 실행 시에는 EV3에 설치된 `python-ev3dev2`를 사용합니다.

즉:

```text
학생 PC
→ 타입 정보와 자동완성만 사용

EV3
→ 실제 python-ev3dev2 실행
```

입니다.

우리 Xbox 라이브러리도:

```text
ev3/ev3xbox.py
ev3/ev3xbox.pyi
```

를 통해 코드와 자동완성을 제공합니다.

---

# 11. 학생이 자주 만나는 오류

## 빨간 줄은 있는데 EV3 실행과는 별개

Pylance의 빨간 줄은 학생 PC의 코드 분석 결과입니다.

EV3에서 실제로 실행한 오류는:

```text
EV3: 로그 보기
```

의 Traceback을 확인합니다.

## SSH 연결 실패

먼저:

```text
EV3: 상태 확인
```

을 실행합니다.

실패하면:

```text
EV3 전원이 켜져 있는가?
USB/네트워크 연결이 되어 있는가?
EV3의 Robot ID가 맞는가?\n자동 검색이 안 될 때 예비 host 주소가 맞는가?
```

를 확인합니다.

## ModuleNotFoundError: ev3xbox

`sync_library`가 `true`인지 확인합니다.

```json
"sync_library": true
```

배포할 때 `ev3xbox.py`가 학생 프로그램과 같은 원격 폴더에 복사됩니다.

## AttributeError

메서드와 속성을 혼동했는지 확인합니다.

예:

```python
gyro.angle
```

는 속성입니다.

```python
gyro.angle()
```

처럼 쓰면 오류가 발생할 수 있습니다.

자세히: [속성과 메서드](properties-methods.md)

---

# 12. 수업 중 기본 작업 순서

학생에게는 다음 흐름만 먼저 익히게 해도 충분합니다.

```text
1. main.py 작성
2. 저장
3. Ctrl + Shift + B
4. EV3 동작 확인
5. 문제가 있으면 EV3: 로그 보기
6. 코드 수정
7. 다시 Ctrl + Shift + B
```

필요하면:

```text
EV3: 정지
EV3: 상태 확인
EV3: 로그 실시간 보기
```

를 사용합니다.

이 반복이 학생의 기본 개발 사이클입니다.

```text
생각
 ↓
코드 작성
 ↓
EV3에서 실행
 ↓
관찰
 ↓
오류/동작 수정
 ↓
다시 실행
```

완성된 로봇 알고리즘을 제공하는 것이 아니라 학생이 이 반복을 통해 자기 로봇 동작을 만들어가는 것을 목표로 합니다.

<!-- brickrun note: it controls EV3 LCD ownership, while student_runner.py reports STARTING/RUNNING/STOPPED/ERROR. -->
