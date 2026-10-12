# 속성과 메서드

`ev3dev2`를 볼 때 가장 먼저 구분하면 좋은 것은 **속성(property)** 과 **메서드(method)** 입니다.

## 가장 간단한 구분

```text
속성
현재 값이나 상태를 읽음
괄호 없음

메서드
어떤 동작을 실행함
괄호 있음
```

예:

```python
motor.position
gyro.angle
touch.is_pressed
```

위 세 개는 속성입니다.

```python
motor.on(...)
motor.off(...)
gyro.reset()
```

위 세 개는 메서드입니다.

## Pybricks와 다른 점

Pybricks에서는 현재 값을 읽는 기능도 메서드 형태인 경우가 많습니다.

```python
# Pybricks
motor.angle()
motor.speed()
gyro.angle()
touch.pressed()
```

ev3dev2에서는 같은 종류의 값이 속성인 경우가 많습니다.

```python
# ev3dev2
motor.position
motor.speed
gyro.angle
touch.is_pressed
```

그래서 Pybricks에 익숙하면 실수로:

```python
gyro.angle()
```

이라고 쓰기 쉽습니다.

ev3dev2에서는:

```python
gyro.angle
```

입니다.

## 값이라고 항상 속성인 것은 아님

라이브러리가 어떻게 설계되었는지에 따라 값 확인도 메서드일 수 있습니다.

우리 Xbox 라이브러리는:

```python
controller.connected()
controller.joystick_left()
controller.triggers()
```

처럼 메서드 형태입니다.

따라서 문서에서 `()`가 있는지 확인하는 습관이 중요합니다.

## 문서에서 표시하는 방법

이 레퍼런스에서는 다음처럼 표시합니다.

```text
[속성] motor.position
[속성] gyro.angle
[메서드] motor.on(...)
[메서드] gyro.reset()
```
