# Chinese Learning App - Extended Edition

Welcome to the most comprehensive Chinese learning tool ever built! This application is designed to support every aspect of learning Chinese, including:

- Vocabulary (words with character, pinyin, English meaning, and examples)
- Study sessions with progress tracking and notes
- Interactive study activities (e.g., character writing and pinyin practice)
- Grouping of words by themes (e.g., Food, Travel, etc.)
- Grammar lessons with detailed explanations and examples
- Listening exercises with audio support and comprehension questions
- Reading passages with annotations and vocabulary highlights
- Writing assignments with prompts and submission tracking

## Setup Instructions

### 1. Install Dependencies
```sh
pip install -r requirements.txt

chinese-learning-app/
├── app.py
├── db.py
├── tasks.py
├── migrate.py
├── requirements.txt
├── Readme.md
├── words.py
├── study_sessions.py
├── study_activities.py
├── groups.py
├── dashboard.py
├── grammar.py
├── listening.py
├── reading.py
├── writing.py
├── assets/               # For images, audio, etc.
├── seeds/
│   ├── create_table_words.sql
│   ├── create_table_word_reviews.sql
│   ├── create_table_word_review_items.sql
│   ├── create_table_word_groups.sql
│   ├── create_table_study_sessions.sql
│   ├── create_table_study_activities.sql
│   ├── create_table_groups.sql
│   ├── create_table_grammar.sql
│   ├── create_table_listening.sql
│   ├── create_table_reading.sql
│   ├── create_table_writing.sql
│   ├── insert_study_activities.sql
│   ├── insert_grammar_lessons.sql
│   ├── insert_listening_exercises.sql
│   ├── insert_reading_passages.sql
│   └── insert_writing_assignments.sql
└── data/
    ├── study_activities.json
    ├── data_verbs.json
    ├── data_adjectives.json
    ├── grammar_lessons.json
    ├── listening_exercises.json
    ├── reading_passages.json
    └── writing_assignments.json


