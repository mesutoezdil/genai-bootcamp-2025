DROP TABLE IF EXISTS words;
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character TEXT NOT NULL,
    pinyin TEXT NOT NULL,
    english TEXT NOT NULL,
    simplified TEXT,
    traditional TEXT,
    example TEXT
);
