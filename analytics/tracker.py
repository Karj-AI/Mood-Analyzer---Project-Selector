"""
Simple local analytics tracker. No database needed yet — logs to a JSON
file so you can show 'most selected moods' and 'most completed projects'
(Option B from the original brainstorm) without extra setup.
"""
import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "activity_log.json")


def _load_log():
    if not os.path.exists(LOG_FILE):
        return {"picks": [], "completions": []}
    with open(LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"picks": [], "completions": []}


def _save_log(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_pick(specialty, mood_vector, difficulty, project_id, project_title):
    """Call this right after the wheel lands on a project."""
    data = _load_log()
    data["picks"].append({
        "timestamp": datetime.now().isoformat(),
        "specialty": specialty,
        "mood_vector": mood_vector,
        "difficulty": difficulty,
        "project_id": project_id,
        "project_title": project_title,
    })
    _save_log(data)


def log_completion(project_id, project_title):
    """Call this when the user marks a project as completed."""
    data = _load_log()
    data["completions"].append({
        "timestamp": datetime.now().isoformat(),
        "project_id": project_id,
        "project_title": project_title,
    })
    _save_log(data)


def most_selected_moods(top_n=3):
    """Returns the most common 'describe_mood' style dimension leanings from picks."""
    data = _load_log()
    counts = {}
    for pick in data["picks"]:
        mv = pick["mood_vector"]
        key = tuple(sorted(mv.items()))
        counts[key] = counts.get(key, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return ranked[:top_n]


def most_completed_projects(top_n=5):
    data = _load_log()
    counts = {}
    for c in data["completions"]:
        title = c["project_title"]
        counts[title] = counts.get(title, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return ranked[:top_n]


def get_history(limit=50):
    """Returns picks (most recent first) with a 'completed' flag attached,
    for the frontend's history/save view."""
    data = _load_log()
    completed_ids = {c["project_id"] for c in data["completions"]}

    history = []
    for pick in reversed(data["picks"][-limit:]):
        history.append({
            **pick,
            "completed": pick["project_id"] in completed_ids,
        })
    return history


def print_summary():
    print("\n=== Analytics Summary ===")
    print("Most common mood picks:")
    for mood, count in most_selected_moods():
        print(f"  {dict(mood)} — picked {count}x")

    print("Most completed projects:")
    for title, count in most_completed_projects():
        print(f"  {title} — completed {count}x")