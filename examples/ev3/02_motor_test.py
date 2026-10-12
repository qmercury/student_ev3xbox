import time

from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port

# EV3 ports are used exactly as printed on the brick.
# Port.A means physical EV3 motor port A.
left_wheel = Motor(Port.A, Direction.CLOCKWISE)

print("Left wheel motor test")
print("Port.A = EV3 physical A")
print("30% duty for 0.5 seconds")

try:
    left_wheel.dc(30)
    time.sleep(0.5)
finally:
    left_wheel.brake()

print("Stopped")
print("angle =", left_wheel.angle())
