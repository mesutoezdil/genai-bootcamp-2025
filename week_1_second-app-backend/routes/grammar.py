from flask import Blueprint, jsonify, request
from db import get_db

grammar_blueprint = Blueprint('grammar', __name__)

@grammar_blueprint.route("/", methods=["GET"])
def get_grammar_lessons():
    db = get_db()
    cur = db.execute("SELECT id, title, content, examples FROM grammar_lessons")
    lessons = cur.fetchall()
    return jsonify([dict(lesson) for lesson in lessons]), 200

@grammar_blueprint.route("/", methods=["POST"])
def add_grammar_lesson():
    lesson_data = request.get_json()
    if "title" not in lesson_data or "content" not in lesson_data:
        return jsonify({"error": "Title and content are required"}), 400
    examples = lesson_data.get("examples", "")
    db = get_db()
    db.execute("INSERT INTO grammar_lessons (title, content, examples) VALUES (?, ?, ?)",
               (lesson_data["title"], lesson_data["content"], examples))
    db.commit()
    return jsonify({"message": "Grammar lesson added successfully."}), 201

@grammar_blueprint.route("/<int:lesson_id>", methods=["PUT"])
def update_grammar_lesson(lesson_id):
    lesson_data = request.get_json()
    db = get_db()
    db.execute("UPDATE grammar_lessons SET title=?, content=?, examples=? WHERE id=?",
               (lesson_data.get("title"), lesson_data.get("content"), lesson_data.get("examples", ""), lesson_id))
    db.commit()
    return jsonify({"message": "Grammar lesson updated successfully."}), 200

@grammar_blueprint.route("/<int:lesson_id>", methods=["DELETE"])
def delete_grammar_lesson(lesson_id):
    db = get_db()
    db.execute("DELETE FROM grammar_lessons WHERE id=?", (lesson_id,))
    db.commit()
    return jsonify({"message": "Grammar lesson deleted successfully."}), 200
