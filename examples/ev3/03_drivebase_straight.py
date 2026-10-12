import time

from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase

# Physical EV3 motor ports:
# A = left drive motor
# D = right drive motor
left_wheel = Motor(Port.A, Direction.CLOCKWISE)
right_wheel = Motor(Port.D, Direction.CLOCKWISE)

# Same constructor style as Pybricks:
# wheel diameter = 88 mm
# axle track = 145 mm
robot = DriveBase(
    left_wheel,
    right_wheel,
    88,
    145,
)

print("DriveBase straight test")
print("200 mm/s for 0.5 seconds")

try:
    robot.drive(200, 0)
    time.sleep(0.5)
finally:
    robot.brake()

print("Stopped")
print("left angle =", left_wheel.angle())
print("right angle =", right_wheel.angle())
