import sqlite3
from collections import defaultdict

DB_PATH = "database/network_logs.db"


def detect_brute_force(threshold=3):
    """
    Detect brute force attempts on SSH (port 22)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source_ip, COUNT(*) 
        FROM logs 
        WHERE port=22 AND action='DENY'
        GROUP BY source_ip
        HAVING COUNT(*) >= ?
    """, (threshold,))

    results = cursor.fetchall()
    conn.close()

    return results


def detect_port_scan(threshold=3):
    """
    Detect port scanning based on multiple port access attempts
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source_ip, COUNT(DISTINCT port)
        FROM logs
        GROUP BY source_ip
        HAVING COUNT(DISTINCT port) >= ?
    """, (threshold,))

    results = cursor.fetchall()
    conn.close()

    return results
