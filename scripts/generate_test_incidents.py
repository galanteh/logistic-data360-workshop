import csv
import os
import time
from datetime import datetime, timezone

def generate_test_incidents(filename="data/ej8_record_tests.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    headers = ["IncidentID", "NumGuia", "FechaApertura", "Severidad", "TipoIncidencia"]
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ts = int(time.time())

    records = [
        [f"INC-{ts}-01", f"TRK-{ts}-FIRE", now_iso, "High", "Route_Delay"],
        [f"INC-{ts}-02", f"TRK-{ts}-NORM", now_iso, "Low", "Wrong_Address"],
        [f"INC-{ts}-03", f"TRK-{ts}-CRIT", now_iso, "High", "Damaged_Package"]
    ]

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)

    print(f"✅ Generated {len(records)} NEW test records in '{filename}':")
    for r in records:
        print(f"   • {r[0]} | Guía: {r[1]} | Severity: {r[3]} | Type: {r[4]}")

if __name__ == "__main__":
    generate_test_incidents()
