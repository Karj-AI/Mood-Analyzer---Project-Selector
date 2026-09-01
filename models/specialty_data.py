"""
The very first question the user sees, before the mood quiz.
Value must match the 'specialty' field used in project banks
(e.g. software_projects.py, security_projects.py, etc).
"""

SPECIALTIES = [
    {"id": "software", "label": "Software Development"},
    {"id": "security", "label": "Cybersecurity"},
    {"id": "data", "label": "Power BI + SQL / Data"},
    {"id": "azure", "label": "Azure / Cloud"},
    {"id": "gaming", "label": "Game Development"},
]


def choose_specialty_terminal():
    print("What's your specialty?")
    for i, s in enumerate(SPECIALTIES, start=1):
        print(f"  {i}. {s['label']}")

    choice = None
    while choice is None:
        raw = input("Pick a number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(SPECIALTIES):
            choice = int(raw)
        else:
            print("Not a valid option, try again.")

    return SPECIALTIES[choice - 1]["id"]