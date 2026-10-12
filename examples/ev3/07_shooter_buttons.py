from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Direction, Port
from pybricks.iodevices import XboxController
from pybricks.tools import StopWatch, wait, run_task


# -------------------------------------------------
# Shooter motor setup
# -------------------------------------------------
# Change only the Direction values after the robot is assembled
# so positive dc() means "shooting direction" for both motors.
left_shooter = Motor(
    Port.B,
    Direction.CLOCKWISE,
)

right_shooter = Motor(
    Port.C,
    Direction.CLOCKWISE,
)

controller = XboxController()


# -------------------------------------------------
# Safe bench-test values
# -------------------------------------------------
SHOOTER_POWER = 30
SHOOTER_FORWARD_ANGLE = 35
SHOOTER_BACK_ANGLE = 5
SHOOTER_DIFF_LIMIT = 15
SHOOTER_TIMEOUT_MS = 500


async def shooter():
    pre_rb = False
    pre_lb = False

    # 1 = shooting direction
    # -1 = return direction
    direction = 1

    # "auto"   : RB -> shoot and return automatically
    # "manual" : LB -> move one step at a time
    mode = None
    running = False

    timer = StopWatch()

    left_shooter.reset_angle(0)
    right_shooter.reset_angle(0)

    left_start_angle = left_shooter.angle()
    right_start_angle = right_shooter.angle()

    print("Shooter button test")
    print("RB = automatic shot and return")
    print("LB = manual forward / return")
    print("RB or LB again while moving = emergency stop")
    print("Power =", SHOOTER_POWER)

    try:
        while True:
            await wait(5)

            pressed = controller.buttons.pressed()

            rb_now = Button.RB in pressed
            lb_now = Button.LB in pressed

            rb_pressed = rb_now and not pre_rb
            lb_pressed = lb_now and not pre_lb

            pre_rb = rb_now
            pre_lb = lb_now

            # -------------------------------------------------
            # RB: auto shot / emergency stop
            # -------------------------------------------------
            if rb_pressed:
                if running:
                    left_shooter.brake()
                    right_shooter.brake()

                    running = False
                    direction = 1
                    mode = None
                    print("Emergency stop")
                    continue

                mode = "auto"
                direction = 1
                running = True

                left_start_angle = left_shooter.angle()
                right_start_angle = right_shooter.angle()

                timer.reset()
                print("RB: auto shot")

            # -------------------------------------------------
            # LB: manual forward / return / emergency stop
            # -------------------------------------------------
            elif lb_pressed:
                if running:
                    left_shooter.brake()
                    right_shooter.brake()

                    running = False
                    direction = 1
                    mode = None
                    print("Emergency stop")
                    continue

                current_angle = abs(left_shooter.angle())
                mode = "manual"

                if current_angle >= SHOOTER_FORWARD_ANGLE:
                    direction = -1
                    print("LB: manual return")
                else:
                    direction = 1
                    print("LB: manual forward")

                running = True

                left_start_angle = left_shooter.angle()
                right_start_angle = right_shooter.angle()

                timer.reset()

            if not running:
                continue

            left_raw_angle = left_shooter.angle()
            right_raw_angle = right_shooter.angle()

            left_angle = abs(left_raw_angle)
            right_angle = abs(right_raw_angle)

            # -------------------------------------------------
            # Safety 1: stop if the two shooter motors disagree
            # -------------------------------------------------
            left_moved = abs(left_raw_angle - left_start_angle)
            right_moved = abs(right_raw_angle - right_start_angle)

            if abs(left_moved - right_moved) >= SHOOTER_DIFF_LIMIT:
                left_shooter.brake()
                right_shooter.brake()

                running = False
                direction = 1
                mode = None

                print(
                    "Shooter motor difference:",
                    left_moved,
                    right_moved,
                )
                continue

            # -------------------------------------------------
            # Safety 2: timeout
            # -------------------------------------------------
            if timer.time() >= SHOOTER_TIMEOUT_MS:
                left_shooter.brake()
                right_shooter.brake()

                running = False
                direction = 1
                mode = None

                print(
                    "Shooter timeout:",
                    left_angle,
                    right_angle,
                )
                continue

            # -------------------------------------------------
            # RB automatic mode
            # -------------------------------------------------
            if mode == "auto":
                if (
                    direction == 1
                    and left_angle >= SHOOTER_FORWARD_ANGLE
                ):
                    left_shooter.brake()
                    right_shooter.brake()

                    direction = -1

                    left_start_angle = left_shooter.angle()
                    right_start_angle = right_shooter.angle()

                    timer.reset()
                    await wait(5)

                elif (
                    direction == -1
                    and left_angle <= SHOOTER_BACK_ANGLE
                ):
                    left_shooter.brake()
                    right_shooter.brake()

                    running = False
                    direction = 1
                    mode = None

                    left_shooter.reset_angle(0)
                    right_shooter.reset_angle(0)

                    print("Auto shot complete")
                    continue

            # -------------------------------------------------
            # LB manual mode
            # -------------------------------------------------
            elif mode == "manual":
                if (
                    direction == 1
                    and left_angle >= SHOOTER_FORWARD_ANGLE
                ):
                    left_shooter.brake()
                    right_shooter.brake()

                    running = False
                    mode = None

                    print("Manual forward complete")
                    continue

                elif (
                    direction == -1
                    and left_angle <= SHOOTER_BACK_ANGLE
                ):
                    left_shooter.brake()
                    right_shooter.brake()

                    running = False
                    direction = 1
                    mode = None

                    left_shooter.reset_angle(0)
                    right_shooter.reset_angle(0)

                    print("Manual return complete")
                    continue

            left_shooter.dc(
                direction * SHOOTER_POWER
            )

            right_shooter.dc(
                direction * SHOOTER_POWER
            )

    finally:
        left_shooter.brake()
        right_shooter.brake()
        controller.close()


run_task(shooter())
