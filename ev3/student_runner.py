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
    def __init__(self, main_file):
        self.main_file = main_file
        self.status_file = os.path.join(os.path.dirname(main_file), ".student-status")
        self.lcd_enabled = os.environ.get("EV3_STUDENT_LCD", "1") != "0"
        self.display = None
        self.lock = threading.Lock()
        self.current = None

    def set(self, value):
        with self.lock:
            if self.current == value:
                return
            self.current = value

            # Write atomically so the deploy/check commands never see a partial state.
            try:
                temporary = self.status_file + ".tmp"
                with open(temporary, "w") as output:
                    output.write(value + "\n")
                os.rename(temporary, self.status_file)
            except OSError as exc:
                print("STUDENT_STATUS_FILE_ERROR: {}".format(exc), file=sys.stderr)

            print("STUDENT_STATUS={}".format(value))

            if not self.lcd_enabled:
                return

            try:
                if self.display is None:
                    from ev3dev2.display import Display
                    self.display = Display()

                self.display.clear()
                self.display.draw.text((12, 12), "STUDENT PROGRAM", fill="black")
                self.display.draw.text((12, 49), value, fill="black")
                self.display.draw.text((12, 91), "main.py", fill="black")
                self.display.update()
            except Exception as exc:
                # LCD ownership/permissions must NEVER prevent student code running.
                print("LCD_STATUS_UNAVAILABLE: {}".format(exc), file=sys.stderr)
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
