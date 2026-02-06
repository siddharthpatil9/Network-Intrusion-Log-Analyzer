# 🛡️ Network Log Analyzer

## Overview
A Python-based cybersecurity and digital forensics project that collects system logs, detects malicious activity (such as SSH brute-force attacks and port scans), correlates incidents, preserves forensic evidence and generates professional incident response reports.
This project follows the end-to-end Security Operations Center (SOC) & Digital Forensics lifecycle.

## Project Objectives
- Collect and parse live system/network logs
- Detect common cyber attacks (Brute Force, Port Scanning)
- Correlate multiple events into a single incident
- Store forensic evidence securely
- Generate incident response reports (Terminal & PDF)
- Visualize attack patterns for analysis

## Architecture Overview
Logs → Collector → SQLite DB → Detectors
↓
Incident Correlation
↓
Forensic Report Generator
↓
Visualization


## How to Run
1. Install dependencies
- pip3 install matplotlib pandas
2. Start live log collection
- python3 collector/live_db_inserter.py
3. Run attack detectors
- python3 detector/bruteforce_detector.py
- python3 detector/portscan_detector.py
4. Correlate incidents
- python3 forensics/incident_correlation.py
5. Generate incident report
- python3 forensics/incident_report.py
- python3 forensics/report_pdf.py
6. Visualize attacks
- python3 visualization/attack_graph.py

## Key Features
- Real-time log ingestion
- Automated threat detection
- Incident correlation
- Forensic evidence handling
- Professional reporting
- Visualization for SOC analysis

## Use Cases
- SOC monitoring projects
- Digital forensics demonstrations
- CDAC / cybersecurity academic submission
- Resume and interview showcase
- Blue-team learning labs

