import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import os

DB_PATH = "logs/network_logs.db"
REPORT_FILE = "reports/incident_correlation.txt"

TIME_WINDOW = timedelta(minutes=2)
THRESHOLD = 5

def correlate_incidents():
    if not os.path.exists("reports"):
        os.mkdir("reports")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, src_ip, port
        FROM logs
        WHERE action = 'DENY'
        ORDER BY timestamp ASC
    """)

    rows = cur.fetchall()
    conn.close()

    events = defaultdict(list)

    for ts, ip, port in rows:
        time_obj = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        events[(ip, port)].append(time_obj)

    report_lines = []
    report_lines.append("🚨 CORRELATED INCIDENT REPORT")
    report_lines.append("=" * 60)

    incident_count = 0

    for (ip, port), times in events.items():
        window = []

        for t in times:
            window = [x for x in window if t - x <= TIME_WINDOW]
            window.append(t)

            if len(window) >= THRESHOLD:
                incident_count += 1
                report_lines.append("[INCIDENT] Brute Force Detected")
                report_lines.append(f"Source IP : {ip}")
                report_lines.append(f"Target Port : {port}")
                report_lines.append(f"Attempts : {len(window)}")
                report_lines.append(
                    f"Time Window : {window[0]} → {window[-1]}"
                )
                report_lines.append("-" * 60)
                break

    report_lines.append(f"Total incidents identified: {incident_count}")

    report_text = "\n".join(report_lines)

    # Save report
    with open(REPORT_FILE, "w") as f:
        f.write(report_text)

    # Print report
    print("\n" + report_text)

if __name__ == "__main__":
    correlate_incidents()
