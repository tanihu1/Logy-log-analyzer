from src.ConfigParser import ConfigParser, ConfigError
from src.Printer import Printer
from src.Scanner import Scanner
import argparse
from datetime import datetime

printer = Printer()


# Define arguments
def set_arguments():
    parser = argparse.ArgumentParser(
        description="Logy - A log analyzer FOR the people, BY the people!"
    )
    parser.add_argument(
        "-l",
        "--log-dir",
        type=str,
        required=True,
        help="Path to directory containing logs",
    )
    parser.add_argument(
        "-e",
        "--events-file",
        type=str,
        required=True,
        help="Path to configuration file",
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="start_time",
        type=str,
        required=False,
        help="Filter logs based on start timestamp",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="end_time",
        type=str,
        required=False,
        help="Filter logs based on end timestamp",
    )
    return parser.parse_args()


# Parse events file using the `ConfigParser`
def parse_config(config_path) -> list:
    parser = ConfigParser()
    try:
        events = parser.parse_config_file(config_path)
        return events
    except FileNotFoundError:
        printer.print_no_config_file()
        exit()
    except ConfigError as e:
        printer.print_config_error(e)
        exit()
    except Exception:
        print("Something went horribly wrong! Please try again")
        exit()


# Initiates log scan according to events
def start_scan(args, events) -> list:
    start_time = None
    end_time = None
    # Test timestamps
    if args.start_time:
        try:
            start_time = datetime.fromisoformat(args.start_time)
        except ValueError:
            printer.print_invalid_timestamp_arg(is_from=True)
            exit()
    if args.end_time:
        try:
            end_time = datetime.fromisoformat(args.end_time)
        except ValueError:
            printer.print_invalid_timestamp_arg(is_from=False)
            exit()

    # Initialize scanner
    scanner = Scanner(events, start_time, end_time)
    # This part is prone to many errors - extensive testing
    try:
        return scanner.scan_log_directory(args.log_dir)
    except FileNotFoundError:
        printer.print_no_log_file()
        exit()
    except NotADirectoryError:
        printer.print_not_dir_error()
        exit()
    except IndexError:
        printer.print_log_file_error()
        exit()
    except ValueError:
        printer.print_log_file_error()
        exit()


def print_results(results):
    printer.print_results(results)


def main():
    args = set_arguments()
    events = parse_config(args.events_file)
    scan_results = start_scan(args, events)
    print_results(scan_results)


if __name__ == "__main__":
    main()
