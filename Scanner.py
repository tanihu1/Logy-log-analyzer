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
        # TODO Take care of this
        except IndexError as e:
            raise e
        
    def __str__(self) -> str:
        return self.timestamp + ' ' + self.level + ' ' + self.type + ' ' + self.content


class Scanner:
    # Scanner initially wants to map log lines to events
    def __init__(self, events: list) -> None:
        self.events = events
        event_idx = 0
        self.event_results = {}
        for event in events:
            self.event_results[0] = []
            event_idx += 1

    # Finding all corresponding events for the log line
    def _find_event_matchs(self, log_line: LogLine) -> list:
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
                    f"Event: {event.type} "+
                    f"{f'level [{event.level}] ' if event.level else ''}"+
                    f"{f'pattern [{event.pattern}] ' if event.pattern else ''}"+
                    f"count - matches: {len(value)} entries"
                )
            else:
                result.append(
                    f"Event: {event.type} "+
                    f"{f'level [{event.level}]' if event.level else ''} "+
                    f"{f'pattern [{event.pattern}]' if event.pattern else ''} "+
                    f"- matching log lines:"
                )
                for log_line in value:
                    result.append(str(log_line))

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
