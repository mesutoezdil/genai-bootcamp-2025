import sqlite3
from typing import Dict, List
from pathlib import Path
import pytest
import os

class Database:
    def __init__(self, db_path: str = "words.db"):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_word(self, simplified: str, pinyin: str, english: str, parts: Dict = None) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO words (simplified, pinyin, english, parts) VALUES (?, ?, ?, ?)",
                (simplified, pinyin, english, str(parts) if parts else None)
            )
            return cursor.lastrowid

    def get_words(self) -> List[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, simplified, pinyin, english, parts FROM words")
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "simplified": row[1],
                    "pinyin": row[2],
                    "english": row[3],
                    "parts": row[4]
                }
                for row in rows
            ]

    def create_group(self, name: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO groups (name) VALUES (?)", (name,))
            return cursor.lastrowid

    def add_word_to_group(self, word_id: int, group_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO word_groups (word_id, group_id) VALUES (?, ?)",
                (word_id, group_id)
            )

    def create_study_session(self, group_id: int) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO study_sessions (group_id) VALUES (?)",
                (group_id,)
            )
            return cursor.lastrowid

    def record_word_review(self, word_id: int, study_session_id: int, correct: bool):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO word_review_items 
                   (word_id, study_session_id, correct) 
                   VALUES (?, ?, ?)""",
                (word_id, study_session_id, correct)
            )

@pytest.fixture
def db():
    test_db = "test_words.db"
    # Setup test database
    with open("migrations/001_initial_schema.sql") as f:
        schema = f.read()
    db = Database(test_db)
    with db.get_connection() as conn:
        conn.executescript(schema)
    yield db
    # Cleanup
    os.remove(test_db)

def test_add_word(db):
    word_id = db.add_word("你好", "nǐ hǎo", "hello")
    assert word_id > 0
    words = db.get_words()
    assert len(words) == 1
    assert words[0]["simplified"] == "你好"
