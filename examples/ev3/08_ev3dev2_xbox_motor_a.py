import time

from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent
from ev3xbox import XboxController


# Hardware connection test only:
# Xbox left-stick Y -> EV3 motor port A.
# Output is limited to 30% for a bench test.
MAX_POWER = 30

motor = LargeMotor(OUTPUT_A)
controller = XboxController()

print("ev3dev2 + Xbox motor test")
print("Lift the drive wheels before testing.")
print("Left stick Y controls motor A, limited to +/-30%.")
print("Ctrl+C to stop.")

try:
    if not controller.wait_until_connected(timeout=5):
        raise RuntimeError("Xbox relay is not connected.")

    while True:
        _, stick_y = controller.joystick_left()
        power = int(stick_y * MAX_POWER / 100)

        if power == 0:
            motor.off(brake=True)
        else:
            motor.on(SpeedPercent(power))

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nTest stopped.")

finally:
    motor.off(brake=True)
    controller.close()
