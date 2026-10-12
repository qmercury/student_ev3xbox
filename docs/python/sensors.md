# Sensors

EV3 센서는 `python-ev3dev2`에서 대부분 **현재 값을 속성(property)으로 읽는 방식**입니다.

예:

```python
gyro.angle
touch.is_pressed
color.reflected_light_intensity
ultrasonic.distance_centimeters
```

괄호가 없으면 현재 값을 읽는 속성이고, `reset()`, `calibrate()`처럼 괄호가 있으면 동작을 실행하는 메서드입니다.

## import

```python
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
```

센서 포트는 EV3의 실제 입력 포트와 같습니다.

```text
INPUT_1 → 포트 1
INPUT_2 → 포트 2
INPUT_3 → 포트 3
INPUT_4 → 포트 4
```

## 빠른 API

| 센서 | 종류 | API | 의미 |
|---|---|---|---|
| TouchSensor | 속성 | `is_pressed` | 눌림 여부 |
| TouchSensor | 메서드 | `wait_for_pressed()` | 눌릴 때까지 기다림 |
| TouchSensor | 메서드 | `wait_for_released()` | 놓일 때까지 기다림 |
| TouchSensor | 메서드 | `wait_for_bump()` | 눌렀다 놓을 때까지 기다림 |
| ColorSensor | 속성 | `reflected_light_intensity` | 반사광 0~100 |
| ColorSensor | 속성 | `ambient_light_intensity` | 주변광 0~100 |
| ColorSensor | 속성 | `color` | 감지한 색 번호 |
| ColorSensor | 속성 | `color_name` | 색 이름 |
| ColorSensor | 속성 | `raw` | 원시 RGB 값 |
| ColorSensor | 속성 | `rgb` | 0~255로 보정된 RGB |
| UltrasonicSensor | 속성 | `distance_centimeters` | 거리 cm |
| UltrasonicSensor | 속성 | `distance_inches` | 거리 inch |
| UltrasonicSensor | 속성 | `other_sensor_present` | 다른 초음파 신호 감지 |
| GyroSensor | 속성 | `angle` | 누적 각도 |
| GyroSensor | 속성 | `rate` | 각속도 |
| GyroSensor | 속성 | `angle_and_rate` | 각도와 각속도 |
| GyroSensor | 메서드 | `reset()` | 각도 기준 초기화 |
| GyroSensor | 메서드 | `calibrate()` | 자이로 보정 |

---

# TouchSensor

## 장치 선언

```python
touch = TouchSensor(INPUT_1)
```

## is_pressed

**속성**

현재 버튼이 눌려 있는지 확인합니다.

```python
if touch.is_pressed:
    print("pressed")
```

반환값:

```text
True   눌림
False  눌리지 않음
```

## wait_for_pressed()

**메서드**

센서가 눌릴 때까지 기다립니다.

```python
touch.wait_for_pressed()
```

## wait_for_released()

**메서드**

센서가 놓일 때까지 기다립니다.

```python
touch.wait_for_released()
```

## wait_for_bump()

**메서드**

한 번 눌렸다가 다시 놓일 때까지 기다립니다.

```python
touch.wait_for_bump()
```

비동기 task 안에서는 이런 대기형 메서드보다 `is_pressed`를 반복해서 확인하는 방식이 더 적합할 수 있습니다.

---

# ColorSensor

## 장치 선언

```python
color = ColorSensor(INPUT_2)
```

## reflected_light_intensity

**속성**

반사광의 밝기를 읽습니다.

```python
value = color.reflected_light_intensity
```

범위:

```text
0     매우 어두움
100   매우 밝음
```

라인트레이싱처럼 바닥에서 반사되는 빛을 비교할 때 주로 사용합니다.

## ambient_light_intensity

**속성**

주변 환경의 빛 밝기를 읽습니다.

```python
value = color.ambient_light_intensity
```

범위:

```text
0 ~ 100
```

## color

**속성**

감지한 색을 숫자로 읽습니다.

```python
value = color.color
```

주요 값:

```text
0  No color
1  Black
2  Blue
3  Green
4  Yellow
5  Red
6  White
7  Brown
```

상수를 이용하면 숫자를 외울 필요가 없습니다.

```python
if color.color == ColorSensor.COLOR_RED:
    print("red")
```

## color_name

**속성**

색 이름을 문자열로 읽습니다.

```python
print(color.color_name)
```

## raw

**속성**

센서의 원시 RGB 값을 읽습니다.

```python
red, green, blue = color.raw
```

## rgb

**속성**

원시 RGB 값을 0~255 범위로 보정한 값을 읽습니다.

```python
red, green, blue = color.rgb
```

## calibrate_white()

**메서드**

현재 흰색 표면을 기준으로 RGB 보정을 설정합니다.

```python
color.calibrate_white()
```

---

# UltrasonicSensor

## 장치 선언

```python
ultrasonic = UltrasonicSensor(INPUT_3)
```

## distance_centimeters

**속성**

현재 거리를 cm 단위로 읽습니다.

```python
distance = ultrasonic.distance_centimeters
```

## distance_inches

**속성**

현재 거리를 inch 단위로 읽습니다.

```python
distance = ultrasonic.distance_inches
```

## distance_centimeters_ping

**속성**

single-shot 방식으로 한 번 측정합니다.

```python
distance = ultrasonic.distance_centimeters_ping
```

single-shot ping을 매우 빠르게 반복하면 센서 동작이 불안정할 수 있으므로 연속 제어에서는 일반 `distance_centimeters`를 우선 사용하는 편이 단순합니다.

## other_sensor_present

**속성**

다른 초음파 센서의 신호가 감지되는지 확인합니다.

```python
if ultrasonic.other_sensor_present:
    print("another ultrasonic signal")
```

---

# GyroSensor

## 장치 선언

```python
gyro = GyroSensor(INPUT_4)
```

## angle

**속성**

현재 누적 회전 각도를 읽습니다.

```python
angle = gyro.angle
```

Pybricks의:

```python
gyro.angle()
```

와 달리 ev3dev2에서는 괄호가 없습니다.

## rate

**속성**

현재 회전 속도를 읽습니다.

```python
rate = gyro.rate
```

일반적으로 각속도를 의미합니다.

## angle_and_rate

**속성**

각도와 각속도를 한 번에 읽습니다.

```python
angle, rate = gyro.angle_and_rate
```

## reset()

**메서드**

현재 방향을 기준으로 각도 값을 다시 초기화합니다.

```python
gyro.reset()
```

## calibrate()

**메서드**

자이로 센서를 보정합니다.

```python
gyro.calibrate()
```

보정하는 동안에는 로봇과 센서를 움직이지 않는 것이 중요합니다.

---

## async 안에서 센서 읽기

센서의 속성값을 짧은 주기로 읽을 때는 다음처럼 사용할 수 있습니다.

```python
async def sensor_task():
    while True:
        angle = gyro.angle
        distance = ultrasonic.distance_centimeters

        # 학생이 원하는 판단 코드 작성

        await asyncio.sleep(0.02)
```

센서 알고리즘 자체는 학생이 로봇에 맞게 작성합니다.

## 공식 문서

https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html
