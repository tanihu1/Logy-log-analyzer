from ConfigParser import ConfigParser, ConfigError, Event
import unittest

VALID_CONFIG_LINE = "TELEMETRY --count --pattern ^Iteration time:\\s\\d+\\.\\d+\\ssec$"
INVALID_FLAG = "DEVICE --count --level WARNING --amber"

class TestBasicExecution(unittest.TestCase):
    def test_valid_line(self):
        parser = ConfigParser()
        result = parser.parse_config_line(VALID_CONFIG_LINE)

        self.assertEqual(result.type, "TELEMETRY", "Config parser detected incorrect type of event!")
        self.assertTrue(result.count, "Config parser detected wrong 'count' flag!")
        self.assertEqual(result.pattern, "^Iteration time:\\s\\d+\\.\\d+\\ssec$", "Config parser detected incorrect regex!")

    def test_detectes_invalid_flag(self):
        parser = ConfigParser()
        try:
            parser.parse_config_line(INVALID_FLAG)
            # If no exception is thrown, test failed
            self.fail("Config parser did not detect invalid type!")
        except ConfigError as e:
            self.assertTrue(e.is_flag_err(), "Config parser raised wrong exception!")
