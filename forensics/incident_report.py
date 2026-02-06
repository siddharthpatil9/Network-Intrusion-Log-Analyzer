import sqlite3
from collections import defaultdict
from datetime import datetime
import os

DB_PATH = "logs/network_logs.db"
REPORT_FILE = "reports/incident_report.txt"

def generate_report():
    if not os.path.exists("reports"):
        os.mkdir("reports")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, src_ip, port
        FROM logs
        WHERE action='DENY'
        ORDER BY timestamp ASC
    """)

    rows = cur.fetchall()
    conn.close()

    incidents = defaultdict(list)

    for ts, ip, port in rows:
        incidents[(ip, port)].append(ts)

    report_lines = []
    report_lines.append("📄 INCIDENT RESPONSE REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"Generated At : {datetime.now()}")
    report_lines.append("=" * 70)

    incident_id = 1

    for (ip, port), timestamps in incidents.items():
        if len(timestamps) >= 5:
            report_lines.append(f"Incident ID   : INC-2026-{incident_id:03d}")
            report_lines.append("Attack Type   : SSH Brute Force")
            report_lines.append(f"Source IP     : {ip}")
            report_lines.append(f"Target Port   : {port}")
            report_lines.append(f"First Seen    : {timestamps[0]}")
            report_lines.append(f"Last Seen     : {timestamps[-1]}")
            report_lines.append(f"Total Attempts: {len(timestamps)}")
            report_lines.append("Severity      : HIGH")
            report_lines.append(
                "Evidence      : SQLite logs, SSH authentication failures"
            )
            report_lines.append("-" * 70)
            incident_id += 1

    if incident_id == 1:
        report_lines.append("No reportable incidents found.")

    report_text = "\n".join(report_lines)

    # Save report
    with open(REPORT_FILE, "w") as f:
        f.write(report_text)

    # Print report
    print("\n" + report_text)

if __name__ == "__main__":
    generate_report()
