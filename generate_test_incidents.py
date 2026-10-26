import csv
import uuid
import os
from datetime import datetime, timezone

def generate_test_csv(filename="data/ej8_record_tests.csv"):
    """
    Generates a test CSV file with incident records for Data Cloud ingestion.
    The second record contains Priority = 'High' to trigger the Data Action.
    """
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Define the expected headers for the Incident Data Stream
    headers = ["Incident_Id", "NumGuia", "Priority", "Internal_Organization", "Reported_Date"]
    
    # Create 3 dummy records. The second one is the trigger (Priority = High).
    records = [
        [str(uuid.uuid4()), "TRK-2026A", "Low",    "MTY-HUB",  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")],
        [str(uuid.uuid4()), "TRK-2026B", "High",   "CDMX-HUB", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")], # <- The Trigger!
        [str(uuid.uuid4()), "TRK-2026C", "Medium", "GDL-HUB",  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")]
    ]
    
    # Write to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(records)
    
    print(f"✅ Successfully generated file '{filename}' with 3 test records.")
    print("-> Please upload this CSV to your Data Cloud Data Stream and click 'Refresh'.")

if __name__ == "__main__":
    generate_test_csv()
