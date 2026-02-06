import re

def parse_log_line(line):
    """
    Parses a single network log line and returns a dictionary.
    """

    pattern = (
        r"(\d{4}-\d{2}-\d{2})\s+"      # Date
        r"(\d{2}:\d{2}:\d{2})\s+"      # Time
        r"(TCP|UDP)\s+"               # Protocol
        r"([\d\.]+)\s+"               # Source IP
        r"([\d\.]+)\s+"               # Destination IP
        r"(\d+)\s+"                   # Port
        r"(ALLOW|DENY)"               # Action
    )

    match = re.match(pattern, line)

    if match:
        return {
            "date": match.group(1),
            "time": match.group(2),
            "protocol": match.group(3),
            "source_ip": match.group(4),
            "destination_ip": match.group(5),
            "port": int(match.group(6)),
            "action": match.group(7)
        }
    else:
        return None
