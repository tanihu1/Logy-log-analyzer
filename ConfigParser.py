class Event:
    def __init__(
        self, type: str, count: bool = False, level: str = "", pattern: str = ""
    ):
        self.type = type
        self.count = count
        self.level = level
        self.pattern = pattern

class ConfigParser:

    def __init__(self):
        pass

    # Gets line pre-stripped
    #FIXME This function is too big
    def parse_config_line(self, line: str) -> Event:
        tokens = line.split()

        event_name = tokens[0]
        count = False
        level = ""
        pattern = ""

        # Line contains flags
        if len(tokens) > 1:
            i = 1
            while i < len(tokens):
                # --pattern is a special flag requiring more attention
                if tokens[i] == "--pattern":
                    regex_tokens = []
                    i += 1
                    while i < len(tokens) and not tokens[i].startswith("--"):
                        regex_tokens.append(tokens[i])
                        i+=1
                    pattern = ' '.join(regex_tokens)
                    continue

                match tokens[i]:
                    case "--count":
                        count = True
                        i += 1
                    case "--level":
                        try:
                            level = tokens[i + 1]
                            i += 2
                        except IndexError:
                            raise ConfigError(
                                "Bad config",
                                ConfigError.MISSING_FLAG_PARAM,
                                i,
                                line
                            )
                        if level.startswith("--"):
                            raise ConfigError("Bad config",ConfigError.MISSING_FLAG_PARAM,i,line)
                    case _:
                        raise ConfigError("Bad config",ConfigError.FLAG_ERROR,i,line)
        return Event(event_name,count, level, pattern)

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
            raise e  # TODO Check for this in main
        for line in config_lines:
            if not line:
                continue
            try:
                result.append(self.parse_config_line(line))
            except ConfigError as e:
                raise e

        return result

class ConfigError(Exception):
    FLAG_ERROR = 1  # TODO refactor?
    MISSING_FLAG_PARAM = 2

    def __init__(self, message, error_type: int, line_num: int, line: str):
        super().__init__(message)
        self.error_type = error_type
        self.line_num = line_num
        self.line = line

    def is_flag_err(self) -> bool:  # TODO are there more errors?
        return self.error_type == self.FLAG_ERROR