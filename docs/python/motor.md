# Motor

## 빠른 API

| 종류 | 기능 | 사용 |
|---|---|---|
| 클래스 | 라지 모터 | `LargeMotor(OUTPUT_A)` |
| 클래스 | 미디엄 모터 | `MediumMotor(OUTPUT_B)` |
| 메서드 | 계속 회전 | `motor.on(speed)` |
| 메서드 | 정지 | `motor.off(brake=True)` |
| 메서드 | 시간만큼 | `motor.on_for_seconds(speed, seconds)` |
| 메서드 | 각도만큼 | `motor.on_for_degrees(speed, degrees)` |
| 메서드 | 회전수만큼 | `motor.on_for_rotations(speed, rotations)` |
| 메서드 | 목표 위치 | `motor.on_to_position(speed, position)` |
| 속성 | 엔코더 위치 | `motor.position` |
| 속성 | 현재 속도 | `motor.speed` |
| 속성 | 동작 중 | `motor.is_running` |

공식 `Motor.on(speed, brake=True, block=False)`는 기본적으로 계속 회전시키고 바로 다음 코드로 넘어갑니다.

공식 클래스:

```python
from ev3dev2.motor import (
    LargeMotor,
    MediumMotor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
    SpeedPercent,
    SpeedRPM,
    SpeedRPS,
    SpeedDPS,
)
```

## 모터 만들기

```python
left_motor = LargeMotor(OUTPUT_A)
shooter_motor = MediumMotor(OUTPUT_B)
```

`LargeMotor`는 EV3 Large Motor, `MediumMotor`는 EV3 Medium Motor가
해당 포트에 연결되어 있어야 초기화됩니다.

## 속도 단위

가장 쉬운 것은 퍼센트입니다.

```python
SpeedPercent(30)
SpeedPercent(-30)
```

다른 단위도 사용할 수 있습니다.

```python
SpeedRPM(200)
SpeedRPS(2)
SpeedDPS(500)
```

## 로봇축구에서 가장 중요한 두 명령

로봇축구에서는 먼저 `on()`과 `off()`를 익힙니다. 정해진 각도나 시간이
아니라 컨트롤러 상태가 바뀔 때까지 모터를 계속 움직이는 경우가 대부분입니다.

## on(speed, brake=True, block=False)

**메서드**

계속 회전합니다. `on()`은 기본적으로 기다리지 않고 바로 다음 Python 코드로
넘어갑니다.

```python
motor.on(SpeedPercent(30))
```

다른 명령이나 정지 명령이 올 때까지 회전합니다.

## off(brake=True)

**메서드**

모터를 정지합니다.

```python
motor.off()
```

```python
motor.off(brake=False)
```

- `brake=True`: 브레이크 정지
- `brake=False`: coast 정지

## 정해진 양만큼 움직이는 명령

아래 명령들은 로봇축구의 기본 조종보다는 자동 미션, 특정 기구의 위치 이동,
테스트 등에 필요할 때 사용합니다.

## on_for_seconds(speed, seconds, brake=True, block=True)

**메서드**

정해진 시간만큼 회전합니다.

```python
motor.on_for_seconds(
    SpeedPercent(30),
    2,
)
```

2초 동안 회전하고 멈춥니다.

## on_for_degrees(speed, degrees, brake=True, block=True)

**메서드**

정해진 각도만큼 회전합니다.

```python
motor.on_for_degrees(
    SpeedPercent(30),
    360,
)
```

## on_for_rotations(speed, rotations, brake=True, block=True)

**메서드**

정해진 회전 수만큼 움직입니다.

```python
motor.on_for_rotations(
    SpeedPercent(30),
    2,
)
```

## on_to_position(speed, position, brake=True, block=True)

**메서드**

엔코더의 목표 위치로 이동합니다.

```python
motor.on_to_position(
    SpeedPercent(30),
    90,
)
```

## position

**속성**

현재 엔코더 위치를 읽습니다.

```python
print(motor.position)
```

LEGO EV3 회전 모터에서는 위치 값을 각도처럼 사용할 수 있습니다.

현재 위치를 0으로 만들려면:

```python
motor.position = 0
```

## speed

**속성**

현재 속도를 읽습니다.

```python
print(motor.speed)
```

## polarity

**속성**

모터의 양의 방향을 반대로 바꾸고 싶을 때 사용합니다.

```python
motor.polarity = motor.POLARITY_INVERSED
```

원래대로:

```python
motor.polarity = motor.POLARITY_NORMAL
```

로봇을 조립한 뒤 좌우 모터 방향이 다르면 각 모터의 `polarity`를 설정할 수
있습니다.

## 상태

```python
print(motor.is_running)
print(motor.is_holding)
print(motor.is_stalled)
```

또는:

```python
print(motor.state)
```

## block

`on_for_seconds()`, `on_for_degrees()` 등의 기본값은 완료될 때까지 기다리는
`block=True`입니다.

```python
motor.on_for_degrees(
    SpeedPercent(30),
    360,
    block=False,
)
```

로 실행하면 명령을 시작하고 다음 Python 코드로 바로 넘어갑니다.

## 자주 쓰는 예제

```python
from ev3dev2.motor import (
    MediumMotor,
    OUTPUT_B,
    SpeedPercent,
)

shooter = MediumMotor(OUTPUT_B)

shooter.position = 0

shooter.on_for_degrees(
    SpeedPercent(50),
    35,
)

print(shooter.position)

shooter.off(brake=True)
```

공식 문서:
https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
