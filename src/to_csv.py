"""Convert FOIA requests page to a singular CSV file."""

import csv
import pdfplumber

with pdfplumber.open("data/pii/requests.pdf") as pdf:
    # Open CSV file once and write headers
    with open("data/pii/requests_parsed.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "desc"])

        for i, p in enumerate(pdf.pages):
            table = p.extract_table()
            if table:
                for row in table:
                    if row and len(row) >= 2:
                        id_val = "".join(row[0].split("\n"))
                        writer.writerow([id_val, row[1]])
