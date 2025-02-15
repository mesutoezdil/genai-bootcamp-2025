DROP TABLE IF EXISTS word_groups;
CREATE TABLE word_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL,
    description TEXT
);
