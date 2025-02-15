DROP TABLE IF EXISTS listening_exercises;
CREATE TABLE listening_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    audio_url TEXT NOT NULL,
    transcript TEXT,
    questions TEXT
);
