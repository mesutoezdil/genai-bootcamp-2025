from flask import Blueprint, jsonify, request
from db import get_db

writing_blueprint = Blueprint('writing', __name__)

@writing_blueprint.route("/", methods=["GET"])
def get_writing_assignments():
    db = get_db()
    cur = db.execute("SELECT id, prompt, submission, feedback FROM writing_assignments")
    assignments = cur.fetchall()
    return jsonify([dict(assignment) for assignment in assignments]), 200

@writing_blueprint.route("/", methods=["POST"])
def add_writing_assignment():
    assignment_data = request.get_json()
    if "prompt" not in assignment_data:
        return jsonify({"error": "Prompt is required"}), 400
    submission = assignment_data.get("submission", "")
    feedback = assignment_data.get("feedback", "")
    db = get_db()
    db.execute("INSERT INTO writing_assignments (prompt, submission, feedback) VALUES (?, ?, ?)",
               (assignment_data["prompt"], submission, feedback))
    db.commit()
    return jsonify({"message": "Writing assignment added successfully."}), 201

@writing_blueprint.route("/<int:assignment_id>", methods=["PUT"])
def update_writing_assignment(assignment_id):
    assignment_data = request.get_json()
    db = get_db()
    db.execute("UPDATE writing_assignments SET prompt=?, submission=?, feedback=? WHERE id=?",
               (assignment_data.get("prompt"), assignment_data.get("submission"), assignment_data.get("feedback", ""), assignment_id))
    db.commit()
    return jsonify({"message": "Writing assignment updated successfully."}), 200

@writing_blueprint.route("/<int:assignment_id>", methods=["DELETE"])
def delete_writing_assignment(assignment_id):
    db = get_db()
    db.execute("DELETE FROM writing_assignments WHERE id=?", (assignment_id,))
    db.commit()
    return jsonify({"message": "Writing assignment deleted successfully."}), 200
