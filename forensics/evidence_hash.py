import hashlib
import os
from datetime import datetime

LOG_FILE = "logs/network.log"
HASH_LEDGER = "forensics/evidence_hashes.txt"

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        print("❌ Evidence file not found.")
        exit(1)

    hash_value = calculate_hash(LOG_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"{timestamp} | {LOG_FILE} | SHA256 | {hash_value}\n"

    # Append to ledger
    with open(HASH_LEDGER, "a") as ledger:
        ledger.write(entry)

    print("\n🔐 FORENSIC EVIDENCE HASH STORED")
    print("=" * 70)
    print(entry.strip())
    print("=" * 70)
