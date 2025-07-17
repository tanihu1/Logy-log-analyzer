class ConfigParser:

    def __init__(self):
        pass

    def parse_config_line(self, input_config) -> list:
        return []

    def parse_config_file(self, file_path) -> list:
        return []


class Event:
    def __init__(
        self, type: str, count: bool = False, level: str = "", pattern: str = ""
    ):
        self.type = type
        self.count = count
        self.level = level
        self.pattern = pattern


class ConfigError(Exception):
    FLAG_ERROR = 1  # TODO refactor?

    def __init__(self, message, error_type):
        super().__init__(message)
        self.error_type = error_type

    def is_flag_err(self) -> bool:  # TODO are there more errors?
        return self.error_type == self.FLAG_ERROR
