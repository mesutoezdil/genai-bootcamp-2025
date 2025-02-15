from flask import Blueprint, jsonify, request
from db import get_db

reading_blueprint = Blueprint('reading', __name__)

@reading_blueprint.route("/", methods=["GET"])
def get_reading_passages():
    db = get_db()
    cur = db.execute("SELECT id, title, content, vocabulary FROM reading_passages")
    passages = cur.fetchall()
    return jsonify([dict(passage) for passage in passages]), 200

@reading_blueprint.route("/", methods=["POST"])
def add_reading_passage():
    passage_data = request.get_json()
    if "title" not in passage_data or "content" not in passage_data:
        return jsonify({"error": "Title and content are required"}), 400
    vocabulary = passage_data.get("vocabulary", "")
    db = get_db()
    db.execute("INSERT INTO reading_passages (title, content, vocabulary) VALUES (?, ?, ?)",
               (passage_data["title"], passage_data["content"], vocabulary))
    db.commit()
    return jsonify({"message": "Reading passage added successfully."}), 201

@reading_blueprint.route("/<int:passage_id>", methods=["PUT"])
def update_reading_passage(passage_id):
    passage_data = request.get_json()
    db = get_db()
    db.execute("UPDATE reading_passages SET title=?, content=?, vocabulary=? WHERE id=?",
               (passage_data.get("title"), passage_data.get("content"), passage_data.get("vocabulary", ""), passage_id))
    db.commit()
    return jsonify({"message": "Reading passage updated successfully."}), 200

@reading_blueprint.route("/<int:passage_id>", methods=["DELETE"])
def delete_reading_passage(passage_id):
    db = get_db()
    db.execute("DELETE FROM reading_passages WHERE id=?", (passage_id,))
    db.commit()
    return jsonify({"message": "Reading passage deleted successfully."}), 200
