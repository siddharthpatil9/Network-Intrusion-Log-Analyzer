#!/usr/bin/env python3
"""
Live SSH Log Collector
---------------------
• Reads live SSH logs from systemd journal
• Detects failed SSH authentication attempts
• Supports IPv4 and IPv6 addresses
• Writes normalized network logs to logs/network.log
"""

import subprocess
import re
import datetime
import os

# Output file
OUTPUT_LOG = "logs/network.log"

# Regex to capture IPv4 + IPv6
SSH_FAIL_REGEX = re.compile(
    r"Failed password.* from ([0-9a-fA-F:.]+)"
)

def collect_live_logs():
    print("[DEBUG] Collector script started")
    print("[+] Live SSH log collection started...\n")

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Start journalctl process
    process = subprocess.Popen(
        ["journalctl", "-u", "ssh", "-f", "-o", "short"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Read journal output line by line
    for line in process.stdout:
        line = line.strip()

        # Check for SSH failure
        match = SSH_FAIL_REGEX.search(line)
        if match:
            src_ip = match.group(1)

            timestamp = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Normalized log format
            log_entry = (
                f"{timestamp} TCP {src_ip} 127.0.0.1 22 DENY\n"
            )

            # Write to network log
            with open(OUTPUT_LOG, "a") as f:
                f.write(log_entry)

            print(f"[LOG ADDED] {log_entry.strip()}")

if __name__ == "__main__":
    try:
        collect_live_logs()
    except KeyboardInterrupt:
        print("\n[!] Live log collection stopped by user")
