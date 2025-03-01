"""Classify each FOIA based on keywords"""

import csv

REQUESTS_FILE = "./data/data.csv"
DEPARTMENTS_FILE = "./data/departments.csv"

def match_categories(foia_description: str) -> str:
    """Get category matches based off a FOIA description."""

    # Some of these are split()'d because they were written Excel
    # rather than being hard-coded into the program, like it is now.
    #
    # There is a better way to do this but because we only have a week,
    # this is the only "good" way without putting in a *lot* of effort.
    categories = {
        "Video - Locomotive": "dashcam,dash cam".split(","),
        "Video - Surveillance/APD": "video,body cam,surveillance".split(","),
        "Lawsuits": "lawsuit,lawsuits,law suit,law suits".split(","),
        "Amtrak PD": "police reports,police,use-of-force".split(","),
        "Audits": ["OIG", "Office of the Inspector General"],
        "Claims": ["baggage claim", "claims"],
        "Employee Medical Records": ["medical disqualification"],
        "Procurement": "procurement,solicitation".split(","),
        "Train Fares": "fee,fees".split(","),
        "Ridership Statistics, Station Ridership Data": ["statistics"],
        "Noise Assessments": "noise assessment,noise assessments".split(","),
        "Central Reporting": "accident,incident,train incident,train accident".split(
            ","
        ),
        "Contract Management": "bid,bid solicitation,contracts,contractors,contract,contactor".split(
            ","
        ),
        "Comptroller/Finance": "financial,finance".split(","),
        "Email Searches (eDiscovery)": ["emails", "internal emails"],
        "Telephone Records": ["telephone"],
        "Train Scheduling": ["train delays", "delays", "delay"],
    }

    v_adjectives = []
    for word in foia_description.split(" "):
        for adj, keywords in categories.items():
            if word in keywords:
                if adj not in v_adjectives:
                    v_adjectives.append(adj)

        # print(foia_description)
        # v_adjectives.append([adjective, foia_id])

    # If we don't have any adjectives, the report is not known.
    if len(v_adjectives) < 1:
        v_adjectives.append("Unknown")

    return v_adjectives

    # departments = open(DEPARTMENTS_FILE, "r")
    # for entry in departments:
    #     print(entry)


def main(data):
    """
    This script is responsible for classifying each request with
    the appropriate category based on keywords that specified below.
    Each keyword corresponds with a specific "category" (department)
    that is equipped with handling said report
    """
    foias = open(data, "r")
    reader = csv.reader(foias, delimiter=",")
    for row in reader:
        print(f"{row[0]} {match_categories(row[1])}")
    # match_category("hi")
    # return categories


main(REQUESTS_FILE)
