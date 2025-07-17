import re

#TODO Are log lines necessarily correct?
class _LogLine:
    def __init__(self, line:str) -> None:
        tokens = line.split()
        try:
            self.timestamp = tokens[0]
            self.level = tokens[1]
            self.type = tokens[2]
            self.content = " ".join(tokens[3:])
        #TODO Take care of this
        except IndexError as e:
            raise e

class Scanner:
    def __init__(self, events:list) -> None:
        self.events = events
        event_idx = 0
        self.event_results = {}
        for event in events:
            self.event_results[0] = []
            event_idx += 1
    
    def _find_event_match(self, log_line:_LogLine) -> list:
        idx = 0
        indices = []
        for event in self.events:
            if not event.type == log_line.type:
                idx +=1
                continue
            if event.level and not (event.level == log_line.level):
                idx += 1
                continue
            if event.pattern:
                if re.match(event.pattern,log_line.content):
                    indices.append(idx)
                    idx += 1
                else:
                    idx += 1
                    continue
            indices.append(idx)
            idx += 1

        return indices




    def _scan_log_line(self,line:str):
        parsed_line = _LogLine(line)
        event_idx = self._find_event_match(parsed_line)

    def scan_log_file(self,file_path:str) -> list:
        log_lines = []
        try:
            with open(file_path,'r') as f:
                log_lines = f.readlines()
        except FileNotFoundError as e:
            raise e
        
        for line in log_lines:
            line = line.strip()
            self._scan_log_line(line)

        return []

