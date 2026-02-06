from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

OUTPUT_PDF = "reports/Forensic_Incident_Report.pdf"

REPORT_FILES = [
    "reports/timeline_report.txt",
    "reports/incident_correlation.txt",
    "reports/incident_report.txt"
]

def generate_pdf():
    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Network Log Forensic Investigation Report")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Generated on: {datetime.now()}")
    y -= 40

    for file in REPORT_FILES:
        if not os.path.exists(file):
            continue

        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"Report Source: {file}")
        y -= 20

        c.setFont("Helvetica", 9)

        with open(file, "r") as f:
            for line in f:
                if y < 40:
                    c.showPage()
                    c.setFont("Helvetica", 9)
                    y = height - 40

                c.drawString(40, y, line.strip())
                y -= 12

        y -= 20

    c.save()
    print(f"[+] PDF report generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_pdf()
