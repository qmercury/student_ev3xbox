from typing import Optional, Tuple

class TouchSensor:
    is_pressed: bool
    def __init__(self, address: str = ..., **kwargs) -> None: ...
    def wait_for_pressed(self, timeout_ms: Optional[int] = ..., sleep_ms: int = ...) -> bool: ...
    def wait_for_released(self, timeout_ms: Optional[int] = ..., sleep_ms: int = ...) -> bool: ...
    def wait_for_bump(self, timeout_ms: Optional[int] = ..., sleep_ms: int = ...) -> bool: ...

class ColorSensor:
    COLOR_NOCOLOR: int
    COLOR_BLACK: int
    COLOR_BLUE: int
    COLOR_GREEN: int
    COLOR_YELLOW: int
    COLOR_RED: int
    COLOR_WHITE: int
    COLOR_BROWN: int
    reflected_light_intensity: int
    ambient_light_intensity: int
    color: int
    color_name: str
    raw: Tuple[int, int, int]
    rgb: Tuple[int, int, int]
    red: int
    green: int
    blue: int
    def __init__(self, address: str = ..., **kwargs) -> None: ...
    def calibrate_white(self) -> None: ...

class UltrasonicSensor:
    distance_centimeters: float
    distance_centimeters_continuous: float
    distance_centimeters_ping: float
    distance_inches: float
    distance_inches_continuous: float
    distance_inches_ping: float
    other_sensor_present: bool
    def __init__(self, address: str = ..., **kwargs) -> None: ...

class GyroSensor:
    angle: int
    rate: int
    angle_and_rate: Tuple[int, int]
    def __init__(self, address: str = ..., **kwargs) -> None: ...
    def calibrate(self) -> None: ...
    def reset(self) -> None: ...
    def wait_until_angle_changed_by(self, delta: float, direction_sensitive: bool = ...) -> None: ...

class InfraredSensor:
    proximity: int
    def __init__(self, address: str = ..., **kwargs) -> None: ...
