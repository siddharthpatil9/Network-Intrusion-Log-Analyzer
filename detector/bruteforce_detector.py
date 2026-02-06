#!/usr/bin/env python3
"""
Brute Force Detection Engine
----------------------------
• Reads logs from SQLite
• Detects SSH brute-force attacks
• Uses time-window based threshold
"""

import sqlite3
import time
from datetime import datetime, timedelta

DB_FILE = "logs/network_logs.db"
THRESHOLD = 5          # attempts
WINDOW_MINUTES = 1     # time window

def detect_bruteforce():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    print("[+] Brute-force detection started...\n")

    while True:
        time_limit = (
            datetime.now() - timedelta(minutes=WINDOW_MINUTES)
        ).strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
            SELECT src_ip, COUNT(*) 
            FROM logs
            WHERE action = 'DENY'
              AND port = 22
              AND timestamp >= ?
            GROUP BY src_ip
            HAVING COUNT(*) >= ?
        """, (time_limit, THRESHOLD))

        results = cur.fetchall()

        if results:
            print("🚨 BRUTE FORCE ATTACK DETECTED 🚨")
            for ip, count in results:
                print(
                    f"[ALERT] IP {ip} → {count} failed SSH attempts "
                    f"in last {WINDOW_MINUTES} minute(s)"
                )
            print("-" * 50)

        time.sleep(10)  # check every 10 seconds

if __name__ == "__main__":
    detect_bruteforce()
