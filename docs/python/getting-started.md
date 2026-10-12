# EV3Dev2 처음 시작하기

이 문서는 Pybricks에 익숙하지만 `python-ev3dev2`가 처음인 경우를 위한 빠른 시작 문서입니다.

핵심 차이는 하나입니다.

```text
Pybricks
ev3 = EV3Brick()

ev3dev2
필요한 장치를 각각 객체로 만듭니다.
```

## 1. 라이브러리 import

수업용 기본 import 예:

```python
import asyncio

from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, MoveSteering, MoveJoystick, MoveDifferential, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3xbox import XboxButton, XboxController
```

모든 클래스를 반드시 사용할 필요는 없습니다. 학생은 실제로 필요한 것만 남겨도 됩니다.

## 2. 장치 선언

Pybricks처럼 `ev3 = EV3Brick()`를 먼저 만들지 않습니다.

모터:

```python
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_D)
shooter = MediumMotor(OUTPUT_B)
```

센서:

```python
touch = TouchSensor(INPUT_1)
color = ColorSensor(INPUT_2)
ultrasonic = UltrasonicSensor(INPUT_3)
gyro = GyroSensor(INPUT_4)
```

Xbox:

```python
controller = XboxController()
```

EV3 본체 기능:

```python
button = Button()
leds = Leds()
sound = Sound()
battery = PowerSupply()
```

## 3. 두 모터를 주행 장치로 묶기

좌우 모터를 각각 제어하고 싶으면:

```python
drive = MoveTank(
    OUTPUT_A,
    OUTPUT_D,
)
```

steering 방식이면:

```python
drive = MoveSteering(
    OUTPUT_A,
    OUTPUT_D,
)
```

Xbox 조이스틱처럼 x/y 값으로 제어하고 싶으면:

```python
drive = MoveJoystick(
    OUTPUT_A,
    OUTPUT_D,
)
```

## 4. 가장 기본적인 동작

모터 계속 회전:

```python
motor.on(
    SpeedPercent(50)
)
```

정지:

```python
motor.off(
    brake=True
)
```

모터 엔코더 읽기:

```python
print(
    motor.position
)
```

자이로 각도:

```python
print(
    gyro.angle
)
```

Xbox 왼쪽 스틱:

```python
x, y = controller.joystick_left()
```

Xbox 버튼:

```python
pressed = controller.buttons.pressed()

if XboxButton.A in pressed:
    print("A")
```

## 5. 속성과 메서드

ev3dev2에서는 현재 상태값을 **속성**으로 제공하는 경우가 많습니다.

```python
motor.position
motor.speed
gyro.angle
touch.is_pressed
```

동작을 실행하는 것은 보통 **메서드**입니다.

```python
motor.on(...)
motor.off(...)
gyro.reset()
```

자세한 설명: [속성과 메서드](properties-methods.md)

## 6. Pybricks와 비교

| Pybricks에서 익숙한 생각 | ev3dev2에서는 |
|---|---|
| `EV3Brick()` | 본체 기능을 각각 `Button()`, `Leds()`, `Sound()`, `PowerSupply()`로 만듦 |
| `Motor(Port.A)` | `LargeMotor(OUTPUT_A)` 또는 `MediumMotor(OUTPUT_A)` |
| `DriveBase(...)` | `MoveTank`, `MoveSteering`, `MoveJoystick`, `MoveDifferential` |
| `gyro.angle()` | `gyro.angle` |
| `motor.angle()` | `motor.position` |
| `motor.run(...)` | `motor.on(...)` |
| `motor.stop()` | `motor.off(...)` |

함수 호출인지 속성 읽기인지가 다를 수 있으므로 괄호 유무를 잘 봅니다.

예:

```python
gyro.angle
motor.position
```

는 **속성**이라 괄호가 없습니다.

반면:

```python
motor.on(...)
motor.off(...)
controller.joystick_left()
```

는 **함수/메서드**라 괄호가 있습니다.

## 7. async는 Python 기능

```python
import asyncio
```

`async`, `await`, `asyncio.gather()`는 ev3dev2의 기능이 아니라 Python 3 표준 기능입니다.

예:

```python
async def drive():
    while True:
        x, y = controller.joystick_left()

        # 학생이 주행 코드 작성

        await asyncio.sleep(0.02)
```

## 8. 학생 코드 작성 순서

학생은 보통 다음 순서로 작성하면 됩니다.

```text
1. 필요한 라이브러리 import
2. 장치 선언
3. 변수 선언
4. 함수 / async 함수 작성
5. main 작성
6. 실행
```

하지만 함수 구조나 알고리즘은 정해진 정답이 아닙니다. 로봇에 맞게 학생이 직접 설계합니다.
