# 학생용 비동기 프로그램 구조 한 장 정리

이 문서는 완성된 로봇 알고리즘이 아니라 **프로그램의 뼈대**만 보여주는 참고 문서입니다.

학생은 장치 구성, 버튼 역할, 주행 방식, 슈터 동작, 속도 변경 방법을 직접 설계합니다.

## 전체 구조

```python
import asyncio

from ev3dev2.motor import MediumMotor, MoveJoystick, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3xbox import XboxController


# 1. 장치 선언
drive = MoveJoystick(OUTPUT_A, OUTPUT_D)
shooter = MediumMotor(OUTPUT_B)
controller = XboxController()


# 2. 기능별 async 함수
async def drive_task():
    while True:
        # 학생이 주행 알고리즘 작성

        await asyncio.sleep(0.02)


async def shooter_task():
    while True:
        # 학생이 슈터 알고리즘 작성

        await asyncio.sleep(0.02)


# 3. 여러 기능 함께 실행
async def main():
    await asyncio.gather(
        drive_task(),
        shooter_task(),
    )


# 4. main 실행
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())

finally:
    # 5. 프로그램이 끝날 때 안전 정리
    drive.off(brake=True)
    shooter.off(brake=True)
    controller.close()
    loop.close()
```

## 순서로 보면

```text
import
  ↓
장치 선언
  ↓
async 기능 함수 작성
  ↓
main()에서 gather
  ↓
event loop로 main 실행
  ↓
finally에서 안전 정리
```

---

## 1. import

필요한 기능을 불러옵니다.

```python
import asyncio

from ev3dev2.motor import MediumMotor, MoveJoystick, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3xbox import XboxController
```

Xbox 버튼 이름이 필요하면:

```python
from ev3xbox import XboxButton, XboxController
```

처럼 `XboxButton`도 불러옵니다.

---

## 2. 장치 선언

실제로 사용할 장치를 객체로 만듭니다.

```python
drive = MoveJoystick(OUTPUT_A, OUTPUT_D)
shooter = MediumMotor(OUTPUT_B)
controller = XboxController()
```

이 부분은 로봇에 따라 달라집니다.

학생은 자기 로봇의:

```text
모터 종류
모터 포트
센서 종류
센서 포트
주행 클래스
```

를 직접 정합니다.

---

## 3. 기능별 async 함수

서로 독립적으로 계속 확인해야 하는 기능을 나눌 수 있습니다.

```python
async def drive_task():
    while True:
        # 주행 관련 코드

        await asyncio.sleep(0.02)
```

```python
async def shooter_task():
    while True:
        # 슈터 관련 코드

        await asyncio.sleep(0.02)
```

중요한 것은 함수 이름이 아니라 **기능을 어떻게 나눌지 학생이 결정하는 것**입니다.

예:

```text
drive_task()
shooter_task()
sensor_task()
speed_task()
display_task()
```

모든 로봇에 이 다섯 개가 필요한 것은 아닙니다.

---

## 4. main()과 asyncio.gather()

여러 async 기능을 같이 실행합니다.

```python
async def main():
    await asyncio.gather(
        drive_task(),
        shooter_task(),
    )
```

Pybricks에서 익숙한 구조와 비교하면:

```text
Pybricks
await multitask(...)

Python asyncio
await asyncio.gather(...)
```

역할이 비슷합니다.

---

## 5. event loop로 main 실행

```python
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())
```

Pybricks의:

```python
run_task(main())
```

와 대응되는 부분이라고 생각하면 이해하기 쉽습니다.

```text
Pybricks
run_task(main())

Python asyncio
loop.run_until_complete(main())
```

Pybricks는 실행 환경을 라이브러리가 감싸주고, 일반 Python에서는 event loop를 직접 다룹니다.

---

## 6. finally에서 안전 정리

```python
finally:
    drive.off(brake=True)
    shooter.off(brake=True)
    controller.close()
    loop.close()
```

역할:

```text
drive.off()
→ 주행 모터 정지

shooter.off()
→ 슈터 모터 정지

controller.close()
→ 학생 프로그램의 Xbox 수신 종료

loop.close()
→ asyncio event loop 종료
```

학생이 기능을 더 추가했다면 그 장치에 필요한 정리 코드도 추가할 수 있습니다.

---

## 7. 각 task 안에서는 await를 잊지 않기

잘못된 예:

```python
async def drive_task():
    while True:
        # 계속 실행
        pass
```

이렇게 하면 다른 task가 실행될 기회를 얻지 못할 수 있습니다.

기본 형태:

```python
async def drive_task():
    while True:
        # 학생 코드

        await asyncio.sleep(0.02)
```

입니다.

---

## Pybricks를 배운 학생이 기억할 대응 관계

| Pybricks | ev3dev + Python 3 |
|---|---|
| `async def` | `async def` |
| `await` | `await` |
| `multitask(...)` | `asyncio.gather(...)` |
| `run_task(main())` | `loop.run_until_complete(main())` |
| Pybricks runtime | Python `asyncio` event loop |

핵심 비동기 개념은 같습니다. 실행을 도와주는 라이브러리가 다릅니다.

---

## 학생이 직접 결정하는 부분

이 예제는 아래 내용을 정해주지 않습니다.

```text
어떤 스틱으로 주행할지
어떤 버튼으로 슈터를 작동할지
속도를 어떻게 계산할지
모터 방향을 어떻게 할지
센서를 어떻게 사용할지
task를 몇 개 만들지
```

이 부분이 학생의 로봇 알고리즘입니다.
