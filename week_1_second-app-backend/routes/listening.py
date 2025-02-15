from flask import Blueprint, jsonify, request
from db import get_db

listening_blueprint = Blueprint('listening', __name__)

@listening_blueprint.route("/", methods=["GET"])
def get_listening_exercises():
    db = get_db()
    cur = db.execute("SELECT id, title, audio_url, transcript, questions FROM listening_exercises")
    exercises = cur.fetchall()
    return jsonify([dict(ex) for ex in exercises]), 200

@listening_blueprint.route("/", methods=["POST"])
def add_listening_exercise():
    exercise_data = request.get_json()
    if "title" not in exercise_data or "audio_url" not in exercise_data:
        return jsonify({"error": "Title and audio URL are required"}), 400
    transcript = exercise_data.get("transcript", "")
    questions = exercise_data.get("questions", "")
    db = get_db()
    db.execute("INSERT INTO listening_exercises (title, audio_url, transcript, questions) VALUES (?, ?, ?, ?)",
               (exercise_data["title"], exercise_data["audio_url"], transcript, questions))
    db.commit()
    return jsonify({"message": "Listening exercise added successfully."}), 201

@listening_blueprint.route("/<int:exercise_id>", methods=["PUT"])
def update_listening_exercise(exercise_id):
    exercise_data = request.get_json()
    db = get_db()
    db.execute("UPDATE listening_exercises SET title=?, audio_url=?, transcript=?, questions=? WHERE id=?",
               (exercise_data.get("title"), exercise_data.get("audio_url"), exercise_data.get("transcript"), exercise_data.get("questions", ""), exercise_id))
    db.commit()
    return jsonify({"message": "Listening exercise updated successfully."}), 200

@listening_blueprint.route("/<int:exercise_id>", methods=["DELETE"])
def delete_listening_exercise(exercise_id):
    db = get_db()
    db.execute("DELETE FROM listening_exercises WHERE id=?", (exercise_id,))
    db.commit()
    return jsonify({"message": "Listening exercise deleted successfully."}), 200
