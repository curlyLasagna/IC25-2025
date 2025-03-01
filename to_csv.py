from pypdf import PdfReader
import csv

reader = PdfReader("./yo.pdf")
for p in reader.pages:
    print(p.extract_text())
    # with open("data.csv", "w", newline="") as csvFile:
    # writer = csv.writer(csvFile)
    # writer.writerow(p.extract_text())
