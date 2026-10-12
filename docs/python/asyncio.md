# asyncio와 로봇 기능 나누기

`async`, `await`, `asyncio`는 EV3 전용 기능이 아니라 **Python 3 표준 비동기 기능**입니다.

EV3에서 여러 기능을 한 프로그램 안에서 자주 확인해야 할 때 사용할 수 있습니다.

## 먼저 알아둘 용어

| 용어 | 뜻 |
|---|---|
| `async def` | 비동기 함수를 정의 |
| coroutine | `async def`로 만든 함수가 실행을 기다리는 객체 |
| `await` | 현재 coroutine이 잠시 실행권을 양보 |
| event loop | 실행할 coroutine들을 번갈아 관리 |
| `asyncio.gather()` | 여러 coroutine을 함께 실행 |
| `asyncio.sleep()` | 다른 coroutine이 실행될 수 있게 기다림 |

## 일반 함수와 async 함수

일반 함수:

```python
def read_sensor():
    print("sensor")
```

비동기 함수:

```python
async def read_sensor():
    print("sensor")
    await asyncio.sleep(0.02)
```

`async def`를 사용했다고 해서 함수가 자동으로 동시에 실행되는 것은 아닙니다.

예를 들어:

```python
result = read_sensor()
```

라고 하면 async 함수의 본문을 바로 끝까지 실행하는 것이 아니라 **coroutine 객체**가 만들어집니다.

실제로 실행하려면 event loop 안에서 `await`하거나 `gather()` 등에 전달해야 합니다.

## await

`await`는 **현재 async 함수가 잠깐 실행권을 넘기는 지점**입니다.

```python
await asyncio.sleep(0.02)
```

이 순간 event loop는 다른 coroutine을 실행할 수 있습니다.

중요:

```text
async 함수가 여러 개 있다고 자동으로 번갈아 실행되는 것이 아님
→ 각 함수가 await를 만나야 다른 coroutine이 실행될 기회가 생김
```

## asyncio.sleep()과 time.sleep()의 차이

일반 Python 코드:

```python
from time import sleep

sleep(1)
```

`sleep(1)` 동안 현재 Python 실행이 멈춥니다.

async 함수에서는:

```python
await asyncio.sleep(1)
```

을 사용하면 현재 coroutine만 기다리고, event loop는 다른 coroutine을 실행할 수 있습니다.

따라서 여러 로봇 기능을 async로 나눴다면 긴 `time.sleep()`을 async 함수 안에 넣지 않는 것이 중요합니다.

## asyncio.gather()

여러 coroutine을 같은 event loop에서 함께 실행합니다.

```python
async def drive_task():
    while True:
        # 주행 관련 처리
        await asyncio.sleep(0.02)


async def shooter_task():
    while True:
        # 슈터 관련 처리
        await asyncio.sleep(0.02)


async def main():
    await asyncio.gather(
        drive_task(),
        shooter_task(),
    )
```

개념적으로는:

```text
drive_task 실행
   ↓ await
shooter_task 실행
   ↓ await
drive_task 실행
   ↓ await
...
```

처럼 각 coroutine이 `await`에서 양보할 때 event loop가 다른 coroutine을 실행합니다.

이것은 여러 CPU 코어에서 실제로 동시에 계산하는 병렬 처리와는 다릅니다.

## EV3에서 main 실행

수업에서는 구형 Python 3 환경과도 넓게 호환되도록 다음 형태를 기본으로 사용합니다.

```python
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())

finally:
    loop.close()
```

흐름:

```text
asyncio.get_event_loop()
→ event loop 가져오기

loop.run_until_complete(main())
→ main coroutine 실행

loop.close()
→ 프로그램 종료 시 event loop 닫기
```

## 로봇 기능을 나누는 기준

`모터 하나 = task 하나`로 정할 필요는 없습니다.

학생이 서로 독립적으로 관리하고 싶은 기능을 기준으로 나눕니다.

예:

```text
주행
공 처리
속도 모드
센서 감시
상태 표시
```

어떤 기능을 따로 나눌지는 로봇 설계와 학생 알고리즘에 따라 달라집니다.

## 값을 계속 읽는 task

Xbox:

```python
async def controller_task():
    while True:
        x, y = controller.joystick_left()
        pressed = controller.buttons.pressed()

        # 학생 코드

        await asyncio.sleep(0.02)
```

센서:

```python
async def sensor_task():
    while True:
        angle = gyro.angle
        distance = ultrasonic.distance_centimeters

        # 학생 코드

        await asyncio.sleep(0.02)
```

`0.02`초는 20 ms입니다.

## 비차단 명령

다음처럼 계속 동작을 시작하고 바로 반환하는 명령은 async 제어와 잘 맞습니다.

```python
motor.on(SpeedPercent(50))
drive.on(0, 50)
```

명령을 내린 뒤 Python 코드는 바로 다음 줄로 진행합니다.

## blocking 명령

반대로 완료될 때까지 기다리는 명령도 있습니다.

```python
motor.on_for_degrees(
    SpeedPercent(50),
    360,
)
```

기본 `block=True`이면 동작이 끝날 때까지 해당 Python 호출이 반환되지 않습니다.

async 함수 안에서 다른 coroutine도 계속 실행되어야 한다면:

```python
motor.on_for_degrees(
    SpeedPercent(50),
    360,
    block=False,
)

while motor.is_running:
    await asyncio.sleep(0.01)
```

처럼 비차단으로 시작한 뒤 상태를 확인하는 방법을 사용할 수 있습니다.

## async와 PLAY_NO_WAIT_FOR_COMPLETE의 차이

둘 다 "기다리지 않는다"는 표현이 나오지만 다른 개념입니다.

```text
PLAY_NO_WAIT_FOR_COMPLETE
→ Sound 메서드가 소리 재생 완료를 기다리지 않고 반환

async / await
→ Python event loop가 여러 coroutine의 실행 순서를 관리
```

예:

```python
sound.beep(
    play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
)

await asyncio.sleep(0.02)
```

첫 번째 줄은 Sound의 재생 방식이고, 두 번째 줄은 Python coroutine의 실행 방식입니다.

## 자주 하는 실수

### 1. async 함수 안에서 time.sleep()

```python
async def task():
    sleep(1)
```

이 시간 동안 다른 coroutine도 실행되지 못합니다.

대신:

```python
async def task():
    await asyncio.sleep(1)
```

을 사용합니다.

### 2. await 없이 무한 반복

```python
async def task():
    while True:
        print("running")
```

이 함수가 실행권을 계속 잡고 있어서 다른 coroutine이 실행되지 못할 수 있습니다.

반복 안에:

```python
await asyncio.sleep(0.02)
```

같은 양보 지점이 필요합니다.

### 3. 일반 함수에서 await 사용

```python
def task():
    await asyncio.sleep(1)
```

은 사용할 수 없습니다.

`await`는 `async def` 안에서 사용합니다.

## 빠른 API

| 하고 싶은 일 | 사용 |
|---|---|
| async 함수 만들기 | `async def function():` |
| 잠시 양보 | `await asyncio.sleep(seconds)` |
| 여러 coroutine 같이 실행 | `await asyncio.gather(...)` |
| event loop 가져오기 | `asyncio.get_event_loop()` |
| main 실행 | `loop.run_until_complete(main())` |
| event loop 종료 | `loop.close()` |

## 공식 문서

Python asyncio:
https://docs.python.org/3/library/asyncio.html
