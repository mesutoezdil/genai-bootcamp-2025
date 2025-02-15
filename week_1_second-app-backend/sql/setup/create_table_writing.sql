DROP TABLE IF EXISTS writing_assignments;
CREATE TABLE writing_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT NOT NULL,
    submission TEXT,
    feedback TEXT
);
