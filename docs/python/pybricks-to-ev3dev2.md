# Pybricks → ev3dev2 빠른 비교

Pybricks에 익숙할 때 자주 헷갈리는 부분만 빠르게 비교합니다.

| 목적 | Pybricks | ev3dev2 |
|---|---|---|
| EV3 본체 | `ev3 = EV3Brick()` | 전체 본체 객체 없음 |
| 라지 모터 A | `Motor(Port.A)` | `LargeMotor(OUTPUT_A)` |
| 미디엄 모터 B | `Motor(Port.B)` | `MediumMotor(OUTPUT_B)` |
| 모터 계속 회전 | `motor.run(500)` | `motor.on(SpeedPercent(50))` |
| 모터 정지 | `motor.stop()` | `motor.off()` |
| 모터 각도 | `motor.angle()` | `motor.position` |
| 탱크 주행 | `DriveBase` 또는 직접 제어 | `MoveTank` |
| steering 주행 | 직접 계산 | `MoveSteering` |
| 조이스틱 주행 | 직접 계산 | `MoveJoystick` |
| 거리/회전/좌표 | `DriveBase` | `MoveDifferential` |
| 자이로 각도 | `gyro.angle()` | `gyro.angle` |
| 터치센서 | `TouchSensor` | `TouchSensor` |
| 컬러센서 | `ColorSensor` | `ColorSensor` |
| 초음파센서 | `UltrasonicSensor` | `UltrasonicSensor` |
| EV3 버튼 | `ev3.buttons` | `Button()` |
| EV3 LED | `ev3.light` | `Leds()` |
| EV3 소리 | `ev3.speaker` | `Sound()` |
| 비동기 | Pybricks 환경별 방식 | Python 표준 `asyncio` |

## 가장 중요한 차이

Pybricks에서는 하나의 EV3 객체 아래에 본체 기능이 모입니다.

```python
ev3 = EV3Brick()
```

ev3dev2에서는 필요한 본체 기능을 각각 만듭니다.

```python
button = Button()
leds = Leds()
sound = Sound()
battery = PowerSupply()
```

모터/센서도 실제 장치 종류와 포트로 직접 만듭니다.

```python
motor = LargeMotor(OUTPUT_A)
gyro = GyroSensor(INPUT_1)
```

## 괄호를 주의해서 보기

Pybricks와 ev3dev2는 같은 정보를 읽더라도 함수와 속성 형태가 다를 수 있습니다.

```python
# ev3dev2
angle = gyro.angle
position = motor.position
```

여기에는 괄호가 없습니다.

반면:

```python
x, y = controller.joystick_left()
motor.on(SpeedPercent(50))
```

는 함수/메서드이므로 괄호가 있습니다.
