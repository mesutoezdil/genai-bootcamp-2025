DROP TABLE IF EXISTS word_reviews;
CREATE TABLE word_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER,
    review_date TEXT,
    score INTEGER,
    FOREIGN KEY (word_id) REFERENCES words(id)
);
