from flask import Blueprint, jsonify, request
from db import get_db

sessions_blueprint = Blueprint('sessions', __name__)

@sessions_blueprint.route("/", methods=["GET"])
def get_sessions():
    db = get_db()
    cur = db.execute("SELECT id, session_date, progress, notes FROM study_sessions")
    sessions = cur.fetchall()
    return jsonify([dict(session) for session in sessions]), 200

@sessions_blueprint.route("/", methods=["POST"])
def add_session():
    session_data = request.get_json()
    if "session_date" not in session_data:
        return jsonify({"error": "session_date is required"}), 400
    progress = session_data.get("progress", 0)
    notes = session_data.get("notes", "")
    db = get_db()
    db.execute("INSERT INTO study_sessions (session_date, progress, notes) VALUES (?, ?, ?)",
               (session_data["session_date"], progress, notes))
    db.commit()
    return jsonify({"message": "Session added successfully."}), 201

@sessions_blueprint.route("/<int:session_id>", methods=["PUT"])
def update_session(session_id):
    session_data = request.get_json()
    db = get_db()
    db.execute("UPDATE study_sessions SET session_date=?, progress=?, notes=? WHERE id=?",
               (session_data.get("session_date"), session_data.get("progress"), session_data.get("notes"), session_id))
    db.commit()
    return jsonify({"message": "Session updated successfully."}), 200

@sessions_blueprint.route("/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    db = get_db()
    db.execute("DELETE FROM study_sessions WHERE id=?", (session_id,))
    db.commit()
    return jsonify({"message": "Session deleted successfully."}), 200