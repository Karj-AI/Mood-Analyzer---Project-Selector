"""
Flask API for the mood project picker.
Run with: python app.py
Endpoints:
  GET  /api/specialties        -> list of specialties
  GET  /api/quiz                -> list of quiz questions
  POST /api/submit-quiz         -> body: {specialty, answer_indexes, difficulty}
  GET  /api/history              -> recent picks with completion status
  POST /api/complete             -> body: {project_id, project_title}
"""
from flask import Flask, jsonify, request

from models.specialty_data import SPECIALTIES
from models.quiz_data import QUESTIONS
from models.software_projects import SOFTWARE_PROJECTS
from models.security_projects import SECURITY_PROJECTS
from models.data_projects import DATA_PROJECTS
from models.azure_projects import AZURE_PROJECTS
from models.gaming_projects import GAMING_PROJECTS
from logic.scoring import calculate_mood
from logic.matcher import get_candidates, spin_wheel, describe_match_reason
from models.mood_axes import describe_mood
from analytics.tracker import log_pick, log_completion, get_history

app = Flask(__name__)

PROJECT_BANKS = {
    "software": SOFTWARE_PROJECTS,
    "security": SECURITY_PROJECTS,
    "data": DATA_PROJECTS,
    "azure": AZURE_PROJECTS,
    "gaming": GAMING_PROJECTS,
}


@app.route("/api/specialties", methods=["GET"])
def get_specialties():
    return jsonify(SPECIALTIES)


@app.route("/api/quiz", methods=["GET"])
def get_quiz():
    public_questions = []
    for q in QUESTIONS:
        public_questions.append({
            "id": q["id"],
            "text": q["text"],
            "options": [{"label": opt["label"]} for opt in q["options"]],
        })
    return jsonify(public_questions)


@app.route("/api/submit-quiz", methods=["POST"])
def submit_quiz():
    data = request.get_json(force=True)

    specialty = data.get("specialty")
    answer_indexes = data.get("answer_indexes")
    difficulty = data.get("difficulty")

    if specialty not in PROJECT_BANKS:
        return jsonify({"error": f"Unknown specialty '{specialty}'"}), 400

    if difficulty not in ("easy", "medium", "hard"):
        return jsonify({"error": f"Invalid difficulty '{difficulty}'"}), 400

    if not isinstance(answer_indexes, list) or len(answer_indexes) != len(QUESTIONS):
        return jsonify({"error": f"Expected {len(QUESTIONS)} answer_indexes"}), 400

    selected_effects = []
    for question, choice_index in zip(QUESTIONS, answer_indexes):
        options = question["options"]
        if not isinstance(choice_index, int) or not (0 <= choice_index < len(options)):
            return jsonify({"error": f"Invalid option index for question '{question['id']}'"}), 400
        selected_effects.append(options[choice_index]["effect"])

    mood_vector = calculate_mood(selected_effects)
    projects = PROJECT_BANKS[specialty]
    candidates = get_candidates(mood_vector, difficulty, projects, pool_size=5)

    if not candidates:
        return jsonify({"error": f"No projects found for '{specialty}' at difficulty '{difficulty}'"}), 404

    result = spin_wheel(candidates, mood_vector)
    reason = describe_match_reason(mood_vector, result)

    log_pick(specialty, mood_vector, difficulty, result["id"], result["title"])

    return jsonify({
        "mood_vector": mood_vector,
        "mood_description": describe_mood(mood_vector),
        "candidates": [{"id": p["id"], "title": p["title"]} for p in candidates],
        "result": result,
        "reason": reason,
    })


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(get_history())


@app.route("/api/complete", methods=["POST"])
def complete():
    data = request.get_json(force=True)
    project_id = data.get("project_id")
    project_title = data.get("project_title")

    if not project_id or not project_title:
        return jsonify({"error": "project_id and project_title required"}), 400

    log_completion(project_id, project_title)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run()
