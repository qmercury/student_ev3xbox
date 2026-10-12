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

    REFRESH_SECONDS = 0.6

    def __init__(self, main_file):
        self.main_file = main_file
        self.status_file = os.path.join(os.path.dirname(main_file), ".student-status")
        self.lcd_enabled = os.environ.get("EV3_STUDENT_LCD", "1") != "0"
        self.display = None
        self.font_header = None
        self.font_status = None
        self.lock = threading.Lock()
        self.current = None

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
            self._centered_text("STUDENT", 7, self.font_header, "white")
            self._centered_text(self.current, 47, self.font_status)
            self.display.draw.line((9, 91, width - 10, 91), fill="black")
            self._centered_text("main.py", 101, self.font_header)

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

    def refresh_until(self, finished):
        # Brickman/other framebuffer users may repaint over our one-time draw.
        # Re-submit the cached image at a low rate while Python is running.
        # Do not render fonts repeatedly, or block student motor code with work.
        while not finished.wait(self.REFRESH_SECONDS):
            with self.lock:
                if not self.lcd_enabled or self.display is None:
                    continue
                if self.current not in ("STARTING", "RUNNING"):
                    continue
                try:
                    self.display.update()
                except Exception as exc:
                    print("LCD_REFRESH_UNAVAILABLE: {}".format(exc), file=sys.stderr)
                    self.lcd_enabled = False


def main():
    if len(sys.argv) != 2:
        print("Usage: student_runner.py /absolute/path/main.py", file=sys.stderr)
        return 2

    main_file = os.path.abspath(sys.argv[1])
    status = StudentStatus(main_file)
    finished = threading.Event()

    def stop_on_term(signum, frame):
        # Raise in the main thread: student try/finally blocks can run.
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, stop_on_term)

    status.set("STARTING")

    lcd_keeper = threading.Thread(target=status.refresh_until, args=(finished,))
    lcd_keeper.daemon = True
    lcd_keeper.start()

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
        status.set(final_status)

    return 0


if __name__ == "__main__":
    sys.exit(main())
