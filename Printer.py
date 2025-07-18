from ConfigParser import ConfigError

class Printer:
    def __init__(self) -> None:
        pass

    def print_results(self, strings:list):
        for string in strings:
            print(string)
    
    def print_config_error(self, error:ConfigError):
        match error.error_type:
            case ConfigError.FLAG_ERROR:
                print("Oops! It seems like the config file contains incorrect flags")
                print()
                print("-"*len(error.line))
                print(error.line)
                print("-"*len(error.line))
                print()
                print("Please fix config file and try again.")
            case ConfigError.MISSING_FLAG_PARAM:
                print(
                    "Oops! It seems like one or more flags in the config file" +
                    " are missing their required parameters"
                    )
                print()
                print("-"*len(error.line))
                print(error.line)
                print("-"*len(error.line))
                print()
                print("Please fix config file and try again.")
            case ConfigError.NO_EVENTS:
                print("Oops! No events could be parsed from config file")
                print("Please add at least one valid event and try again.")
