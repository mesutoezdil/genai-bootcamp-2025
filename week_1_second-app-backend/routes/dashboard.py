from flask import Blueprint, jsonify
from db import get_db

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route("/", methods=["GET"])
def get_dashboard():
    db = get_db()
    word_count = db.execute("SELECT COUNT(*) as count FROM words").fetchone()["count"]
    session_count = db.execute("SELECT COUNT(*) as count FROM study_sessions").fetchone()["count"]
    activity_count = db.execute("SELECT COUNT(*) as count FROM study_activities").fetchone()["count"]
    group_count = db.execute("SELECT COUNT(*) as count FROM word_groups").fetchone()["count"]
    grammar_count = db.execute("SELECT COUNT(*) as count FROM grammar_lessons").fetchone()["count"]
    listening_count = db.execute("SELECT COUNT(*) as count FROM listening_exercises").fetchone()["count"]
    reading_count = db.execute("SELECT COUNT(*) as count FROM reading_passages").fetchone()["count"]
    writing_count = db.execute("SELECT COUNT(*) as count FROM writing_assignments").fetchone()["count"]

    avg_progress_row = db.execute("SELECT AVG(progress) as avg_progress FROM study_sessions").fetchone()
    avg_progress = avg_progress_row["avg_progress"] if avg_progress_row["avg_progress"] is not None else 0

    return jsonify({
        "total_words": word_count,
        "total_sessions": session_count,
        "total_activities": activity_count,
        "total_groups": group_count,
        "total_grammar_lessons": grammar_count,
        "total_listening_exercises": listening_count,
        "total_reading_passages": reading_count,
        "total_writing_assignments": writing_count,
        "average_progress": avg_progress,
        "message": "Keep going – your Chinese learning journey is truly epic!"
    }), 200
