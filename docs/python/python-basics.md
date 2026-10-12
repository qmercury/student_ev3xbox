# Python 기본

EV3 코드는 MicroPython이 아니라 ev3dev Linux에서 실행되는 **일반 Python 3**입니다.

따라서 Python 문법은 PC에서 사용하는 Python과 같습니다. EV3 전용인 것은 `python-ev3dev2`와 이 프로젝트의 `ev3xbox` API입니다.

## 빠른 찾기

| 하고 싶은 일 | Python 문법 |
|---|---|
| 값 저장 | `speed = 50` |
| 조건 판단 | `if` / `elif` / `else` |
| 계속 반복 | `while` |
| 정해진 횟수 반복 | `for` |
| 기능 묶기 | `def` |
| 값 돌려주기 | `return` |
| 여러 값 저장 | `list`, `tuple`, `dict`, `set` |
| 포함 여부 확인 | `in` |
| 전역 변수 변경 | `global` |
| 종료 시 정리 | `try` / `finally` |
| 잠시 기다리기 | `time.sleep()` |
| async에서 기다리기 | `await asyncio.sleep()` |

---

# 변수

값에 이름을 붙입니다.

```python
speed = 30
distance = 500
name = "robot"
enabled = True
```

Python에서는 변수의 자료형을 앞에 적지 않습니다.

```text
30          int
30.5        float
"robot"     str
True        bool
```

## 값 변경

```python
speed = 30
speed = 50
```

기존 값을 이용해 변경할 수도 있습니다.

```python
speed = speed + 10
```

축약하면:

```python
speed += 10
speed -= 10
```

---

# 비교 연산자

조건문에서 많이 사용합니다.

```text
==   같다
!=   다르다
>    크다
<    작다
>=   크거나 같다
<=   작거나 같다
```

예:

```python
if speed >= 50:
    print("fast")
```

중요:

```python
speed = 50
```

의 `=`는 **값을 저장**하는 기호이고,

```python
speed == 50
```

의 `==`는 **같은지 비교**하는 기호입니다.

---

# 논리 연산자

여러 조건을 조합할 수 있습니다.

```text
and   둘 다 참
or    하나라도 참
not   참/거짓 반전
```

예:

```python
if speed > 20 and speed < 80:
    print("normal")
```

```python
if not controller.connected():
    print("disconnected")
```

---

# if / elif / else

조건에 따라 다른 코드를 실행합니다.

```python
if speed > 70:
    print("fast")

elif speed > 30:
    print("normal")

else:
    print("slow")
```

Python에서는 들여쓰기가 문법의 일부입니다.

```python
if speed > 50:
    print("inside")

print("outside")
```

---

# while

조건이 참인 동안 반복합니다.

```python
while True:
    print("running")
```

센서나 Xbox 상태를 계속 읽는 로봇 프로그램에서 자주 사용합니다.

일반 동기 코드에서는:

```python
from time import sleep

while True:
    x, y = controller.joystick_left()

    print(x, y)

    sleep(0.02)
```

처럼 짧게 기다려 CPU를 계속 점유하지 않도록 할 수 있습니다.

## break

반복문을 끝냅니다.

```python
while True:
    if button.enter:
        break
```

## continue

현재 반복의 남은 코드를 건너뛰고 다음 반복으로 갑니다.

```python
while True:
    if not controller.connected():
        continue

    print("connected")
```

실제 제어 루프에서는 `continue` 전에 필요한 대기나 안전 처리를 빼먹지 않도록 주의합니다.

---

# for

정해진 횟수 또는 여러 항목을 차례로 처리합니다.

```python
for number in range(5):
    print(number)
```

출력:

```text
0
1
2
3
4
```

리스트도 반복할 수 있습니다.

```python
speeds = [20, 40, 60]

for speed in speeds:
    print(speed)
```

---

# 함수

반복해서 사용할 동작을 하나의 이름으로 묶습니다.

```python
def stop_robot():
    drive.off(brake=True)
```

호출:

```python
stop_robot()
```

## 매개변수

함수에 값을 전달할 수 있습니다.

```python
def set_speed(speed):
    motor.on(
        SpeedPercent(speed)
    )
```

호출:

```python
set_speed(50)
```

## return

함수가 계산한 값을 돌려줍니다.

```python
def double(value):
    return value * 2

speed = double(30)
```

이제 `speed`는 `60`입니다.

여러 값을 동시에 돌려줄 수도 있습니다.

```python
def read_stick():
    x, y = controller.joystick_left()
    return x, y
```

---

# list

순서가 있는 여러 값을 저장합니다.

```python
speeds = [20, 40, 60]
```

값 읽기:

```python
print(speeds[0])
```

Python의 위치 번호는 0부터 시작합니다.

추가:

```python
speeds.append(80)
```

---

# tuple

순서가 있는 여러 값을 묶습니다.

Xbox 스틱처럼 두 값을 한 번에 반환할 때 자주 볼 수 있습니다.

```python
x, y = controller.joystick_left()
```

개념적으로 반환값은:

```python
(x, y)
```

형태의 tuple입니다.

트리거도 같습니다.

```python
lt, rt = controller.triggers()
```

---

# set

**중복되지 않는 값들의 집합**입니다.

Xbox 버튼 처리에서 특히 중요합니다.

```python
pressed = controller.buttons.pressed()
```

`pressed`는 set입니다.

버튼 포함 여부:

```python
if XboxButton.A in pressed:
    print("A")
```

## set 빼기

이전 상태와 현재 상태의 차이를 구할 수 있습니다.

```python
previous = set()
current = controller.buttons.pressed()

just_pressed = current - previous
just_released = previous - current
```

의미:

```text
current - previous
→ 이번에 새로 생긴 버튼
→ 방금 눌린 버튼

previous - current
→ 이전에는 있었는데 지금은 없는 버튼
→ 방금 놓인 버튼
```

이 때문에 Xbox 버튼 이벤트 처리에서 set이 유용합니다.

---

# dict

이름과 값을 짝으로 저장합니다.

```python
robot = {
    "speed": 30,
    "wheel": 88,
}
```

값 읽기:

```python
print(robot["speed"])
```

값 변경:

```python
robot["speed"] = 50
```

---

# in

어떤 값이 들어 있는지 확인합니다.

리스트:

```python
if 50 in speeds:
    print("found")
```

set:

```python
if XboxButton.A in pressed:
    print("A")
```

로봇 코드에서는 버튼 집합을 확인할 때 자주 사용합니다.

---

# min() / max()

값이 정해진 범위를 넘지 않도록 제한할 때 편리합니다.

```python
speed = min(100, speed + 10)
```

속도를 올려도 최대 100을 넘지 않습니다.

```python
speed = max(20, speed - 10)
```

속도를 내려도 최소 20보다 작아지지 않습니다.

둘을 함께 쓰면:

```python
speed = max(
    0,
    min(100, speed)
)
```

처럼 범위를 제한할 수 있습니다.

---

# global

함수 밖에서 만든 변수를 함수 안에서 **변경**하려면 `global`이 필요할 수 있습니다.

```python
drive_speed = 50


def increase_speed():
    global drive_speed

    drive_speed += 10
```

읽기만 하는 경우에는 보통 `global`이 필요하지 않습니다.

```python
drive_speed = 50


def show_speed():
    print(drive_speed)
```

`global`을 너무 많이 사용하면 코드 관계를 파악하기 어려워질 수 있으므로 필요한 경우에만 사용합니다.

---

# try / finally

로봇 프로그램에서는 **프로그램이 끝날 때 반드시 실행해야 하는 정리 코드**에 중요합니다.

```python
try:
    while True:
        # robot code
        pass

finally:
    drive.off(brake=True)
    controller.close()
```

중간에 오류가 발생하더라도 `finally` 부분은 정리 작업을 위해 실행됩니다.

모터 정지나 Xbox 수신 종료 같은 코드에 적합합니다.

---

# try / except

오류를 직접 처리하고 싶을 때 사용합니다.

```python
try:
    value = int(text)

except ValueError:
    print("number required")
```

처음부터 모든 오류를 `except Exception:`으로 숨기기보다는 어떤 오류를 처리하는지 명확하게 작성하는 것이 좋습니다.

---

# import

다른 모듈의 기능을 불러옵니다.

모듈 전체:

```python
import asyncio
```

필요한 클래스 하나:

```python
from ev3dev2.motor import LargeMotor
```

여러 개:

```python
from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent
```

Xbox:

```python
from ev3xbox import XboxButton, XboxController
```

조이스틱만 사용하고 버튼 이름은 사용하지 않는다면:

```python
from ev3xbox import XboxController
```

만 import해도 됩니다.

---

# sleep

일반 동기 코드:

```python
from time import sleep

sleep(1)
```

단위는 초입니다.

```python
sleep(0.02)
```

는 20 ms입니다.

async 함수 안에서는 일반 `sleep()` 대신:

```python
await asyncio.sleep(0.02)
```

를 사용합니다.

---

# async / await

로봇의 여러 독립 기능을 같은 프로그램에서 관리할 때 사용할 수 있습니다.

```python
async def drive_task():
    while True:
        # student code

        await asyncio.sleep(0.02)
```

`async def`는 비동기 함수를 정의합니다.

호출하면 coroutine 객체가 만들어지고, event loop 안에서 `await` 또는 `asyncio.gather()` 등을 통해 실행됩니다.

```python
async def main():
    await asyncio.gather(
        drive_task(),
        shooter_task(),
    )
```

EV3 수업에서는 다음 실행 형태를 기본으로 사용합니다.

```python
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())

finally:
    loop.close()
```

자세한 내용은 [asyncio 로봇 기능 나누기](asyncio.md)를 봅니다.

---

## 수업에서 우선 익힐 Python 문법

처음부터 Python 전체 문법을 외울 필요는 없습니다.

로봇 수업에서는 우선:

```text
변수
if / elif / else
while
함수
return
list / tuple
set
in
try / finally
async / await
```

정도를 이해하면 모터, 센서, Xbox API를 조합해서 상당히 많은 프로그램을 만들 수 있습니다.

학생은 완성된 알고리즘을 외우기보다 필요한 문법과 API를 찾아 조합합니다.

## 공식 문서

Python 3 Tutorial:
https://docs.python.org/3/tutorial/
