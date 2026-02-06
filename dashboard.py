import sqlite3
import matplotlib.pyplot as plt
from collections import Counter

DB_PATH = "logs/network_logs.db"

def generate_dashboard():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT src_ip
        FROM logs
        WHERE action='DENY'
    """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No data available for dashboard.")
        return

    ip_counts = Counter([r[0] for r in rows])

    ips = list(ip_counts.keys())
    counts = list(ip_counts.values())

    plt.figure()
    plt.bar(ips, counts)
    plt.xlabel("Source IP")
    plt.ylabel("Failed Attempts")
    plt.title("SSH Brute Force Attempts per IP")
    plt.show()

if __name__ == "__main__":
    generate_dashboard()
