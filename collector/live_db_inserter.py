#!/usr/bin/env python3
"""
Live Database Inserter
---------------------
• Tails logs/network.log in real time
• Parses each new entry
• Inserts into SQLite database
"""

import time
import sqlite3

LOG_FILE = "logs/network.log"
DB_FILE = "logs/network_logs.db"

def insert_log(entry):
    parts = entry.strip().split()

    if len(parts) != 7:
        return

    timestamp = parts[0] + " " + parts[1]
    protocol = parts[2]
    src_ip = parts[3]
    dst_ip = parts[4]
    port = int(parts[5])
    action = parts[6]

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO logs (timestamp, protocol, src_ip, dst_ip, port, action)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, protocol, src_ip, dst_ip, port, action))

    conn.commit()
    conn.close()

    print(f"[DB INSERTED] {src_ip} → {port}")

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def main():
    print("[+] Live SQLite insertion started...\n")

    with open(LOG_FILE, "r") as logfile:
        for line in follow(logfile):
            insert_log(line)

if __name__ == "__main__":
    main()
