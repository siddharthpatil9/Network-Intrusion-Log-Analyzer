from parser.log_parser import parse_log_line
from database.db_handler import create_table, insert_log, clear_logs
from analyzer.attack_detector import detect_brute_force, detect_port_scan

log_file = "logs/network.log"

create_table()
clear_logs()   # 🔥 Important line

with open(log_file, "r") as file:
    for line in file:
        parsed = parse_log_line(line.strip())
        if parsed:
            insert_log(parsed)

print("\n🚨 Attack Detection Results 🚨")

brute_force = detect_brute_force()
port_scan = detect_port_scan()

if brute_force:
    print("\nBrute Force Detected:")
    for ip, count in brute_force:
        print(f"IP {ip} → {count} failed SSH attempts")
else:
    print("\nNo Brute Force Detected")

if port_scan:
    print("\nPort Scanning Detected:")
    for ip, count in port_scan:
        print(f"IP {ip} → accessed {count} different ports")
else:
    print("\nNo Port Scanning Detected")
