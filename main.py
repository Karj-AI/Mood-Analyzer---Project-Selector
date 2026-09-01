"""
Terminal-only test harness. No Flask, no React.
Run with: python main.py
Walks you through the 7 questions, calculates your mood, filters projects
by difficulty and mood fit, then randomly picks one like the wheel will.
"""

from models.quiz_data import QUESTIONS
from models.mood_axes import describe_mood
from models.specialty_data import choose_specialty_terminal
from models.software_projects import SOFTWARE_PROJECTS
from models.security_projects import SECURITY_PROJECTS
from models.data_projects import DATA_PROJECTS
from models.azure_projects import AZURE_PROJECTS
from models.gaming_projects import GAMING_PROJECTS
from logic.scoring import calculate_mood
from logic.matcher import get_candidates, spin_wheel
from analytics.tracker import log_pick, log_completion, print_summary

PROJECT_BANKS = {
    "software": SOFTWARE_PROJECTS,
    "security": SECURITY_PROJECTS,
    "data": DATA_PROJECTS,
    "azure": AZURE_PROJECTS,
    "gaming": GAMING_PROJECTS,
}


def run_quiz():
    selected_effects = []

    print("=== Mood Check ===\n")
    for question in QUESTIONS:
        print(question["text"])
        for i, option in enumerate(question["options"], start=1):
            print(f"  {i}. {option['label']}")

        choice = None
        while choice is None:
            raw = input("Pick a number: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(question["options"]):
                choice = int(raw)
            else:
                print("Not a valid option, try again.")

        selected_effects.append(question["options"][choice - 1]["effect"])
        print()

    return selected_effects


def choose_difficulty():
    valid = ["easy", "medium", "hard"]
    print("Pick a difficulty: easy / medium / hard")
    while True:
        raw = input("> ").strip().lower()
        if raw in valid:
            return raw
        print("Type one of: easy, medium, hard")


def main():
    specialty = choose_specialty_terminal()
    projects = PROJECT_BANKS.get(specialty)

    if not projects:
        print(f"\nNo project bank yet for '{specialty}'.")
        return

    print()
    selected_effects = run_quiz()
    mood_vector = calculate_mood(selected_effects)

    print("=== Your Mood ===")
    print(mood_vector)
    print(describe_mood(mood_vector))
    print()

    difficulty = choose_difficulty()
    candidates = get_candidates(mood_vector, difficulty, projects, pool_size=5)

    if not candidates:
        print(f"\nNo projects found at difficulty '{difficulty}' for '{specialty}'.")
        return

    print(f"\n=== Candidate Pool ({len(candidates)}) ===")
    for p in candidates:
        print(f"- {p['title']}")

    result = spin_wheel(candidates)

    print("\n=== The wheel landed on ===")
    print(f"{result['title']}")
    print(result["description"])
    print(f"Tech stack: {', '.join(result['tech_stack'])}")
    print("Steps:")
    for step in result["steps"]:
        print(f"  - {step}")
    print("Stretch goals:")
    for goal in result["stretch_goals"]:
        print(f"  - {goal}")

    log_pick(specialty, mood_vector, difficulty, result["id"], result["title"])

    done = input("\nDid you complete this project? (y/n): ").strip().lower()
    if done == "y":
        log_completion(result["id"], result["title"])
        print("Nice work, logged as completed.")


if __name__ == "__main__":
    main()
    view_stats = input("\nView analytics summary? (y/n): ").strip().lower()
    if view_stats == "y":
        print_summary()