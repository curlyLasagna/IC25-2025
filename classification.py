"""Classify each FOIA based on keywords"""

import csv

REQUESTS_FILE = "./data/data.csv"
DEPARTMENTS_FILE = "./data/departments.csv"


def initialize_foia_keyword_map():
    """
    Load a list of keywords then map them to their
    corresponding department, and designated POC within a tuple.
    """

    keyword_dict = {}
    file = open(DEPARTMENTS_FILE, "r", encoding="utf8")
    reader = csv.reader(file)

    # Column order: Department, Keywords, Name
    for i, row in enumerate(reader):
        dept_name = row[0]
        poc_name = row[2]
        
        # combine dept name and contact name into a tuple,
        # so its easier to grab 'n parse programatically
        department_info = tuple([dept_name, poc_name])

        # skip the first row
        if i == 0:
            continue

        # load the keywords if the department is not in the map
        if dept_name not in keyword_dict:
            keyword_dict[department_info] = row[1]

    file.close()
    return keyword_dict


def match_categories(foia_description: str, categories: dict) -> str:
    """Get category matches based off a FOIA description."""

    categories = initialize_foia_keyword_map()
    v_adjectives = []
    for word in foia_description.split(" "):
        for dept_info, dept_keywords in categories.items():
            dept_name_and_poc = f"{dept_info[0]} - {dept_info[1]}"

            if word in dept_keywords.split(","):
                if dept_name_and_poc not in v_adjectives:
                    v_adjectives.append(dept_name_and_poc)

    # If we don't have any adjectives, the report is not known.
    if len(v_adjectives) < 1:
        v_adjectives.append("Unknown")

    return v_adjectives

    # departments = open(DEPARTMENTS_FILE, "r")
    # for entry in departments:
    #     print(entry)


def main(data, dept_keywords: dict) -> None:
    """
    This script is responsible for classifying each request with
    the appropriate category based on keywords that specified below.
    Each keyword corresponds with a specific "category" (department)
    that is equipped with handling said report
    """
    foias = open(data, "r", encoding="utf8")
    reader = csv.reader(foias, delimiter=",")
    for row in reader:
        dept_matches = match_categories(row[1], dept_keywords)
        res = {
            "foiaId": row[0],
            "departments": [x for x in dept_matches]
        }
        
        print(res)

    foias.close()


if __name__ == "__main__":
    # Load keywords into memory prior to doing anything.
    keywords = initialize_foia_keyword_map()

    main(REQUESTS_FILE, keywords)
