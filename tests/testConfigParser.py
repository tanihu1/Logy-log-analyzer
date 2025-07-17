from ConfigParser import ConfigParser, ConfigError
import unittest

VALID_CONFIG_LINE = "TELEMETRY --count --pattern ^Iteration time:\s\d+\.\d+\ssec$"
INVALID_FLAG = "DEVICE --count --level WARNING --amber"

class TestBasicExecution(unittest.TestCase):
    def test_valid_line(self):
        parser = ConfigParser()
        result = parser.parse_config_str(VALID_CONFIG_LINE)

        self.assertEqual(len(result),1,"Config parser detected incorrect amount of events!")
        self.assertEqual(result[0].type, "TELEMETRY", "Config parser detected incorrect type of event!")
        self.assertTrue(result[0].count, "Config parser detected wrong 'count' flag!")
        self.assertEqual(result[0].type, "^Iteration time:\s\d+\.\d+\ssec$", "Config parser detected incorrect regex!")

    def test_detectes_invalid_flag(self):
        parser = ConfigParser()
        try:
            parser.parse_config_str(INVALID_FLAG)
            # If no exception is thrown, test failed
            self.fail("Config parser did not detect invalid type!")
        except ConfigError as e:
            self.assertTrue(e.is_flag_err(), "Config parser raised wrong exception!")
