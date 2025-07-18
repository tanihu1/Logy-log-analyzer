from datetime import datetime
from typing import Optional
from ConfigParser import Event
import re


# TODO Are log lines necessarily correct?
class LogLine:
    def __init__(self, line: str) -> None:
        tokens = line.split()
        try:
            self.timestamp = tokens[0]
            self.level = tokens[1]
            self.type = tokens[2]
            self.content = " ".join(tokens[3:])
        except IndexError as e:
            raise e

    def __str__(self) -> str:
        return self.timestamp + " " + self.level + " " + self.type + " " + self.content


class Scanner:
    # Scanner initially wants to map log lines to events
    def __init__(
        self,
        events: list,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> None:
        self.events = events
        self.start_time = start_time
        self.end_time = end_time
        event_idx = 0
        self.event_results = {}
        for event in events:
            self.event_results[event_idx] = []
            event_idx += 1

    # Finding all corresponding events for the log line
    def _find_event_matchs(self, log_line: LogLine) -> list:
        if not self._check_line_timestamp(log_line):
            return []
        idx = 0
        indices = []
        for event in self.events:
            if not event.type == log_line.type:
                idx += 1
                continue
            if event.level and not (event.level == log_line.level):
                idx += 1
                continue
            if event.pattern:
                if re.match(event.pattern, log_line.content):
                    indices.append(idx)
                    idx += 1
                    continue
                else:
                    idx += 1
                    continue
            indices.append(idx)
            idx += 1

        return indices

    def _check_line_timestamp(self,line:LogLine) -> bool:
        line_time = datetime.fromisoformat(line.timestamp)
        if self.start_time and self.end_time:
            return line_time >= self.start_time and line_time <= self.end_time
        
        if self.start_time:
            return line_time >= self.start_time

        if self.end_time:
            return line_time <= self.end_time
        
        return True
    
    def _scan_log_line(self, line: str):
        parsed_line = LogLine(line)
        event_indices = self._find_event_matchs(parsed_line)

        for idx in event_indices:
            self.event_results[idx].append(parsed_line)

    # Assembles final array of print-ready strings
    def _create_printable_result(self) -> list:
        # Python 3.7 saves insertion order (nice)
        result = []
        for key, value in self.event_results.items():
            event: Event = self.events[key]
            if event.count:
                result.append(
                    # Python formatting shananigens
                    f"\033[33mEvent\033[0m: {event.type} "
                    + f"{f'level [\033[32m{event.level}\033[0m] ' if event.level else ''}"
                    + f"{f'pattern [\033[34m{event.pattern}\033[0m] ' if event.pattern else ''}"
                    + f"count - matches: {len(value)} entries"
                )
            else:
                result.append(
                    f"\033[33mEvent\033[0m: {event.type} "
                    + f"{f'level [\033[32m{event.level}\033[0m]' if event.level else ''} "
                    + f"{f'pattern [\033[34m{event.pattern}\033[0m]' if event.pattern else ''} "
                    + f"- matching log lines:"
                )
                for log_line in value:
                    result.append(str(log_line))
            result.append("") # For better formatting

        return result

    # Intializes scan
    def scan_log_file(self, file_path: str) -> list:
        log_lines = []
        try:
            with open(file_path, "r") as f:
                log_lines = f.readlines()
        except FileNotFoundError as e:
            raise e

        for line in log_lines:
            line = line.strip()
            self._scan_log_line(line)

        return self._create_printable_result()
