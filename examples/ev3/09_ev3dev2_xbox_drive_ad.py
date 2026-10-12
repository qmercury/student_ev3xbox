import time

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3xbox import XboxController


# Hardware connection test only.
# Left-stick Y = forward/backward
# Right-stick X = steering
# Both drive outputs are limited to +/-30%.
MAX_POWER = 30

drive = MoveTank(OUTPUT_A, OUTPUT_D)
controller = XboxController()

print("ev3dev2 + Xbox A/D drive test")
print("Lift the drive wheels before testing.")
print("Left stick Y = forward/backward")
print("Right stick X = steering")
print("Output limited to +/-30%.")
print("Ctrl+C to stop.")

try:
    if not controller.wait_until_connected(timeout=5):
        raise RuntimeError("Xbox relay is not connected.")

    while True:
        _, forward = controller.joystick_left()
        turn, _ = controller.joystick_right()

        left = forward + turn
        right = forward - turn

        left = max(-100, min(100, left))
        right = max(-100, min(100, right))

        left_power = int(left * MAX_POWER / 100)
        right_power = int(right * MAX_POWER / 100)

        if left_power == 0 and right_power == 0:
            drive.off(brake=True)
        else:
            drive.on(
                SpeedPercent(left_power),
                SpeedPercent(right_power),
            )

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nTest stopped.")

finally:
    drive.off(brake=True)
    controller.close()
