DROP TABLE IF EXISTS study_activities;
CREATE TABLE study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT,
    preview_url TEXT,
    description TEXT
);
