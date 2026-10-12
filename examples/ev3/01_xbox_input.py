import time

from pybricks.iodevices import XboxController
from pybricks.parameters import Button

controller = XboxController()

print("Xbox student API test")
print("Press A on the teacher-connected Xbox controller.")
print("Ctrl+C to stop")

previous = None

try:
    while True:
        pressed = controller.buttons.pressed()
        snapshot = (
            tuple(sorted(pressed)),
            controller.joystick_left(),
            controller.joystick_right(),
            controller.triggers(),
            controller.connected(),
        )

        if snapshot != previous:
            previous = snapshot
            print(
                "connected={} buttons={} left={} right={} triggers={}".format(
                    snapshot[4],
                    ",".join(snapshot[0]) or "-",
                    snapshot[1],
                    snapshot[2],
                    snapshot[3],
                )
            )

        if Button.A in pressed:
            pass

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nTest stopped.")

finally:
    controller.close()
