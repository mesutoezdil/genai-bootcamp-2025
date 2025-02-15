DROP TABLE IF EXISTS reading_passages;
CREATE TABLE reading_passages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    vocabulary TEXT
);
