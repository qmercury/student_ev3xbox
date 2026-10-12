# 로봇축구 제어 루프

로봇축구에서는 보통 모터를 **몇 도**, **몇 초**, **몇 바퀴**처럼 미리 정한
양만큼 움직이지 않습니다.

대부분의 동작은 다음 형태입니다.

```text
입력 상태 확인
   ↓
움직여야 하면 on()
   ↓
계속 반복
   ↓
버튼을 놓거나 다른 입력이 오면 off() 또는 새로운 on()
```

즉 수업의 기본은 **이벤트를 기다리는 제어 루프**입니다. 실제 로봇축구 수업에서는 이 제어 루프를 기능별 `async` task로 나누는 방식을 기본으로 사용합니다.

## 가장 기본적인 패턴

먼저 한 기능만 보면 다음처럼 동작합니다.

```python
from time import sleep

from ev3dev2.motor import (
    MediumMotor,
    OUTPUT_B,
    SpeedPercent,
)

from ev3xbox import (
    XboxButton,
    XboxController,
)

motor = MediumMotor(OUTPUT_B)
controller = XboxController()

try:
    while True:
        pressed = controller.buttons.pressed()

        if XboxButton.A in pressed:
            motor.on(
                SpeedPercent(100)
            )
        else:
            motor.off(
                brake=True
            )

        sleep(0.02)

finally:
    motor.off(brake=True)
    controller.close()
```

A 버튼을 누르는 동안에는 계속 회전하고, A 버튼을 놓으면 다음 제어 루프에서
즉시 정지합니다.

`motor.on()`은 모터를 계속 회전시키고 바로 다음 Python 코드로 넘어갑니다.
따라서 버튼을 누르는 동안 `on()`을 유지하고 버튼을 놓으면 `off()`를
호출하는 구조가 로봇축구에 잘 맞습니다.

## 조이스틱 주행

```python
from time import sleep

from ev3dev2.motor import (
    MoveJoystick,
    OUTPUT_A,
    OUTPUT_D,
)

from ev3xbox import XboxController

drive = MoveJoystick(
    OUTPUT_A,
    OUTPUT_D,
)

controller = XboxController()

try:
    while True:
        x, y = controller.joystick_left()

        drive.on(
            x,
            y,
        )

        sleep(0.02)

finally:
    drive.off(brake=True)
    controller.close()
```

조이스틱을 중앙으로 놓으면 `x=0, y=0`이 전달되므로 주행 출력도 0이 됩니다.

## 현재 상태와 이벤트의 차이

`buttons.pressed()`는 **지금 누르고 있는 버튼의 집합**입니다.

```python
pressed = controller.buttons.pressed()
```

예:

```text
현재: {A, RB}
```

A를 계속 누르고 있으면 루프가 반복될 때마다 계속 A가 포함되어 있습니다.

반면 **방금 눌림**과 **방금 놓임**은 이전 상태와 비교하면 알 수 있습니다.

```python
previous = set()

while True:
    current = controller.buttons.pressed()

    just_pressed = current - previous
    just_released = previous - current

    previous = current
```

## 버튼을 누른 순간

```python
if XboxButton.A in just_pressed:
    print("A가 방금 눌림")
```

## 버튼을 놓은 순간

```python
if XboxButton.A in just_released:
    print("A가 방금 놓임")
```

## 눌렀을 때 시작하고 놓았을 때 정지

```python
previous = set()

while True:
    current = controller.buttons.pressed()

    just_pressed = current - previous
    just_released = previous - current

    if XboxButton.A in just_pressed:
        motor.on(
            SpeedPercent(100)
        )

    if XboxButton.A in just_released:
        motor.off(
            brake=True
        )

    previous = current

    sleep(0.02)
```

이 방식은 매 루프마다 같은 모터 명령을 다시 보내지 않고 실제 상태가 바뀐
순간에만 명령을 보내고 싶을 때 유용합니다.

## 여러 장치를 동시에 제어

로봇축구에서는 주행, 슈터, 속도 변경 같은 기능을 각각 독립된 `async` task로
나눕니다.

```python
async def drive_task():
    while True:
        x, y = controller.joystick_left()
        drive.on(x, y)

        await asyncio.sleep(0.02)


async def shooter_task():
    while True:
        pressed = controller.buttons.pressed()

        if XboxButton.A in pressed:
            shooter.on(
                SpeedPercent(100)
            )
        else:
            shooter.off(
                brake=True
            )

        await asyncio.sleep(0.02)


async def main():
    await asyncio.gather(
        drive_task(),
        shooter_task(),
    )
```

이렇게 하면 주행과 슈터가 서로 독립적으로 계속 동작합니다.

`motor.on()`과 `drive.on()` 자체는 비차단 명령이지만, `asyncio`를 사용하면
학생이 로봇을 **기능 단위로 나누어 작성하고 나중에 각 기능을 독립적으로
변경하기 쉬워집니다.**

자세한 내용은 [asyncio 로봇 기능 나누기](asyncio.md)를 봅니다.

## 제어 주기

단일 동기식 예제에서는 `sleep(0.02)`를 사용할 수 있지만, 여러 기능을 동시에 실행하는 `async` task 안에서는:

```python
await asyncio.sleep(0.02)
```

를 사용합니다.

를 사용합니다.

20 ms 간격이므로 약 초당 50번 입력을 확인합니다. 학생 코드는 각 task 안에서 오래 기다리는 blocking 명령을 사용하지 않는 것이 중요합니다.

로봇축구에서는 다음 명령을 우선 사용합니다.

```text
motor.on()
motor.off()

drive.on()
drive.off()

controller.buttons.pressed()
controller.joystick_left()
controller.joystick_right()
controller.triggers()
```

`on_for_seconds()`, `on_for_degrees()`, `on_for_rotations()` 같은 정해진
양의 동작은 자동 미션이나 특정 메커니즘 동작이 필요할 때 선택적으로 사용합니다.
