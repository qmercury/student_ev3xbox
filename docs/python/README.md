# EV3 Python Reference

이 문서는 **ev3dev + Python 3 + python-ev3dev2 + EV3 Xbox Relay** 환경에서
학생들이 로봇 코드를 작성할 때 보는 수업용 레퍼런스입니다.

Pybricks 문법을 흉내 내지 않습니다. EV3에 실제 설치되어 있는
`python-ev3dev2`의 클래스와 메서드를 그대로 사용하고, Xbox 부분만
이 프로젝트의 `ev3xbox` 라이브러리를 사용합니다.

공식 문서:

- https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/
- Motor: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
- Sensor: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html
- API Index: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/genindex.html

## 먼저 보기

- [EV3Dev2 처음 시작하기](getting-started.md) — Pybricks에 익숙한 경우 먼저 보기
- [Pybricks → ev3dev2 빠른 비교](pybricks-to-ev3dev2.md) — 자주 헷갈리는 문법 비교
- [속성과 메서드](properties-methods.md) — 괄호가 있는 것과 없는 것의 차이
- [API 빠른 색인](api-index.md) — 하고 싶은 동작에서 바로 함수 찾기

## 빠른 찾기

- [학생용 비동기 프로그램 구조](student-program-structure.md) — import부터 finally까지 한 장 정리
- [asyncio 로봇 기능 나누기](asyncio.md) — 주행, 슈터, 속도 변경을 독립 task로 실행
- [로봇축구 제어 루프](control-loop.md) — 버튼/조이스틱 상태에 따라 계속 움직이고 즉시 정지
- [Motor](motor.md) — LargeMotor, MediumMotor, 연속 회전과 정지, 필요할 때 위치/시간 제어
- [Drive](drive.md) — MoveTank, MoveSteering, MoveJoystick, MoveDifferential
- [Sensors](sensors.md) — Touch, Color, Ultrasonic, Gyro
- [Brick](brick.md) — 버튼, LED, 소리, 배터리
- [Xbox](xbox.md) — 교사 Relay에서 전달되는 Xbox 입력
- [Python 기본](python-basics.md) — 변수, 조건문, 반복문, 함수, set, global, 예외
- [VSCode](vscode.md) — 작성, 업로드, 실행, 로그

## 로봇축구의 기본 제어 방식

로봇축구에서는 정해진 각도나 시간을 미리 주는 것보다 **현재 컨트롤러 상태에
따라 계속 움직이고, 버튼을 놓거나 다른 입력이 오면 즉시 멈추거나 방향을
바꾸는 방식**을 기본으로 합니다.

수업에서는 여기에 `asyncio`를 사용해서 로봇의 기능을 나눕니다.

```text
drive_task()      주행
shooter_task()    슈터
speed_task()      속도 변경
```

각 task는 짧게 상태를 확인하고 `await asyncio.sleep()`으로 다른 task에
실행 기회를 넘깁니다. 자세한 구조는 [asyncio 로봇 기능 나누기](asyncio.md)를
봅니다.

```python
import asyncio

from ev3dev2.motor import MediumMotor, OUTPUT_B, SpeedPercent
from ev3xbox import XboxButton, XboxController

motor = MediumMotor(OUTPUT_B)
controller = XboxController()


async def shooter_task():
    while True:
        pressed = controller.buttons.pressed()

        if XboxButton.A in pressed:
            motor.on(SpeedPercent(100))
        else:
            motor.off(brake=True)

        await asyncio.sleep(0.02)
```

자세한 패턴은 [로봇축구 제어 루프](control-loop.md)를 봅니다.

## 가장 기본적인 Xbox 코드

```python
from time import sleep

from ev3xbox import XboxButton, XboxController

controller = XboxController()

try:
    while True:
        pressed = controller.buttons.pressed()

        if XboxButton.A in pressed:
            print("A")

        x, y = controller.joystick_left()
        print(x, y)

        sleep(0.02)

finally:
    controller.close()
```

## 포트 이름

모터:

```python
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
```

센서:

```python
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
```

수업에서는 실제 EV3 포트와 같은 문자를 그대로 사용합니다.

## 수업 원칙

학생은 완성된 로봇 코드를 외우는 것이 아니라 레퍼런스에서 필요한 API를 찾아 조합합니다. 이 문서는 알고리즘의 정답을 제공하지 않고, 사용할 수 있는 Python/EV3/Xbox 기능을 찾기 쉽게 정리하는 데 목적이 있습니다.

예를 들어:

```text
모터를 30%로 계속 돌리고 싶다
→ Motor 문서
→ motor.on(SpeedPercent(30))

오른쪽 스틱 값을 알고 싶다
→ Xbox 문서
→ controller.joystick_right()

500 mm 직진하고 싶다
→ Drive 문서
→ MoveDifferential.on_for_distance(...)
```

이 문서에 없는 고급 기능은 공식 python-ev3dev2 문서의 API Index에서
추가로 찾습니다.
