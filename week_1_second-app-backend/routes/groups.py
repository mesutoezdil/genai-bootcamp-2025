from flask import Blueprint, jsonify, request
from db import get_db

groups_blueprint = Blueprint('groups', __name__)

@groups_blueprint.route("/", methods=["GET"])
def get_groups():
    db = get_db()
    cur = db.execute("SELECT id, group_name, description FROM word_groups")
    groups = cur.fetchall()
    return jsonify([dict(group) for group in groups]), 200

@groups_blueprint.route("/", methods=["POST"])
def add_group():
    group_data = request.get_json()
    if "group_name" not in group_data:
        return jsonify({"error": "Group name is required"}), 400
    description = group_data.get("description", "")
    db = get_db()
    db.execute("INSERT INTO word_groups (group_name, description) VALUES (?, ?)", (group_data["group_name"], description))
    db.commit()
    return jsonify({"message": "Group added successfully."}), 201

@groups_blueprint.route("/<int:group_id>", methods=["PUT"])
def update_group(group_id):
    group_data = request.get_json()
    db = get_db()
    db.execute("UPDATE word_groups SET group_name=?, description=? WHERE id=?", (group_data.get("group_name"), group_data.get("description"), group_id))
    db.commit()
    return jsonify({"message": "Group updated successfully."}), 200

@groups_blueprint.route("/<int:group_id>", methods=["DELETE"])
def delete_group(group_id):
    db = get_db()
    db.execute("DELETE FROM word_groups WHERE id=?", (group_id,))
    db.commit()
    return jsonify({"message": "Group deleted successfully."}), 200
