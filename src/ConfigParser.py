import re


# A basic Event data structure representing a single event from the events file
class Event:
    def __init__(
        self, type: str, count: bool = False, level: str = "", pattern: str = ""
    ):
        self.type = type
        self.count = count
        self.level = level
        self.pattern = pattern


# The config parser is responsible for creating Event objects out of events file
class ConfigParser:

    def __init__(self):
        pass

    def _extract_event_name(self, line: str) -> str:
        return line.split()[0]

    def _extract_event_count(self, line: str) -> bool:
        tokens = line.split()
        for token in tokens:
            if token == "--count":
                return True
        return False

    def _extract_event_level(self, line: str) -> str:
        tokens = line.split()
        level = ""
        for token in tokens:
            if token == "--level":
                idx = tokens.index(token)
                # Flag must be followed with an arg
                try:
                    level = tokens[idx + 1]
                except IndexError:
                    raise ConfigError(
                        "Bad config", ConfigError.MISSING_FLAG_PARAM, idx, line
                    )
                if level.startswith("--"):
                    raise ConfigError(
                        "Bad config", ConfigError.MISSING_FLAG_PARAM, idx, line
                    )
        return level

    def _extract_event_pattern(self, line: str) -> str:
        tokens = line.split()
        pattern = ""

        for token in tokens:
            if token == "--pattern":
                idx = tokens.index(token) + 1
                regex_tokens = []
                # Pick regex tokens until a flag is encountered
                while idx < len(tokens) and not tokens[idx].startswith("--"):
                    regex_tokens.append(tokens[idx])
                    idx += 1
                pattern = " ".join(regex_tokens)
                # Regex must compile
                try:
                    re.compile(pattern)
                except:
                    raise ConfigError(
                        "Bad regex in config", ConfigError.REGEX_ERROR, idx, line
                    )

        return pattern

    # Gets line pre-stripped. Parses a single event file line
    def parse_config_line(self, line: str) -> Event:
        tokens = line.split()

        # Check for invalid flags
        for token in tokens:
            if (
                token.startswith("--")
                and token != "--level"
                and token != "--count"
                and token != "--pattern"
            ):
                raise ConfigError("Bad config", ConfigError.FLAG_ERROR, 0, line)

        event_name = self._extract_event_name(line)
        count = self._extract_event_count(line)
        level = self._extract_event_level(line)
        pattern = self._extract_event_pattern(line)

        return Event(event_name, count, level, pattern)

    # Initiates the parsing of an entire events file
    def parse_config_file(self, file_path) -> list:
        config_lines = []
        result = []
        try:
            with open(file_path, "r") as config_file:
                for line in config_file.readlines():
                    line = line.strip()
                    # Checking for comments
                    if line.startswith("#"):
                        continue
                    config_lines.append(line)
        except FileNotFoundError as e:
            raise e

        for line in config_lines:
            if not line:
                continue
            try:
                result.append(self.parse_config_line(line))
            except ConfigError as e:
                raise e
        if len(result) == 0:
            raise ConfigError("No events in Config file", ConfigError.NO_EVENTS, -1, "")
        return result


# A custom error for expressing a problem with the events file
class ConfigError(Exception):
    FLAG_ERROR = 1
    MISSING_FLAG_PARAM = 2
    NO_EVENTS = 3
    REGEX_ERROR = 4

    def __init__(self, message, error_type: int, line_num: int, line: str):
        super().__init__(message)
        self.error_type = error_type
        self.line_num = line_num
        self.line = line
