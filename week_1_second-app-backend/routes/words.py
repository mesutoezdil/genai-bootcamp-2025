from flask import Blueprint, jsonify, request
from db import get_db

words_blueprint = Blueprint('words', __name__)

@words_blueprint.route("/", methods=["GET"])
def get_words():
    db = get_db()
    cur = db.execute("SELECT id, character, pinyin, english, simplified, traditional, example FROM words")
    words = cur.fetchall()
    return jsonify([dict(word) for word in words]), 200

@words_blueprint.route("/", methods=["POST"])
def add_word():
    new_word = request.get_json()
    required_fields = ["character", "pinyin", "english"]
    if not all(field in new_word for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    simplified = new_word.get("simplified", new_word["character"])
    traditional = new_word.get("traditional", new_word["character"])
    example = new_word.get("example", "")
    db = get_db()
    db.execute(
        "INSERT INTO words (character, pinyin, english, simplified, traditional, example) VALUES (?, ?, ?, ?, ?, ?)",
        (new_word["character"], new_word["pinyin"], new_word["english"], simplified, traditional, example)
    )
    db.commit()
    return jsonify({"message": "Word added successfully."}), 201

@words_blueprint.route("/<int:word_id>", methods=["PUT"])
def update_word(word_id):
    update_data = request.get_json()
    db = get_db()
    db.execute(
        "UPDATE words SET character=?, pinyin=?, english=?, simplified=?, traditional=?, example=? WHERE id=?",
        (
            update_data.get("character"),
            update_data.get("pinyin"),
            update_data.get("english"),
            update_data.get("simplified", update_data.get("character")),
            update_data.get("traditional", update_data.get("character")),
            update_data.get("example", ""),
            word_id
        )
    )
    db.commit()
    return jsonify({"message": "Word updated successfully."}), 200

@words_blueprint.route("/<int:word_id>", methods=["DELETE"])
def delete_word(word_id):
    db = get_db()
    db.execute("DELETE FROM words WHERE id=?", (word_id,))
    db.commit()
    return jsonify({"message": "Word deleted successfully."}), 200