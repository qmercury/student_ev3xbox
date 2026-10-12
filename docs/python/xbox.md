# XboxController

Xbox 입력은 `python-ev3dev2` 기능이 아니라 이 프로젝트의 `ev3xbox` 라이브러리입니다.

학생 코드는 네트워크 통신을 직접 작성하지 않습니다.

```text
Xbox Controller
      ↓ Bluetooth
교사용 컴퓨터 EV3 Xbox Relay
      ↓ UDP
EV3 xbox_service.py
      ↓ localhost
학생 프로그램
      ↓
ev3xbox.XboxController
```

## import

```python
from ev3xbox import XboxButton, XboxController
```

## 장치 선언

```python
controller = XboxController()
```

프로그램이 끝날 때는:

```python
controller.close()
```

를 호출합니다.

## 빠른 API

| 종류 | 기능 | API | 반환 |
|---|---|---|---|
| 클래스 | 컨트롤러 만들기 | `XboxController()` | 객체 |
| 속성 | 버튼 인터페이스 | `controller.buttons` | 버튼 객체 |
| 메서드 | 현재 누른 버튼 | `controller.buttons.pressed()` | `set` |
| 메서드 | 왼쪽 스틱 | `controller.joystick_left()` | `(x, y)` |
| 메서드 | 오른쪽 스틱 | `controller.joystick_right()` | `(x, y)` |
| 메서드 | LT / RT | `controller.triggers()` | `(lt, rt)` |
| 메서드 | 연결 상태 | `controller.connected()` | `True / False` |
| 메서드 | 연결될 때까지 대기 | `controller.wait_until_connected()` | `True / False` |
| 메서드 | 종료 | `controller.close()` | 없음 |

---

# 스틱

## joystick_left()

**메서드**

왼쪽 스틱의 현재 위치를 `(x, y)`로 반환합니다.

```python
x, y = controller.joystick_left()
```

범위:

```text
x = -100 ~ 100
y = -100 ~ 100
```

방향:

```text
x < 0    왼쪽
x > 0    오른쪽

y > 0    위
y < 0    아래
```

중앙:

```text
x = 0
y = 0
```

예:

```python
x, y = controller.joystick_left()

print(x)
print(y)
```

## joystick_right()

**메서드**

오른쪽 스틱의 현재 위치를 같은 방식으로 반환합니다.

```python
x, y = controller.joystick_right()
```

범위와 방향은 왼쪽 스틱과 같습니다.

## MoveJoystick과 연결

`MoveJoystick.on(x, y)`도 x/y 값을 받기 때문에 그대로 연결할 수 있습니다.

```python
x, y = controller.joystick_left()

drive.on(
    x,
    y,
)
```

속도 제한, 감도 변경, 데드존 추가 같은 처리는 학생이 자신의 주행 알고리즘에 맞게 작성합니다.

---

# 트리거

## triggers()

**메서드**

LT와 RT의 현재 눌림 정도를 반환합니다.

```python
lt, rt = controller.triggers()
```

범위:

```text
0      누르지 않음
100    완전히 누름
```

중간값도 사용할 수 있습니다.

예:

```python
lt, rt = controller.triggers()

if rt > 50:
    print("RT가 절반 이상 눌림")
```

트리거를 단순 버튼처럼 쓰고 싶으면 임계값을 정하면 됩니다.

```python
if rt > 20:
    print("RT pressed")
```

임계값은 정답이 있는 값이 아니라 학생이 원하는 조작감에 맞게 정할 수 있습니다.

---

# 버튼

## controller.buttons

**속성**

Xbox 버튼 기능에 접근하는 객체입니다.

현재 버튼을 읽으려면:

```python
pressed = controller.buttons.pressed()
```

## buttons.pressed()

**메서드**

현재 눌려 있는 버튼들을 `set`으로 반환합니다.

예를 들어 A와 RB가 동시에 눌려 있으면 개념적으로:

```text
{A, RB}
```

와 같은 집합을 얻습니다.

## 지원 버튼

현재 `ev3xbox`에서 학생 코드에 공개하는 버튼은 다음과 같습니다.

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

D-pad도 버튼과 같은 방식으로 사용합니다.

## 버튼이 현재 눌려 있는지 확인

```python
pressed = controller.buttons.pressed()

if XboxButton.A in pressed:
    print("A")
```

한 줄로도 가능합니다.

```python
if XboxButton.A in controller.buttons.pressed():
    print("A")
```

---

# 눌린 순간과 놓인 순간

`buttons.pressed()`는 **현재 상태**를 알려줍니다.

버튼이 방금 눌렸는지 또는 방금 놓였는지는 이전 상태와 비교해서 만들 수 있습니다.

```python
previous = set()

current = controller.buttons.pressed()

just_pressed = current - previous
just_released = previous - current

previous = current
```

## 방금 눌린 버튼

```python
if XboxButton.A in just_pressed:
    print("A pressed")
```

## 방금 놓인 버튼

```python
if XboxButton.A in just_released:
    print("A released")
```

## 누르는 동안 계속 동작

현재 상태만 보면 됩니다.

```python
if XboxButton.A in controller.buttons.pressed():
    motor.on(
        SpeedPercent(100)
    )
else:
    motor.off(
        brake=True
    )
```

## 한 번 눌렀을 때 한 번만 실행

`just_pressed`를 사용합니다.

```python
if XboxButton.RB in just_pressed:
    speed = speed + 10
```

이렇게 하면 RB를 계속 누르고 있어도 반복해서 증가하지 않고 눌린 순간에 한 번만 처리할 수 있습니다.

---

# 연결 상태

## connected()

**메서드**

교사용 Relay에서 유효한 Xbox 상태가 현재 EV3까지 전달되고 있는지 확인합니다.

```python
if controller.connected():
    print("connected")
```

반환:

```text
True     연결 상태
False    연결되지 않은 상태
```

## wait_until_connected(timeout=None, poll=0.05)

**메서드**

연결될 때까지 기다립니다.

계속 기다리기:

```python
controller.wait_until_connected()
```

최대 3초 기다리기:

```python
ok = controller.wait_until_connected(
    timeout=3
)
```

3초 안에 연결되면 `True`, 그렇지 않으면 `False`입니다.

`poll`은 연결 상태를 다시 확인하는 간격이며 기본값은 0.05초입니다.

### async에서 주의

`wait_until_connected()`는 내부적으로 일반적인 대기 방식으로 동작하므로 실행 중인 async 제어 task 안에서 반복 사용하지 않는 것이 좋습니다.

async 코드에서는 보통:

```python
while not controller.connected():
    await asyncio.sleep(0.05)
```

처럼 확인하면 다른 task도 계속 실행할 수 있습니다.

---

# async에서 Xbox 읽기

Xbox의 스틱, 버튼, 트리거를 읽는 메서드는 값을 바로 반환하므로 async task 안에서도 간단히 사용할 수 있습니다.

```python
async def controller_task():
    while True:
        x, y = controller.joystick_left()
        pressed = controller.buttons.pressed()
        lt, rt = controller.triggers()

        # 학생이 원하는 동작 작성

        await asyncio.sleep(0.02)
```

`asyncio`의 구조 자체는 학생이 로봇 기능에 맞게 설계합니다.

---

# 종료

## close()

**메서드**

학생 프로그램이 사용하는 Xbox 수신 소켓을 닫습니다.

```python
controller.close()
```

프로그램 종료 처리에서 호출하면 됩니다.

예:

```python
try:
    # 학생 코드
    pass

finally:
    controller.close()
```

---

## 정리

```text
왼쪽 스틱         controller.joystick_left()
오른쪽 스틱       controller.joystick_right()
트리거             controller.triggers()
현재 버튼          controller.buttons.pressed()
연결 상태          controller.connected()
종료               controller.close()
```

Xbox 부분만 우리 프로젝트가 제공하는 API입니다.

```text
Motor / Drive / Sensor / EV3 Brick
→ python-ev3dev2

async / await / asyncio
→ Python 3

XboxController / XboxButton
→ ev3xbox
```
