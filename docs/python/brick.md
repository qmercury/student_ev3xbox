# EV3 Brick

`python-ev3dev2`에서는 Pybricks의 `EV3Brick()`처럼 본체 전체를 하나의 객체로 만들지 않습니다.

필요한 기능을 각각 객체로 만듭니다.

```python
button = Button()
leds = Leds()
sound = Sound()
battery = PowerSupply()
display = Display()
console = Console()
```

## import

```python
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.display import Display
from ev3dev2.console import Console
```

## 빠른 API

| 기능 | 종류 | API |
|---|---|---|
| 현재 누른 EV3 버튼 목록 | 속성 | `button.buttons_pressed` |
| 위 버튼 | 속성 | `button.up` |
| 아래 버튼 | 속성 | `button.down` |
| 왼쪽 버튼 | 속성 | `button.left` |
| 오른쪽 버튼 | 속성 | `button.right` |
| 가운데 버튼 | 속성 | `button.enter` |
| 뒤로 버튼 | 속성 | `button.backspace` |
| 아무 버튼이나 눌렸는지 | 메서드 | `button.any()` |
| LED 색 변경 | 메서드 | `leds.set_color(...)` |
| LED 모두 끄기 | 메서드 | `leds.all_off()` |
| 비프음 | 메서드 | `sound.beep()` |
| 음 재생 | 메서드 | `sound.tone(...)` |
| 음량 읽기 | 메서드 | `sound.get_volume()` |
| 음량 설정 | 메서드 | `sound.set_volume(...)` |
| 배터리 전압 | 속성 | `battery.measured_volts` |
| 배터리 전류 | 속성 | `battery.measured_amps` |
| LCD 지우기 | 메서드 | `display.clear()` |
| LCD 갱신 | 메서드 | `display.update()` |
| LCD 그림 객체 | 속성 | `display.draw` |
| 콘솔 글자 출력 | 메서드 | `console.text_at(...)` |
| 콘솔 열 수 | 속성 | `console.columns` |
| 콘솔 행 수 | 속성 | `console.rows` |

---

# Button

## 장치 선언

```python
button = Button()
```

## buttons_pressed

**속성**

현재 눌려 있는 버튼 이름들의 리스트를 반환합니다.

```python
pressed = button.buttons_pressed
print(pressed)
```

예:

```text
["up", "enter"]
```

## up / down / left / right / enter / backspace

**속성**

각 버튼의 현재 눌림 상태를 `True` 또는 `False`로 읽습니다.

```python
if button.up:
    print("up")

if button.enter:
    print("enter")
```

## any()

**메서드**

EV3 본체 버튼 중 하나라도 눌려 있는지 확인합니다.

```python
if button.any():
    print("button pressed")
```

## check_buttons(buttons)

**메서드**

현재 눌린 버튼이 지정한 버튼 목록과 정확히 같은지 확인합니다.

```python
if button.check_buttons(["up", "enter"]):
    print("up + enter")
```

## wait_for_pressed() / wait_for_released() / wait_for_bump()

**메서드**

버튼 입력을 기다리는 메서드입니다.

```python
button.wait_for_pressed(["enter"])
button.wait_for_released(["enter"])
button.wait_for_bump(["enter"])
```

`async` task 안에서는 이런 대기형 메서드보다 `button.enter` 같은 속성을 반복해서 확인하는 방식이 더 적합한 경우가 많습니다.

---

# Leds

## 장치 선언

```python
leds = Leds()
```

## set_color(group, color)

**메서드**

EV3 상태 LED의 색을 설정합니다.

```python
leds.set_color("LEFT", "GREEN")
leds.set_color("RIGHT", "GREEN")
```

EV3에서 주로 사용하는 그룹:

```text
LEFT
RIGHT
```

색상 예:

```text
BLACK
RED
GREEN
YELLOW
AMBER
ORANGE
```

사용 가능한 LED 색상은 플랫폼 설정에 따라 달라질 수 있습니다.

## all_off()

**메서드**

모든 상태 LED를 끕니다.

```python
leds.all_off()
```

## reset()

**메서드**

LED를 기본 상태로 되돌립니다.

```python
leds.reset()
```

---

# Sound

## 장치 선언

```python
sound = Sound()
```

## beep()

**메서드**

간단한 비프음을 냅니다.

```python
sound.beep()
```

## tone()

**메서드**

주파수와 시간을 이용해 음을 재생합니다.

한 음:

```python
sound.tone(
    1000,
    300,
)
```

`tone()`에서 이 형태의 duration은 밀리초 단위입니다.

여러 음:

```python
sound.tone([
    (440, 300, 100),
    (660, 300, 100),
])
```

각 튜플은:

```text
(주파수 Hz, 재생시간 ms, 다음 음까지 지연 ms)
```

입니다.

## play_tone()

**메서드**

주파수, 재생시간, 음량 등을 더 명시적으로 지정할 수 있습니다.

```python
sound.play_tone(
    440,
    0.5,
    volume=50,
)
```

`play_tone()`의 duration은 초 단위입니다.

## play_file()

**메서드**

WAV 파일을 재생합니다.

```python
sound.play_file(
    "/home/robot/sound.wav"
)
```

## speak()

**메서드**

텍스트를 음성으로 읽습니다.

```python
sound.speak(
    "Hello"
)
```

## get_volume()

**메서드**

현재 음량을 읽습니다.

```python
volume = sound.get_volume()
```

## set_volume(volume)

**메서드**

음량을 0~100 범위로 설정합니다.

```python
sound.set_volume(50)
```

## blocking 주의

Sound 메서드는 `play_type`에 따라 재생이 끝날 때까지 기다리거나 바로 다음 코드로 넘어가도록 선택할 수 있습니다.

```python
sound.beep(
    play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
)
```

로봇 제어용 `async` task 안에서는 긴 소리가 전체 제어를 막지 않도록 주의합니다.

---

# PowerSupply

## 장치 선언

```python
battery = PowerSupply()
```

## measured_volts

**속성**

현재 배터리 전압을 V 단위로 읽습니다.

```python
voltage = battery.measured_volts
```

## measured_amps

**속성**

현재 배터리 전류를 A 단위로 읽습니다.

```python
current = battery.measured_amps
```

원시 단위가 필요하면:

```python
battery.measured_voltage
battery.measured_current
```

도 사용할 수 있습니다. 각각 microvolts, microamps 단위입니다.

---

# Display

## 장치 선언

```python
display = Display()
```

`Display`는 EV3 LCD를 PIL 방식으로 그리는 기능입니다.

## clear()

**메서드**

화면 내용을 지웁니다.

```python
display.clear()
```

## draw

**속성**

PIL의 `ImageDraw` 객체를 가져옵니다.

```python
display.draw.rectangle(
    (10, 10, 80, 40),
    fill="black",
)
```

## update()

**메서드**

그린 내용을 실제 EV3 LCD에 표시합니다.

```python
display.update()
```

중요: `draw`로 그리기만 해서는 화면에 나타나지 않고 마지막에 `update()`를 호출해야 합니다.

## xres / yres

**속성**

화면 해상도를 읽습니다.

```python
print(display.xres)
print(display.yres)
```

---

# Console

## 장치 선언

```python
console = Console()
```

`Console`은 EV3 LCD에 텍스트를 행/열 기준으로 표시할 때 편합니다.

## text_at(text, column=1, row=1, ...)

**메서드**

지정한 위치에 글자를 표시합니다.

```python
console.text_at(
    "READY",
    column=1,
    row=1,
    reset_console=True,
)
```

행과 열은 0이 아니라 **1부터 시작**합니다.

## columns / rows

**속성**

현재 폰트로 화면에 표시할 수 있는 열과 행 수를 읽습니다.

```python
print(console.columns)
print(console.rows)
```

폰트 크기에 따라 열과 행 수가 달라집니다.

---

## Pybricks와 비교

Pybricks에서는:

```python
ev3 = EV3Brick()

ev3.buttons
ev3.light
ev3.speaker
```

처럼 하나의 `EV3Brick` 객체 아래에 본체 기능이 모여 있습니다.

ev3dev2에서는:

```python
button = Button()
leds = Leds()
sound = Sound()
battery = PowerSupply()
```

처럼 필요한 기능을 각각 만듭니다.

## 공식 문서

- Button: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/button.html
- Leds: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/leds.html
- Sound: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sound.html
- PowerSupply: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/power-supply.html
- Display: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/display.html
- Console: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/console.html
