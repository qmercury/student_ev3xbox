import asyncio

from ev3dev2.motor import MediumMotor, MoveJoystick, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3xbox import XboxController


# 예시 장치 선언입니다.
# 학생은 자기 로봇에 맞게 장치 종류와 포트를 직접 정합니다.
drive = MoveJoystick(OUTPUT_A, OUTPUT_D)
shooter = MediumMotor(OUTPUT_B)
controller = XboxController()


async def drive_task():
    while True:
        # 학생이 주행 알고리즘을 작성합니다.

        await asyncio.sleep(0.02)


async def shooter_task():
    while True:
        # 학생이 슈터 알고리즘을 작성합니다.

        await asyncio.sleep(0.02)


async def main():
    await asyncio.gather(
        drive_task(),
        shooter_task(),
    )


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())

finally:
    drive.off(brake=True)
    shooter.off(brake=True)
    controller.close()
    loop.close()
