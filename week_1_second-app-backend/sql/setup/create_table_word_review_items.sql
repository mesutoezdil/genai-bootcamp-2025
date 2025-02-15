DROP TABLE IF EXISTS word_review_items;
CREATE TABLE word_review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER,
    question TEXT,
    user_answer TEXT,
    correct_answer TEXT,
    is_correct INTEGER,
    FOREIGN KEY (review_id) REFERENCES word_reviews(id)
);
