from ConfigParser import Event
from Scanner import Scanner
from datetime import datetime
import unittest
import re

BASIC_EVENT = [Event("DEVICE")]
COUNT_EVENT = [Event("TELEMETRY", count=True)]
LEVEL_EVENT = [Event("GNMI", level="ERROR")]
REGEX_EVENT = [Event("TELEMETRY", pattern="^Iteration time:\\s\\d+\\.\\d+\\ssec$")]
TIME_EVENT = [Event("GNMI")]

LOG_FILE = "tests/test_logs.log"


class TestBasicUsage(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        with open(LOG_FILE, "r") as log_file:
            self.lines = [s.strip() for s in log_file.readlines()]

    def test_basic_event(self):
        scanner = Scanner(BASIC_EVENT)
        # TODO error handling
        result = scanner.scan_log_directory(LOG_FILE)
        self.assertEqual(
            len(result), 3, "Scanner detected incorrect amount of log lines!"
        )
        self.assertEqual(result[1], self.lines[1], "Scanner line output mismatch!")
        self.assertEqual(result[2], self.lines[2], "Scanner line output mismatch!")

    def test_count_event(self):
        scanner = Scanner(COUNT_EVENT)
        result = scanner.scan_log_directory(LOG_FILE)
        self.assertEqual(
            len(result), 1, "Scanner detected incorrect amount of log lines!"
        )
        self.assertEqual(
            result[0],
            "Event: TELEMETRY count - matches: 2 entries",
            "Scanner returned wrong result for count event",
        )

    def test_level_event(self):
        scanner = Scanner(LEVEL_EVENT)
        result = scanner.scan_log_directory(LOG_FILE)
        self.assertEqual(
            len(result), 3, "Scanner detected incorrect amount of log lines!"
        )
        self.assertEqual(result[1], self.lines[3], "Scanner line output mismatch!")
        self.assertEqual(result[2], self.lines[7], "Scanner line output mismatch!")

    def test_regex_event(self):
        scanner = Scanner(REGEX_EVENT)
        result = scanner.scan_log_directory(LOG_FILE)
        self.assertEqual(
            len(result), 3, "Scanner detected incorrect amount of log lines!"
        )
        self.assertEqual(result[1], self.lines[0], "Scanner line output mismatch!")

    def test_time_filtering(self):
        scanner = Scanner(
            TIME_EVENT,
            datetime.fromisoformat("2025-06-01T14:05:22"),
            datetime.fromisoformat("2025-06-01T14:10:03"),
        )
        result = scanner.scan_log_directory(LOG_FILE)
        self.assertEqual(
            len(result), 3, "Scanner detected incorrect amount of log lines!"
        )


if __name__ == "__main__":
    unittest.main()
