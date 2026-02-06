#!/usr/bin/env python3
"""
Port Scan / Reconnaissance Detector (SSH-based)
-----------------------------------------------
• Works with SSH-only logs
• Detects rapid repeated connection attempts
"""

import sqlite3
import time
from datetime import datetime, timedelta

DB_FILE = "logs/network_logs.db"
ATTEMPT_THRESHOLD = 8
WINDOW_MINUTES = 1

def detect_recon():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    print("[+] Port scan / recon detection started...\n")

    while True:
        time_limit = (
            datetime.now() - timedelta(minutes=WINDOW_MINUTES)
        ).strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
            SELECT src_ip, COUNT(*) as attempts
            FROM logs
            WHERE timestamp >= ?
              AND port = 22
            GROUP BY src_ip
            HAVING attempts >= ?
        """, (time_limit, ATTEMPT_THRESHOLD))

        results = cur.fetchall()

        if results:
            print("🚨 RECONNAISSANCE ACTIVITY DETECTED 🚨")
            for ip, count in results:
                print(
                    f"[ALERT] IP {ip} → {count} rapid SSH connection attempts "
                    f"in last {WINDOW_MINUTES} minute(s)"
                )
            print("-" * 50)

        time.sleep(10)

if __name__ == "__main__":
    detect_recon()
