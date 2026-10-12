"""Regression checks for student-facing LCD and LED JSON settings.

Run: python3 -m unittest discover -s tests -v
No EV3 hardware or third-party Python packages are required.
"""

import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock

from tools.ev3_deploy import validate_display_config
from ev3.student_runner import StudentLed, StudentStatus


class DisplayConfigTests(unittest.TestCase):
    def test_defaults_preserve_brickrun_led(self):
        config = {}
        validate_display_config(config)
        self.assertEqual(config["lcd_title"], "STUDENT")
        self.assertEqual(config["lcd_running_text"], "RUNNING")
        self.assertEqual(config["led_color"], "DEFAULT")
        self.assertEqual(config["led_effect"], "DEFAULT")

    def test_customization_accepted(self):
        config = {
            "lcd_title": "ROBOT SOCCER",
            "lcd_program": "EV3-01",
            "lcd_running_text": "PLAYING",
            "led_color": "orange",
            "led_effect": "blink",
        }
        validate_display_config(config)
        self.assertEqual(config["lcd_title"], "ROBOT SOCCER")
        self.assertEqual(config["led_color"], "ORANGE")
        self.assertEqual(config["led_effect"], "BLINK")

    def test_invalid_led_rejected(self):
        with self.assertRaises(SystemExit):
            validate_display_config({"led_color": "PURPLE"})
        with self.assertRaises(SystemExit):
            validate_display_config({"led_effect": "FASTER"})

    def test_invalid_lcd_rejected(self):
        for invalid in ("로봇", "x" * 30, "RUN\nSTOP", ""):
            with self.subTest(value=invalid), self.assertRaises(SystemExit):
                validate_display_config({"lcd_title": invalid})

    def test_runtime_status_and_display_label_are_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            main_path = str(Path(directory) / "main.py")
            with mock.patch.dict(os.environ, {
                "EV3_STUDENT_LCD": "0",
                "EV3_STUDENT_LCD_RUNNING": "PLAYING",
            }):
                status = StudentStatus(main_path)
                status.set("RUNNING")
                self.assertEqual(status.status_labels["RUNNING"], "PLAYING")
                with open(status.status_file) as handle:
                    self.assertEqual(handle.read(), "RUNNING\n")


class LedConfigTests(unittest.TestCase):
    def test_default_delegates_to_brickrun(self):
        with mock.patch.dict(os.environ, {
            "EV3_STUDENT_LED_COLOR": "DEFAULT",
            "EV3_STUDENT_LED_EFFECT": "DEFAULT",
        }):
            leds = StudentLed()
            leds.start(threading.Event())
            self.assertIsNone(leds.thread)
            self.assertIsNone(leds.leds)

    def test_custom_led_failure_does_not_prevent_student_program(self):
        import sys
        import types

        module = types.ModuleType("ev3dev2.led")

        class BrokenLeds:
            def __init__(self):
                raise OSError("No LED permission")

        module.Leds = BrokenLeds
        with mock.patch.dict(sys.modules, {"ev3dev2.led": module}):
            with mock.patch.dict(os.environ, {
                "EV3_STUDENT_LED_COLOR": "ORANGE",
                "EV3_STUDENT_LED_EFFECT": "BLINK",
            }):
                leds = StudentLed()
                leds.start(threading.Event())
                self.assertIsNone(leds.thread)


if __name__ == "__main__":
    unittest.main()
