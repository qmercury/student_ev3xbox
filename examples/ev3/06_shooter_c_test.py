import time

from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port

# Second shooter direction check.
# Physical EV3 motor port C only.
shooter = Motor(Port.C, Direction.CLOCKWISE)

print("Shooter motor C direction test")
print("Port.C = EV3 physical C")
print("30% duty for 0.3 seconds")

try:
    shooter.dc(30)
    time.sleep(0.3)
finally:
    shooter.brake()

print("Stopped")
print("angle =", shooter.angle())
