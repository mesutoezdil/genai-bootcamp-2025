# Chinese Learning App - Extended Edition

Welcome to the **most comprehensive Chinese learning tool** ever built! This application seamlessly integrates **vocabulary building**, **study sessions**, **interactive exercises**, and **progress tracking** into a single platform. Whether you are a complete beginner or an advanced learner, this app provides an all-encompassing resource for mastering written and spoken Chinese.

---

## Table of Contents

1. [Introduction & Key Features](#1-introduction--key-features)  
2. [Application Architecture](#2-application-architecture)  
3. [Project Structure](#3-project-structure)  
4. [Setup & Installation](#4-setup--installation)  
5. [Seed Scripts & Database Initialization](#5-seed-scripts--database-initialization)  
6. [Core Modules & Functionalities](#6-core-modules--functionalities)  
   1. [Vocabulary (words.py)](#61-vocabulary-wordspy)  
   2. [Study Sessions (study_sessions.py)](#62-study-sessions-study_sessionspy)  
   3. [Interactive Activities (study_activities.py)](#63-interactive-activities-study_activitiespy)  
   4. [Word Grouping (groups.py)](#64-word-grouping-groupspy)  
   5. [Grammar Lessons (grammar.py)](#65-grammar-lessons-grammarpy)  
   6. [Listening Exercises (listening.py)](#66-listening-exercises-listeningpy)  
   7. [Reading Passages (reading.py)](#67-reading-passages-readingpy)  
   8. [Writing Assignments (writing.py)](#68-writing-assignments-writingpy)  
7. [Additional Scripts](#7-additional-scripts)  
8. [Assets & Data](#8-assets--data)  
9. [Contributing](#9-contributing)  
10. [Future Enhancements](#10-future-enhancements)  

---

## 1. Introduction & Key Features

1. **Vocabulary Mastery**  
   - Each word entry includes **characters**, **pinyin**, **English meaning**, and **usage examples**.  
   - Organized by grammar category (verbs, adjectives, etc.) and skill level.

2. **Study Sessions & Tracking**  
   - Log your daily progress, record personal notes, and maintain a reflective learning journal.  
   - Scorecards or dashboards display performance over time.

3. **Interactive Exercises**  
   - **Character writing** practice and **pinyin** matching.  
   - Timed quizzes and spaced repetition to reinforce new words.

4. **Word Grouping & Thematic Studies**  
   - Group words by themes (Food, Travel, etc.) for more context-based learning.  
   - Additional grouping for HSK levels or custom user-defined categories.

5. **Grammar Lessons**  
   - Detailed explanations, usage notes, and real-life examples.  
   - Linked practice questions to reinforce grammar points.

6. **Listening Exercises**  
   - Audio recordings with comprehension questions.  
   - Difficulty-based modules that adapt to your progress.

7. **Reading Passages**  
   - Texts with inline annotations, pinyin toggles, and vocabulary highlights.  
   - Interactive reading comprehension checkpoints.

8. **Writing Assignments**  
   - Practice prompts with submission tracking and teacher/peer feedback in mind.

---

## 2. Application Architecture

This application is designed with **modularity** and **extensibility** in mind:

- **App Entry (`app.py`)**  
  The main entry point that ties together routes or CLI commands, depending on your setup.
- **Database Layer (`db.py`)**  
  Central point for establishing connections (e.g., SQLite, PostgreSQL) and running queries.
- **Migration Script (`migrate.py`)**  
  Handles database creation or updates (schema migrations).
- **Task Scripts (`tasks.py` and others)**  
  For scheduled tasks (e.g., nightly updates, data cleaning, or batch processes).

---

## 3. Project Structure

A recommended folder layout:

```plaintext
chinese-learning-app/
├── app.py                  # Main application script
├── db.py                   # Database utilities and connection logic
├── tasks.py                # Background or scheduled tasks
├── migrate.py              # Database migration/init script
├── requirements.txt        # Python dependencies
├── Readme.md               # Main documentation (this file)
├── words.py                # Vocabulary management
├── study_sessions.py       # Study sessions logic
├── study_activities.py     # Interactive study module (character writing, pinyin practice)
├── groups.py               # Word groupings (themes, categories)
├── dashboard.py            # Progress tracking & dashboards
├── grammar.py              # Grammar lessons, usage examples
├── listening.py            # Listening exercises & audio handling
├── reading.py              # Reading passages with annotations
├── writing.py              # Writing prompts & submission tracking
├── assets/                 # Images, audio files, etc.
├── seeds/                  # SQL scripts for table creation & data seeding
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
│   └── create_table_writing.sql
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
```

> **Tip**: You may adapt or expand this structure for frameworks like Flask (web routing) or Celery (advanced tasks).

---

## 4. Setup & Installation

1. **Clone the Repository**  
   ```bash
   git clone <repository_url>
   cd chinese-learning-app
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**  
   - Update `db.py` with your database details (SQLite, PostgreSQL, etc.).  
   - Alternatively, use environment variables to store credentials for a production setup.

4. **Run Migrations** *(optional)*  
   ```bash
   python migrate.py
   ```
   This step creates the database schema and tables if you want an automated approach.

5. **Seed Data** *(optional)*  
   - Run SQL scripts from `seeds/` or use a custom script to populate initial data (e.g., essential vocab, grammar lessons).

> **Note**: For advanced use-cases, incorporate a virtual environment (`venv`) or containerize the app with Docker.

---

## 5. Seed Scripts & Database Initialization

Under the `seeds/` directory, each SQL file handles table creation or data insertion. For instance:

- **`create_table_words.sql`**: Defines the schema for storing words (id, character, pinyin, meaning, etc.).  
- **`insert_grammar_lessons.sql`**: Inserts fundamental grammar lessons with short descriptions and example sentences.

You can run these scripts manually or incorporate them into a larger migration workflow (`migrate.py` or a dedicated tool like Alembic).

---

## 6. Core Modules & Functionalities

### 6.1 Vocabulary (`words.py`)
- **CRUD** operations for adding, updating, or deleting words.  
- Potential to **tag** words as verbs, adjectives, or other parts of speech.  
- Integration with spaced repetition logic (if desired).

### 6.2 Study Sessions (`study_sessions.py`)
- Allows tracking of the user’s daily or weekly learning sessions.  
- Stores personal notes, progress milestones, and next steps.

### 6.3 Interactive Activities (`study_activities.py`)
- **Character Writing**: Display stroke order instructions or practice canvas.  
- **Pinyin Practice**: Match phrases with correct pinyin annotations.  
- **Automatic Scoring** or user feedback prompts.

### 6.4 Word Grouping (`groups.py`)
- Assign words to thematic or user-defined groups (Food, HSK Level, etc.).  
- Provide quick ways to generate “smart lists” of relevant vocabulary.

### 6.5 Grammar Lessons (`grammar.py`)
- Storage and retrieval of grammar rules, example sentences, and explanations.  
- Potential for quiz integration to reinforce newly learned structures.

### 6.6 Listening Exercises (`listening.py`)
- Manages **audio clips**, comprehension questions, and answer validation.  
- Could interface with TTS (Text-To-Speech) services for dynamic audio generation.

### 6.7 Reading Passages (`reading.py`)
- Provides text passages with optional pinyin overlays.  
- Tracks reading progress and supplies comprehension checkpoints.

### 6.8 Writing Assignments (`writing.py`)
- Offers prompts for free-form writing tasks (e.g., short essays).  
- Facilitates submission tracking and feedback cycles (teacher or self-review).

---

## 7. Additional Scripts

- **`tasks.py`**  
  Automate periodic tasks (e.g., daily progress summaries, data backups).  
- **`dashboard.py`**  
  Potential UI or console-based module that aggregates user progress, time spent studying, or statistics on words learned.

---

## 8. Assets & Data

1. **assets/**  
   - Houses images, audio recordings, or PDF resources used in the listening or reading modules.
2. **data/**  
   - JSON files containing structured data sets:  
     - `study_activities.json` for interactive tasks  
     - `grammar_lessons.json` for grammar explanations  
     - `listening_exercises.json` for audio-based lessons  
     - … and more.

---

## 9. Contributing

Contributions are welcome! If you have improvements, bug fixes, or new features in mind:

1. **Fork** this repository and clone it locally.  
2. **Create a feature branch** (e.g., `git checkout -b feature/improve-grammar-module`).  
3. **Commit & Push** your changes with descriptive messages.  
4. **Open a Pull Request** describing what you changed, why, and how to test or review it.

---

## 10. Future Enhancements

- **Gamification Features**:  
  Achievements, badges, or streak systems to keep learners engaged.
- **Advanced Analytics**:  
  Track user performance trends, highlight strong/weak areas, and recommend next modules.
- **Integration with AI**:  
  Explore natural language processing for dynamic feedback on writing assignments or speech recognition for speaking practice.
- **Mobile App or PWA**:  
  Convert the interface into a Progressive Web App or develop a native app for on-the-go learning.
