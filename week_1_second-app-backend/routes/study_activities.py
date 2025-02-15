from flask import Blueprint, jsonify, request
from db import get_db

activities_blueprint = Blueprint('activities', __name__)

@activities_blueprint.route("/", methods=["GET"])
def get_activities():
    db = get_db()
    cur = db.execute("SELECT id, name, url, preview_url, description FROM study_activities")
    activities = cur.fetchall()
    return jsonify([dict(activity) for activity in activities]), 200

@activities_blueprint.route("/", methods=["POST"])
def add_activity():
    activity_data = request.get_json()
    if "name" not in activity_data:
        return jsonify({"error": "Activity name is required"}), 400
    description = activity_data.get("description", "")
    db = get_db()
    db.execute("INSERT INTO study_activities (name, url, preview_url, description) VALUES (?, ?, ?, ?)",
               (activity_data.get("name"), activity_data.get("url"), activity_data.get("preview_url"), description))
    db.commit()
    return jsonify({"message": "Activity added successfully."}), 201

@activities_blueprint.route("/<int:activity_id>", methods=["PUT"])
def update_activity(activity_id):
    activity_data = request.get_json()
    db = get_db()
    db.execute("UPDATE study_activities SET name=?, url=?, preview_url=?, description=? WHERE id=?",
               (activity_data.get("name"), activity_data.get("url"), activity_data.get("preview_url"), activity_data.get("description", ""), activity_id))
    db.commit()
    return jsonify({"message": "Activity updated successfully."}), 200

@activities_blueprint.route("/<int:activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    db = get_db()
    db.execute("DELETE FROM study_activities WHERE id=?", (activity_id,))
    db.commit()
    return jsonify({"message": "Activity deleted successfully."}), 200
