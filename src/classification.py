"""Classify each FOIA based on keywords"""

import csv
from types import SimpleNamespace

REQUESTS_FILE = "./data/pii/data.csv"
DEPARTMENTS_FILE = "./data/department.csv"


class CategoryMatch(SimpleNamespace):
    """Define what a category match is."""

    departments: list[str]
    keywords: list[str]


def initialize_foia_keyword_map():
    """
    Load a list of keywords then map them to their
    corresponding department, and designated POC within a tuple.
    """

    keyword_dict = {}
    file = open(DEPARTMENTS_FILE, "r", encoding="latin-1")
    reader = csv.reader(file)

    # Column order: Department, Keywords, Name
    for i, row in enumerate(reader):
        dept_name = row[0]

        # skip the first row
        if i == 0:
            continue

        # load the keywords if the department is not in the map
        if dept_name not in keyword_dict:
            keyword_dict[dept_name] = row[2]

    file.close()
    return keyword_dict


def match_categories(foia_description: str, categories: dict) -> CategoryMatch:
    """Get category matches based off a FOIA description."""

    categories = initialize_foia_keyword_map()
    valid_categories = []
    matched_keywords = []

    for word in foia_description.split(" "):
        for dept, dept_keywords in categories.items():
            if word in dept_keywords.split(",") and len(word) > 0:
                if dept not in valid_categories:
                    matched_keywords.append(word)
                    valid_categories.append(dept)

    # If we don't have any adjectives, the report is not known.
    if len(valid_categories) < 1:
        valid_categories.append("Unknown")

    return CategoryMatch(departments=valid_categories, keywords=matched_keywords)


def main(data, dept_keywords: dict) -> None:
    """
    This script is responsible for classifying each request with
    the appropriate category based on keywords that specified below.
    Each keyword corresponds with a specific "category" (department)
    that is equipped with handling said report
    """
    foias = open(data, "r", encoding="utf8")
    processed_foias_file = open("results.csv", "w", encoding="utf8")

    # We do not include the description because they may include PII.
    fields = ["foia_id", "departments", "keywords"]
    reader = csv.reader(foias, delimiter=",")
    writer = csv.DictWriter(processed_foias_file, delimiter=",", fieldnames=fields)

    writer.writeheader()

    for row in reader:
        classification = match_categories(row[1], dept_keywords)
        res = {
            "foia_id": f"{row[0]}",
            "departments": ",".join(classification.departments),
            "keywords": ",".join(classification.keywords),
        }

        writer.writerow(res)

    foias.close()


if __name__ == "__main__":
    # Load keywords into memory prior to doing anything.
    keywords = initialize_foia_keyword_map()

    main(REQUESTS_FILE, keywords)
