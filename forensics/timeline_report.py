import sqlite3
from datetime import datetime

DB_PATH = "logs/network_logs.db"
REPORT_FILE = "reports/timeline_report.txt"

def generate_timeline():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, protocol, src_ip, dst_ip, port, action
        FROM logs
        ORDER BY timestamp ASC
    """)

    rows = cur.fetchall()
    conn.close()

    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    output = []
    output.append("📜 FORENSIC TIMELINE REPORT")
    output.append("=" * 70)
    output.append(f"Generated At: {timestamp_now}")
    output.append("=" * 70)

    for r in rows:
        output.append(f"{r[0]} | {r[1]} | {r[2]} → {r[3]} | Port {r[4]} | {r[5]}")

    output.append("=" * 70)
    output.append(f"Total events analyzed: {len(rows)}")

    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(output))

    print("\n".join(output))

if __name__ == "__main__":
    generate_timeline()
