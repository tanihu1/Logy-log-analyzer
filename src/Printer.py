from src.ConfigParser import ConfigError


class Printer:
    def __init__(self) -> None:
        pass

    def print_results(self, strings: list):
        for string in strings:
            print(string)

    def print_config_error(self, error: ConfigError):
        match error.error_type:
            case ConfigError.FLAG_ERROR:
                print("Oops! It seems like the config file contains incorrect flags")
                print()
                print("-" * len(error.line))
                print(error.line)
                print("-" * len(error.line))
                print()
                print("Please fix config file and try again.")
            case ConfigError.MISSING_FLAG_PARAM:
                print(
                    "Oops! It seems like one or more flags in the config file"
                    + " are missing their required parameters"
                )
                print()
                print("-" * len(error.line))
                print(error.line)
                print("-" * len(error.line))
                print()
                print("Please fix config file and try again.")
            case ConfigError.REGEX_ERROR:
                print("Oops! It seems like the config file contains invalid regex!")
                print()
                print("-" * len(error.line))
                print(error.line)
                print("-" * len(error.line))
                print()
                print("Please fix config file and try again.")

            case ConfigError.NO_EVENTS:
                print("Oops! No events could be parsed from config file")
                print("Please add at least one valid event and try again.")

    def print_no_config_file(self):
        print("No readable events file could be detected at the defined path.")
        print("Please double-check file location and try again")

    def print_no_log_file(self):
        print("No readable logs file could be detected at the defined path.")
        print("Please double-check file location and try again")

    def print_not_dir_error(self):
        print("Oops! Log directory path provided doesn't seem to be a directory")
        print("Please double-check directory location and try again")

    def print_invalid_timestamp_arg(self, is_from: bool):
        if is_from:
            print("Invalid --from timestamp!")
            print("Please make sure timestamp is in ISO format and try again")
        else:
            print("Invalid --to timestamp!")
            print("Please make sure timestamp is in ISO format and try again")

    def print_log_file_error(self):
        print("Oops! A log file seems to have unformmated lines!")
        print("Please make sure log lines follow:")
        print("<TIMESTAMP IN ISO FORMAT> <LEVEL> <EVENT_TYPE> <MESSAGE>")
