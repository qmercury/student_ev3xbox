# Drive

`python-ev3dev2`에는 두 개의 주행 모터를 함께 제어하는 클래스가 여러 개 있습니다.

## import

```python
from ev3dev2.motor import MoveTank, MoveSteering, MoveJoystick, MoveDifferential, OUTPUT_A, OUTPUT_D, SpeedPercent, SpeedRPM
```

## 어떤 클래스를 쓰면 될까?

| 목적 | 클래스 |
|---|---|
| 왼쪽/오른쪽 속도를 직접 정함 | `MoveTank` |
| steering 값과 speed로 주행 | `MoveSteering` |
| 조이스틱 x/y 값으로 주행 | `MoveJoystick` |
| 거리·곡선·회전·좌표·오도메트리 | `MoveDifferential` |

로봇축구에서 Xbox 스틱을 그대로 이용하려면 `MoveJoystick`이 가장 간단합니다. 학생이 직접 좌우 모터 속도를 계산하고 싶다면 `MoveTank`을 사용할 수도 있습니다.

---

# MoveTank

왼쪽 모터와 오른쪽 모터의 속도를 각각 지정합니다.

## 장치 선언

```python
drive = MoveTank(OUTPUT_A, OUTPUT_D)
```

첫 번째 포트가 왼쪽 모터, 두 번째 포트가 오른쪽 모터입니다.

## 빠른 API

| 종류 | 기능 | API |
|---|---|---|
| 메서드 | 계속 주행 | `drive.on(left_speed, right_speed)` |
| 메서드 | 정지 | `drive.off(brake=True)` |
| 메서드 | 시간만큼 주행 | `drive.on_for_seconds(left_speed, right_speed, seconds, brake=True, block=True)` |
| 메서드 | 각도만큼 주행 | `drive.on_for_degrees(left_speed, right_speed, degrees, brake=True, block=True)` |
| 메서드 | 회전수만큼 주행 | `drive.on_for_rotations(left_speed, right_speed, rotations, brake=True, block=True)` |

## on(left_speed, right_speed)

**메서드**

왼쪽과 오른쪽 모터를 지정한 속도로 계속 회전시킵니다.

```python
drive.on(
    SpeedPercent(50),
    SpeedPercent(50),
)
```

두 값이 같으면 직진합니다.

```python
drive.on(
    SpeedPercent(-50),
    SpeedPercent(50),
)
```

처럼 부호를 반대로 하면 제자리 회전 형태가 됩니다.

`on()`은 계속 주행을 시작하고 바로 다음 Python 코드로 넘어갑니다. 로봇축구처럼 입력이 바뀔 때까지 계속 움직이는 제어에 적합합니다.

## off(brake=True)

**메서드**

두 모터를 정지합니다.

```python
drive.off(
    brake=True
)
```

```text
brake=True     브레이크 정지
brake=False    coast 정지
```

## on_for_seconds(left_speed, right_speed, seconds, brake=True, block=True)

**메서드**

정해진 시간 동안 주행합니다.

```python
drive.on_for_seconds(
    SpeedPercent(50),
    SpeedPercent(50),
    2,
)
```

## on_for_degrees(left_speed, right_speed, degrees, brake=True, block=True)

**메서드**

바깥쪽 모터 기준으로 지정한 각도만큼 움직입니다.

```python
drive.on_for_degrees(
    SpeedPercent(30),
    SpeedPercent(60),
    360,
)
```

## on_for_rotations(left_speed, right_speed, rotations, brake=True, block=True)

**메서드**

바깥쪽 모터 기준으로 지정한 회전수만큼 움직입니다.

```python
drive.on_for_rotations(
    SpeedPercent(50),
    SpeedPercent(50),
    2,
)
```

---

# MoveSteering

`steering` 하나와 `speed` 하나로 두 모터 속도를 계산합니다.

## 장치 선언

```python
drive = MoveSteering(OUTPUT_A, OUTPUT_D)
```

## steering 값

```text
-100   제자리 왼쪽 회전
   0   직진
 100   제자리 오른쪽 회전
```

그 사이의 값은 곡선 주행입니다.

## 빠른 API

| 종류 | 기능 | API |
|---|---|---|
| 메서드 | 계속 주행 | `drive.on(steering, speed)` |
| 메서드 | 시간만큼 | `drive.on_for_seconds(steering, speed, seconds, brake=True, block=True)` |
| 메서드 | 각도만큼 | `drive.on_for_degrees(steering, speed, degrees, brake=True, block=True)` |
| 메서드 | 회전수만큼 | `drive.on_for_rotations(steering, speed, rotations, brake=True, block=True)` |
| 메서드 | 정지 | `drive.off(brake=True)` |

## on(steering, speed)

**메서드**

```python
drive.on(
    0,
    SpeedPercent(50),
)
```

직진합니다.

```python
drive.on(
    30,
    SpeedPercent(50),
)
```

오른쪽으로 휘어 주행합니다.

`speed`는 바깥쪽, 즉 더 빠르게 도는 모터의 속도를 기준으로 계산됩니다.

---

# MoveJoystick

하나의 조이스틱 `x, y` 값을 좌우 모터 속도로 변환합니다.

## 장치 선언

```python
drive = MoveJoystick(OUTPUT_A, OUTPUT_D)
```

## on(x, y, radius=100.0)

**메서드**

```python
drive.on(
    20,
    70,
)
```

```text
x = 0, y = 0       중앙
x < 0              왼쪽 방향
x > 0              오른쪽 방향
y > 0              전진 방향
y < 0              후진 방향
```

`radius`의 기본값은 100입니다.

`MoveJoystick`은 classic arcade-drive 방식으로 x/y 좌표를 왼쪽과 오른쪽 모터의 속도로 변환합니다.

## Xbox와 연결

우리 `XboxController.joystick_left()`는 -100~100 범위의 `(x, y)` 값을 반환하므로 그대로 전달할 수 있습니다.

```python
x, y = controller.joystick_left()

drive.on(
    x,
    y,
)
```

속도 제한을 학생이 추가하고 싶다면 x/y 값을 조절한 뒤 `drive.on()`에 넣으면 됩니다. 어떤 방식으로 조절할지는 학생 알고리즘 영역입니다.

---

# MoveDifferential

`MoveDifferential`은 `MoveTank`을 확장한 고급 주행 클래스입니다.

추가 기능:

```text
거리 직진
좌/우 곡선
제자리 회전
오도메트리
좌표 이동
목표 각도 회전
```

## 장치 선언

기본 형태:

```python
drive = MoveDifferential(
    OUTPUT_A,
    OUTPUT_D,
    wheel_class,
    wheel_distance_mm,
)
```

인자:

```text
left_motor_port     왼쪽 모터 포트
right_motor_port    오른쪽 모터 포트
wheel_class         바퀴 크기를 알고 있는 Wheel 클래스
wheel_distance_mm   좌우 바퀴 중심 간 유효 거리(mm)
```

표준 EV3 타이어를 사용할 경우:

```python
from ev3dev2.wheel import EV3Tire

drive = MoveDifferential(
    OUTPUT_A,
    OUTPUT_D,
    EV3Tire,
    145,
)
```

중요: `EV3Tire`는 EV3 표준 타이어용입니다. 다른 지름의 바퀴를 사용한다면 실제 바퀴 크기에 맞는 `Wheel` 클래스를 사용해야 거리와 오도메트리 계산이 맞습니다. `Wheel`의 기본 생성자는 `Wheel(diameter_mm, width_mm)`이며 단위는 mm입니다.

또한 `wheel_distance_mm`는 단순히 자로 잰 값이 항상 정답은 아닙니다. 공식 문서도 로봇의 무게, 무게중심 등의 영향 때문에 실제 주행으로 보정할 수 있다고 설명합니다.

## 빠른 API

| 종류 | 기능 | API |
|---|---|---|
| 메서드 | 거리 직진 | `on_for_distance(speed, distance_mm, brake=True, block=True)` |
| 메서드 | 오른쪽 곡선 | `on_arc_right(speed, radius_mm, distance_mm, brake=True, block=True)` |
| 메서드 | 왼쪽 곡선 | `on_arc_left(speed, radius_mm, distance_mm, brake=True, block=True)` |
| 메서드 | 지정 각도 회전 | `turn_degrees(speed, degrees, ...)` |
| 메서드 | 오른쪽 회전 | `turn_right(speed, degrees, ...)` |
| 메서드 | 왼쪽 회전 | `turn_left(speed, degrees, ...)` |
| 메서드 | 오도메트리 시작 | `odometry_start(...)` |
| 메서드 | 오도메트리 종료 | `odometry_stop()` |
| 메서드 | 좌표 이동 | `on_to_coordinates(speed, x_target_mm, y_target_mm, ...)` |
| 메서드 | 목표 각도 | `turn_to_angle(speed, angle_target_degrees, ...)` |

## on_for_distance(speed, distance_mm, brake=True, block=True)

**메서드**

직선으로 지정 거리만큼 이동합니다.

```python
drive.on_for_distance(
    SpeedRPM(40),
    500,
)
```

500 mm 이동합니다.

## on_arc_right(speed, radius_mm, distance_mm, brake=True, block=True)

**메서드**

오른쪽 곡선으로 이동합니다.

```python
drive.on_arc_right(
    SpeedRPM(80),
    150,
    700,
)
```

```text
150   곡선 반지름(mm)
700   곡선을 따라 이동할 거리(mm)
```

왼쪽은:

```python
drive.on_arc_left(
    SpeedRPM(80),
    150,
    700,
)
```

입니다.

## turn_right() / turn_left()

**메서드**

제자리에서 지정 각도만큼 회전합니다.

```python
drive.turn_right(
    SpeedRPM(40),
    90,
)

drive.turn_left(
    SpeedRPM(40),
    90,
)
```

전체 형태:

```python
drive.turn_right(
    speed,
    degrees,
    brake=True,
    block=True,
    error_margin=2,
    use_gyro=False,
)
```

`use_gyro=True`를 사용할 때는 `drive.gyro`에 GyroSensor가 지정되어 있어야 하며, 공식 구현은 `use_gyro`, `brake`, `block`이 모두 True일 때 자이로를 이용해 회전 정확도를 높입니다.

## 오도메트리

오도메트리를 시작합니다.

```python
drive.odometry_start()
```

기본 시작값:

```text
theta = 90°
x = 0 mm
y = 0 mm
```

직접 지정할 수도 있습니다.

```python
drive.odometry_start(
    theta_degrees_start=90,
    x_pos_start=0,
    y_pos_start=0,
)
```

오도메트리를 시작하면 별도 스레드가 엔코더 값을 이용해 위치를 계속 갱신합니다.

## on_to_coordinates(speed, x_target_mm, y_target_mm, brake=True, block=True)

**메서드**

오도메트리 좌표를 이용해 목표 지점으로 이동합니다.

```python
drive.on_to_coordinates(
    SpeedRPM(40),
    300,
    300,
)
```

## turn_to_angle(speed, angle_target_degrees, ...)

**메서드**

목표 방향으로 회전합니다.

```python
drive.turn_to_angle(
    SpeedRPM(40),
    90,
)
```

## odometry_stop()

**메서드**

오도메트리 스레드를 종료합니다.

```python
drive.odometry_stop()
```

---

## async에서 주의할 점

`on()`은 계속 움직이기 시작하고 바로 다음 코드로 넘어가므로 로봇축구의 빠른 제어 루프에서 사용하기 좋습니다.

반면 `on_for_distance()`, `turn_right()` 같은 메서드는 기본값이 `block=True`입니다.

async task 안에서 다른 task가 계속 실행되어야 한다면 상황에 따라:

```python
drive.on_for_distance(
    SpeedRPM(40),
    500,
    block=False,
)
```

처럼 비차단으로 시작하고 상태를 직접 관리하는 방식이 필요할 수 있습니다.

어떤 동작을 동시에 실행할지는 학생이 자신의 로봇 알고리즘에 맞게 결정합니다.

## 공식 문서

- Motor / Drive: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
- Wheels: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/wheels.html
