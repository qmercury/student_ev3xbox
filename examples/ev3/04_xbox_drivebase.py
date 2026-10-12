from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Direction, Port
from pybricks.robotics import DriveBase
from pybricks.iodevices import XboxController
from pybricks.tools import wait, run_task


left_wheel = Motor(Port.A, Direction.CLOCKWISE)
right_wheel = Motor(Port.D, Direction.CLOCKWISE)

controller = XboxController()

robot = DriveBase(
    left_wheel,
    right_wheel,
    88,
    145,
)

speed = 200
steer_rate = 2

# Keep this below about 158 deg/s at speed=200 mm/s and axle_track=145 mm
# so the inside wheel stays forward instead of reversing during a turn.
turn_rate = 120


async def main():
    print("Xbox DriveBase test")
    print("D-pad UP/DOWN = forward/backward")
    print("D-pad LEFT/RIGHT = fixed-rate turning")
    print("Right stick X = steering while UP/DOWN is held")
    print("Release D-pad = brake")
    print("Ctrl+C to stop")

    try:
        while True:
            await wait(10)

            pressed = controller.buttons.pressed()
            joystick_x = controller.joystick_right()[0]

            if Button.UP in pressed:
                robot.drive(
                    speed,
                    joystick_x * steer_rate,
                )

            elif Button.DOWN in pressed:
                robot.drive(
                    -speed,
                    joystick_x * steer_rate,
                )

            # Match the previous SPIKE soccer program's button structure.
            elif Button.LEFT in pressed:
                robot.drive(
                    speed,
                    -turn_rate,
                )

            elif Button.RIGHT in pressed:
                robot.drive(
                    speed,
                    turn_rate,
                )

            else:
                robot.brake()

    finally:
        robot.brake()
        controller.close()


run_task(main())
