# Chinese Learning App – Backend Technical Specifications

This backend service powers a **Chinese Learning App** by providing a vocabulary repository, a progress tracking system, and launch points for interactive learning activities. It is designed as a **prototype** with straightforward user flows, minimal authentication needs, and maintainable code for easy iteration and scaling.

---

## Table of Contents

1. [Overview & Business Goals](#1-overview--business-goals)  
2. [Technical Stack](#2-technical-stack)  
3. [Database Schema](#3-database-schema)  
   1. [Schema Explanation](#31-schema-explanation)  
4. [API Endpoints](#4-api-endpoints)  
   1. [Dashboard](#41-dashboard)  
   2. [Study Activities & Sessions](#42-study-activities--sessions)  
   3. [Vocabulary & Groups](#43-vocabulary--groups)  
   4. [Resetting & Maintenance](#44-resetting--maintenance)  
5. [Task Runner (Mage)](#5-task-runner-mage)  
   1. [Initialize Database](#51-initialize-database)  
   2. [Migrate Database](#52-migrate-database)  
   3. [Seed Data](#53-seed-data)  
6. [Authentication](#6-authentication)  
7. [Deployment & Configuration](#7-deployment--configuration)  
8. [Future Enhancements](#8-future-enhancements)

---

## 1. Overview & Business Goals

### 1.1 Purpose

- **Vocabulary Repository**: Stores essential Mandarin words, pinyin, English translations, and additional metadata (e.g., parts-of-speech).  
- **Learning Record Store (LRS)**: Tracks user interactions and accuracy in recalling vocabulary, forming a database of progress metrics.  
- **Launchpad for Activities**: Initiates various interactive exercises (character writing, multiple-choice quizzes, etc.) based on the study session context.

### 1.2 Key Objectives

1. **Ease of Use**  
   - Minimal overhead for adding or updating words, groups, and study sessions.  
2. **Centralized Tracking**  
   - Single user’s progress, correctness, and session history aggregated in one database.  
3. **Extensibility**  
   - Prepared for potential multi-user support and advanced analytics in later phases.

---

## 2. Technical Stack

- **Language**: [Go](https://golang.org/)  
  - Known for its performance, concurrency capabilities, and ease of deployment.
- **Framework**: [Gin](https://gin-gonic.com/)  
  - Lightweight and fast for REST API development.
- **Database**: [SQLite3](https://sqlite.org/)  
  - Chosen for simplicity and minimal setup. Suitable for single-user or small-scale usage.  
- **Task Runner**: [Mage](https://magefile.org/)  
  - Facilitates running commands like database initialization, migrations, and data seeding.  
- **Authentication**: None *(single-user prototype)*  
  - Could be extended later to integrate OAuth, JWT, or other secure methods.
- **Response Format**: JSON  
  - Standard for modern REST APIs, easily parsed by web or mobile clients.

---

## 3. Database Schema

By default, the app interacts with a file-based **`words.db`** (SQLite) database. Below are the primary tables:

- **`words`**  
  - **id** *(integer)*  
  - **simplified** *(string)*  
  - **pinyin** *(string)*  
  - **english** *(string)*  
  - **parts** *(json)*  
- **`word_groups`**  
  - **id** *(integer)*  
  - **word_id** *(integer)*  
  - **group_id** *(integer)*  
- **`groups`**  
  - **id** *(integer)*  
  - **name** *(string)*  
- **`study_sessions`**  
  - **id** *(integer)*  
  - **group_id** *(integer)*  
  - **created_at** *(datetime)*  
  - **study_activity_id** *(integer)*  
- **`study_activities`**  
  - **id** *(integer)*  
  - **study_session_id** *(integer)*  
  - **group_id** *(integer)*  
  - **created_at** *(datetime)*  
- **`word_review_items`**  
  - **word_id** *(integer)*  
  - **study_session_id** *(integer)*  
  - **correct** *(boolean)*  
  - **created_at** *(datetime)*

### 3.1 Schema Explanation

- **`words`**:  
  Central store of vocabulary words. The `parts` column (JSON) can contain additional data like part-of-speech tags (noun, verb, adjective), usage frequencies, or synonyms.
- **`word_groups`** & **`groups`**:  
  Implements a *many-to-many* relationship, grouping words by theme (e.g., “Travel,” “Food,” etc.). Users or content managers can create custom groups.
- **`study_sessions`**:  
  An abstract record representing a user’s learning session. Ties to a *group* of words or a specific activity type.
- **`study_activities`**:  
  Tracks the finer details of an activity within a session, such as start time or references to the group content. Could later expand to store quiz results or advanced metrics.
- **`word_review_items`**:  
  Logs correctness for each attempted word during a study session. Useful for spaced repetition or performance analysis.

---

## 4. API Endpoints

The REST API, powered by **Gin**, uses standard JSON responses. Clients should expect to see `{"error": "some message"}` for error scenarios.

### 4.1 Dashboard

1. **GET** `/api/dashboard/progress_overview`  
   - **Description**: Summarizes user’s study progress (e.g., total sessions, words learned).  
   - **Response**: JSON object with aggregated stats, like:
     ```json
     {
       "totalSessions": 10,
       "wordsMastered": 34,
       "lastSessionDate": "2025-03-25T10:23:42Z"
     }
     ```

2. **GET** `/api/dashboard/performance_stats`  
   - **Description**: Quick performance metrics (accuracy rates, average session duration, etc.).  
   - **Response**: 
     ```json
     {
       "averageAccuracy": 86,
       "recentSessions": [
         { "sessionId": 7, "correct": 12, "incorrect": 3 },
         ...
       ]
     }
     ```

### 4.2 Study Activities & Sessions

1. **GET** `/api/study_activities/:id`  
   - **Description**: Retrieves details for a specific learning activity.  
   - **Response**: Activity metadata, including group references and timestamps.

2. **POST** `/api/study_activities`  
   - **Description**: Creates a new study activity or session.  
   - **Request Body** (example):
     ```json
     {
       "groupId": 2,
       "activityType": "quiz"
     }
     ```
   - **Response**: 
     ```json
     {
       "studyActivityId": 14,
       "createdAt": "2025-03-25T09:10:00Z"
     }
     ```

3. **POST** `/api/study_sessions/:id/words/:word_id/review`  
   - **Description**: Logs whether the user correctly recalled a word during a session.  
   - **Request Body**:
     ```json
     {
       "correct": true
     }
     ```
   - **Response**: Indicates success or error.

### 4.3 Vocabulary & Groups

1. **GET** `/api/words`  
   - **Description**: Returns a paginated list of all words.  
   - **Query Params**: `page`, `limit`, or filters like `groupId`.  
   - **Response**: Array of word objects.

2. **GET** `/api/words/:id`  
   - **Description**: Fetches a single word’s details by ID.  
   - **Response**: 
     ```json
     {
       "id": 45,
       "simplified": "吃",
       "pinyin": "chī",
       "english": "to eat",
       "parts": {
         "partOfSpeech": "verb",
         "examples": ["我喜欢吃苹果。"]
       }
     }
     ```

3. **GET** `/api/groups`  
   - **Description**: Lists all vocabulary groups.  
   - **Response**: Array of group objects, e.g.:
     ```json
     [
       { "id": 1, "name": "Travel" },
       { "id": 2, "name": "Food" }
     ]
     ```

4. **GET** `/api/groups/:id`  
   - **Description**: Retrieves group details, including associated words.  
   - **Response**: 
     ```json
     {
       "id": 2,
       "name": "Food",
       "words": [...]
     }
     ```

### 4.4 Resetting & Maintenance

1. **POST** `/api/reset_history`  
   - **Description**: Clears user’s study data (e.g., word_review_items, study_sessions), but preserves word definitions.  
   - **Response**: `{"status": "ok"}` if successful.

2. **POST** `/api/full_reset`  
   - **Description**: **Wipes the entire database** (including words, groups) and reinitializes schema.  
   - **Response**: `{"status": "ok"}` if the reset is successful.
   - **Warning**: Use with caution, as this is destructive!

---

## 5. Task Runner (Mage)

[**Mage**](https://magefile.org/) is used to script routine tasks like initializing the database or seeding data. Standard tasks might include:

### 5.1 Initialize Database

**Command**: `mage initdb`

- Creates the `words.db` file if it doesn’t exist.
- Might run `CREATE TABLE` statements for all schemas.

### 5.2 Migrate Database

**Command**: `mage migrate`

- Executes SQL migration files in a predefined order.
- Useful for schema changes or versioning the DB structure.

### 5.3 Seed Data

**Command**: `mage seed`

- Loads JSON files containing sample vocabulary or groups.
- Links them to the appropriate database tables.

---

## 6. Authentication

Currently **none**. As a single-user prototype, session-based or token-based auth isn’t implemented. However, for future multi-user expansion, consider:

- **JWT** or **OAuth** for robust, stateless authentication.  
- **Basic** or **Session Cookies** if the environment is simplistic.  
- A user table to differentiate participants and store personal study data.

---

## 7. Deployment & Configuration

- **Local Deployment**  
  - By default, the service runs on port 8080 (or an environment variable `PORT`).  
  - `SQLite` file is stored as `words.db` in the root directory.
- **Production**  
  - Optionally use Docker for packaging.  
  - For concurrency, you may want to integrate with a more robust database (like PostgreSQL).  
  - Consider environment variables or config files for specifying DB path, port, or environment mode (`dev`, `prod`).
