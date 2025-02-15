DROP TABLE IF EXISTS study_sessions;
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_date TEXT NOT NULL,
    progress INTEGER DEFAULT 0,
    notes TEXT
);
