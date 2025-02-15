DROP TABLE IF EXISTS grammar_lessons;
CREATE TABLE grammar_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    examples TEXT
);