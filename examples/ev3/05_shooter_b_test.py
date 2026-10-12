import time

from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port

# First shooter direction check.
# Physical EV3 motor port B only.
shooter = Motor(Port.B, Direction.CLOCKWISE)

print("Shooter motor B direction test")
print("Port.B = EV3 physical B")
print("30% duty for 0.3 seconds")

try:
    shooter.dc(30)
    time.sleep(0.3)
finally:
    shooter.brake()

print("Stopped")
print("angle =", shooter.angle())
