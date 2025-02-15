import sqlite3
from flask import current_app, g

DATABASE = 'chinese_learning.db'

def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(DATABASE)
        g._database.row_factory = sqlite3.Row
    return g._database

def init_db():
    """Initializes the database with extended tables for the Chinese Learning App."""
    db = get_db()
    # Execute migration scripts (order matters)
    migration_files = [
        'seeds/create_table_words.sql',
        'seeds/create_table_word_reviews.sql',
        'seeds/create_table_word_review_items.sql',
        'seeds/create_table_word_groups.sql',
        'seeds/create_table_study_sessions.sql',
        'seeds/create_table_study_activities.sql',
        'seeds/create_table_groups.sql',
        'seeds/create_table_grammar.sql',
        'seeds/create_table_listening.sql',
        'seeds/create_table_reading.sql',
        'seeds/create_table_writing.sql'
    ]
    for file in migration_files:
        with current_app.open_resource(file, mode='r') as f:
            db.executescript(f.read())
    # Insert seed data
    seed_files = [
        'seeds/insert_study_activities.sql',
        'seeds/insert_grammar_lessons.sql',
        'seeds/insert_listening_exercises.sql',
        'seeds/insert_reading_passages.sql',
        'seeds/insert_writing_assignments.sql'
    ]
    for file in seed_files:
        with current_app.open_resource(file, mode='r') as f:
            db.executescript(f.read())
    db.commit()

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
