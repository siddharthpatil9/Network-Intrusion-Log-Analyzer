import sqlite3

DB_PATH = "database/network_logs.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            protocol TEXT,
            source_ip TEXT,
            destination_ip TEXT,
            port INTEGER,
            action TEXT
        )
    """)

    conn.commit()
    conn.close()

def clear_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()


def insert_log(log):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (date, time, protocol, source_ip, destination_ip, port, action)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        log["date"],
        log["time"],
        log["protocol"],
        log["source_ip"],
        log["destination_ip"],
        log["port"],
        log["action"]
    ))

    conn.commit()
    conn.close()
