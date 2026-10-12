# EV3 Python API Index

학생이 **하고 싶은 동작부터 찾아가는 페이지**입니다.

수업의 기본 구성:

```text
Python 3 표준 기능
├─ asyncio
└─ 일반 Python 문법

python-ev3dev2
├─ Motor
├─ Drive
├─ Sensors
└─ EV3 Brick

ev3xbox
└─ XboxController
```

## 모터

| 하고 싶은 일 | API |
|---|---|
| 라지 모터 만들기 | `LargeMotor(OUTPUT_A)` |
| 미디엄 모터 만들기 | `MediumMotor(OUTPUT_B)` |
| 계속 회전 | `motor.on(speed)` |
| 즉시 정지 | `motor.off(brake=True)` |
| 현재 엔코더 위치 | `motor.position` |
| 현재 속도 | `motor.speed` |
| 지정 시간 회전 | `motor.on_for_seconds(...)` |
| 지정 각도 회전 | `motor.on_for_degrees(...)` |
| 지정 회전수 회전 | `motor.on_for_rotations(...)` |
| 목표 위치 이동 | `motor.on_to_position(...)` |
| 동작 중인지 확인 | `motor.is_running` |

자세히: [Motor](motor.md)

## 주행

| 하고 싶은 일 | API |
|---|---|
| 좌/우 모터를 각각 제어 | `MoveTank` |
| steering + speed로 제어 | `MoveSteering` |
| 조이스틱 x/y로 제어 | `MoveJoystick` |
| 거리/회전/좌표 이동 | `MoveDifferential` |
| 계속 주행 | `drive.on(...)` |
| 정지 | `drive.off(brake=True)` |

로봇축구 조이스틱 주행에서는 `MoveJoystick`이 가장 직접적입니다.

자세히: [Drive](drive.md)

## Xbox

| 하고 싶은 일 | 종류 | API |
|---|---|---|
| 컨트롤러 만들기 | 클래스 | `XboxController()` |
| 버튼 인터페이스 | 속성 | `controller.buttons` |
| 현재 누른 버튼 | 메서드 | `controller.buttons.pressed()` |
| 왼쪽 스틱 | 메서드 | `controller.joystick_left()` |
| 오른쪽 스틱 | 메서드 | `controller.joystick_right()` |
| LT / RT | 메서드 | `controller.triggers()` |
| 연결 여부 | 메서드 | `controller.connected()` |
| 연결 대기 | 메서드 | `controller.wait_until_connected()` |
| 종료 | 메서드 | `controller.close()` |

버튼 이름:

```python
XboxButton.A
XboxButton.B
XboxButton.X
XboxButton.Y
XboxButton.LB
XboxButton.RB
XboxButton.UP
XboxButton.DOWN
XboxButton.LEFT
XboxButton.RIGHT
```

자세히: [Xbox](xbox.md)

## 센서

| 센서 | 종류 | 자주 쓰는 API |
|---|---|---|
| TouchSensor | 속성 | `is_pressed` |
| ColorSensor | 속성 | `reflected_light_intensity`, `color`, `rgb` |
| UltrasonicSensor | 속성 | `distance_centimeters` |
| GyroSensor | 속성 | `angle`, `rate` |
| GyroSensor | 메서드 | `reset()`, `calibrate()` |

자세히: [Sensors](sensors.md)

## EV3 본체

| 하고 싶은 일 | 종류 | API |
|---|---|---|
| 현재 눌린 버튼 목록 | 속성 | `button.buttons_pressed` |
| 위/아래/좌/우/가운데 버튼 | 속성 | `button.up`, `button.down`, `button.left`, `button.right`, `button.enter` |
| 아무 버튼이나 눌림 | 메서드 | `button.any()` |
| LED 색 변경 | 메서드 | `leds.set_color(...)` |
| LED 모두 끄기 | 메서드 | `leds.all_off()` |
| 비프음 | 메서드 | `sound.beep()` |
| 음 재생 | 메서드 | `sound.tone(...)` |
| 음량 설정 | 메서드 | `sound.set_volume(...)` |
| 배터리 전압 | 속성 | `battery.measured_volts` |
| 배터리 전류 | 속성 | `battery.measured_amps` |
| LCD 지우기 | 메서드 | `display.clear()` |
| LCD 갱신 | 메서드 | `display.update()` |
| LCD 그림 객체 | 속성 | `display.draw` |
| LCD 텍스트 | 메서드 | `console.text_at(...)` |
| 콘솔 행/열 | 속성 | `console.rows`, `console.columns` |

자세히: [Brick](brick.md)

## asyncio

| 하고 싶은 일 | API |
|---|---|
| 비동기 함수 만들기 | `async def ...` |
| 다른 task에 실행권 넘기기 | `await asyncio.sleep(...)` |
| 여러 기능 동시에 실행 | `await asyncio.gather(...)` |
| EV3에서 이벤트 루프 가져오기 | `asyncio.get_event_loop()` |
| main 실행 | `loop.run_until_complete(main())` |

로봇축구에서는 보통:

```text
drive_task()
shooter_task()
speed_task()
sensor_task()
```

처럼 **기능 단위로 task를 나눕니다.**

자세히: [asyncio](asyncio.md)

## Python 기본 문법

| 하고 싶은 일 | 문법 / 함수 |
|---|---|
| 조건 판단 | `if / elif / else` |
| 계속 반복 | `while` |
| 함수 만들기 | `def` |
| 값 반환 | `return` |
| 포함 여부 | `in` |
| 현재 버튼 집합 | `set` |
| 새로 눌린 버튼 계산 | `current - previous` |
| 전역 변수 변경 | `global` |
| 값 상한 제한 | `min()` |
| 값 하한 제한 | `max()` |
| 종료 정리 | `try / finally` |

자세히: [Python 기본](python-basics.md)

## 포트

모터:

```python
OUTPUT_A
OUTPUT_B
OUTPUT_C
OUTPUT_D
```

센서:

```python
INPUT_1
INPUT_2
INPUT_3
INPUT_4
```

## 속도

가장 많이 쓰는 단위:

```python
SpeedPercent(50)
```

다른 단위:

```python
SpeedRPM(200)
SpeedRPS(2)
SpeedDPS(500)
SpeedDPM(30000)
```

## 공식 문서

이 레퍼런스는 수업용 빠른 문서입니다. 전체 API가 필요하면 공식 문서를 봅니다.

- python-ev3dev2: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/
- Motor/Drive: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
- Sensors: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html
- API Index: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/genindex.html
