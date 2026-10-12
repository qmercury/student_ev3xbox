#!/usr/bin/env python3
"""Run an EV3 student main.py and report its lifecycle on the brick LCD.

This wrapper runs the student's program in the SAME Python process. It must
never run a separate orphanable motor-control child process.
Compatible with EV3 ev3dev Python 3.5.
"""

import os
import runpy
import signal
import sys
import threading


class StudentStatus:
    """Keep an EV3 lifecycle status visible without editing student main.py."""

    def __init__(self, main_file):
        self.main_file = main_file
        self.status_file = os.path.join(os.path.dirname(main_file), ".student-status")
        self.lcd_enabled = os.environ.get("EV3_STUDENT_LCD", "1") != "0"
        self.display = None
        self.font_header = None
        self.font_status = None
        self.lock = threading.Lock()
        self.current = None
        self.title = os.environ.get("EV3_STUDENT_LCD_TITLE", "STUDENT")
        self.footer = os.environ.get("EV3_STUDENT_LCD_PROGRAM", "main.py")
        self.status_labels = {
            "STARTING": os.environ.get("EV3_STUDENT_LCD_STARTING", "STARTING"),
            "RUNNING": os.environ.get("EV3_STUDENT_LCD_RUNNING", "RUNNING"),
            "STOPPED": os.environ.get("EV3_STUDENT_LCD_STOPPED", "STOPPED"),
            "ERROR": os.environ.get("EV3_STUDENT_LCD_ERROR", "ERROR"),
        }

    @staticmethod
    def _font(candidates):
        # ev3dev2 supplies bitmap fonts designed for the 178x128 EV3 LCD.
        from ev3dev2 import fonts

        for name in candidates:
            try:
                return fonts.load(name)
            except (OSError, IOError, ValueError, KeyError):
                continue
        return None

    def _centered_text(self, text, y, font=None, fill="black"):
        width = self.display.xres
        try:
            text_width = self.display.draw.textsize(text, font=font)[0]
        except Exception:
            text_width = len(text) * (14 if font is self.font_status else 8)
        x = max(0, int((width - text_width) / 2))
        self.display.draw.text((x, y), text, font=font, fill=fill)

    def _draw_lcd(self):
        # Caller holds lock. Render only when the lifecycle state changes.
        if not self.lcd_enabled:
            return

        try:
            if self.display is None:
                from ev3dev2.display import Display
                self.display = Display()
                self.font_header = self._font(("luBS14", "helvB14"))
                self.font_status = self._font(("helvB24", "luBS24"))

            self.display.clear()
            width = self.display.xres

            # High-contrast header, large state, small program name.
            self.display.draw.rectangle((0, 0, width - 1, 30), fill="black")
            self._centered_text(self.title, 7, self.font_header, "white")
            self._centered_text(self.status_labels.get(self.current, self.current), 47, self.font_status)
            self.display.draw.line((9, 91, width - 10, 91), fill="black")
            self._centered_text(self.footer, 101, self.font_header)

            self.display.update()
        except Exception as exc:
            # An unavailable or occupied display must not stop motor control.
            print("LCD_STATUS_UNAVAILABLE: {}".format(exc), file=sys.stderr)
            self.lcd_enabled = False

    def set(self, value):
        with self.lock:
            if self.current == value:
                return
            self.current = value

            # Write atomically so check/deploy never see a partial state.
            try:
                temporary = self.status_file + ".tmp"
                with open(temporary, "w") as output:
                    output.write(value + "\n")
                os.rename(temporary, self.status_file)
            except OSError as exc:
                print("STUDENT_STATUS_FILE_ERROR: {}".format(exc), file=sys.stderr)

            print("STUDENT_STATUS={}".format(value))
            self._draw_lcd()


class StudentLed:
    """Optional EV3 key LEDs; DEFAULT delegates to brickrun's heartbeat."""

    def __init__(self):
        self.color = os.environ.get("EV3_STUDENT_LED_COLOR", "DEFAULT")
        self.effect = os.environ.get("EV3_STUDENT_LED_EFFECT", "DEFAULT")
        if self.effect == "DEFAULT" and self.color != "DEFAULT":
            self.effect = "BLINK"
        if self.color == "DEFAULT" and self.effect != "DEFAULT":
            self.color = "GREEN"
        self.leds = None
        self.thread = None

    def _color(self, color):
        for group in ("LEFT", "RIGHT"):
            self.leds.set_color(group, color)

    def start(self, finished):
        if self.effect == "DEFAULT":
            return

        try:
            from ev3dev2.led import Leds
            self.leds = Leds()
            # brickrun enables the green heartbeat trigger before launching us.
            # Detach all four LED channels before setting a custom color.
            for group in ("LEFT", "RIGHT"):
                self.leds.set(group, trigger="none")
        except Exception as exc:
            print("LED_STATUS_UNAVAILABLE: {}".format(exc), file=sys.stderr)
            self.leds = None
            return

        def keep_color():
            try:
                if self.effect == "OFF":
                    self._color("BLACK")
                elif self.effect == "SOLID":
                    self._color(self.color)
                elif self.effect == "BLINK":
                    while not finished.is_set():
                        self._color(self.color)
                        if finished.wait(0.5):
                            break
                        self._color("BLACK")
                        if finished.wait(0.5):
                            break
            except Exception as exc:
                # The LED is informational; failures must never stop a robot.
                print("LED_STATUS_UNAVAILABLE: {}".format(exc), file=sys.stderr)

        self.thread = threading.Thread(target=keep_color)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        # The process exits immediately afterward, when brickrun restores LEDs.
        if self.thread is not None:
            self.thread.join(1.0)


def main():
    if len(sys.argv) != 2:
        print("Usage: student_runner.py /absolute/path/main.py", file=sys.stderr)
        return 2

    main_file = os.path.abspath(sys.argv[1])
    status = StudentStatus(main_file)
    led = StudentLed()
    finished = threading.Event()

    def stop_on_term(signum, frame):
        # Raise in the main thread: student try/finally blocks can run.
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, stop_on_term)

    # brickrun itself is a launcher process; record the Python process as
    # well so that the deploy tool can stop it if the launcher gets stuck.
    runtime_pid_file = os.path.join(os.path.dirname(main_file), ".student.runtime.pid")
    with open(runtime_pid_file, "w") as output:
        output.write("{}\n".format(os.getpid()))

    status.set("STARTING")
    led.start(finished)

    def mark_running():
        # An alive interpreter is RUNNING, not necessarily ready to drive.
        if not finished.wait(1.0):
            status.set("RUNNING")

    watcher = threading.Thread(target=mark_running)
    watcher.daemon = True
    watcher.start()

    final_status = "STOPPED"
    try:
        runpy.run_path(main_file, run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (None, 0):
            final_status = "ERROR"
        raise
    except KeyboardInterrupt:
        pass
    except BaseException:
        final_status = "ERROR"
        raise
    finally:
        finished.set()
        led.stop()
        status.set(final_status)
        try:
            with open(runtime_pid_file, "r") as source:
                recorded_pid = source.read().strip()
            if recorded_pid == str(os.getpid()):
                os.unlink(runtime_pid_file)
        except OSError:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
