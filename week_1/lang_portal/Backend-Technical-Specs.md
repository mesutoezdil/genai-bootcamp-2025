# Advanced Backend Server Technical Specification

## Business Objective
A language training institute aims to build a prototype learning portal focused on **basic-level Chinese vocabulary**. However, the architecture should be flexible enough to scale for more advanced levels in the future. This portal serves three core functions:
1. Acts as a repository for all potential vocabulary (with an emphasis on Chinese words and phrases), ready for extension into more complex language modules.
2. Maintains learning records (as an LRS) by storing correct/incorrect answers for each practice session.
3. Provides a centralized launch platform for a range of learning apps.

## High-Level Technical Requirements
- **Programming Language:** Go (golang)
- **Database:** SQLite3
- **Framework:** Gin (for HTTP routing)
- **Task Runner:** Mage
- **API Responses:** Strictly JSON
- **Security:** No user authentication or authorization in this prototype; treat the system as single-user.
- **Extensibility:** The codebase should be modular enough to allow easy addition of new language topics or expansions into advanced grammar exercises.

### Concurrency and Performance Considerations
- Go’s built-in concurrency model (goroutines & channels) can be leveraged for handling parallel requests when user volume increases.
- SQLite can be sufficient for early phases, but the system should maintain an abstraction layer (via the `models` package) to allow migrating to a more robust DB (PostgreSQL/MySQL) if usage grows.

### Containerization and Deployments (Optional)
- The project may be containerized using Docker for consistent development and deployment.
- Mage tasks can be expanded to include container build and push steps.

## Directory Structure

```text
backend_go/
├── cmd/
│   └── server/         # Main entry point to initialize and start the server
├── internal/
│   ├── models/         # Data structures and low-level database interactions
│   ├── handlers/       # HTTP route handlers (e.g., words, groups, stats)
│   └── service/        # Core business logic (e.g., study session management)
├── db/
│   ├── migrations/     # SQL files for schema versioning
│   └── seeds/          # Sample data for initialization
├── magefile.go         # Mage tasks definitions
├── go.mod              # Go module file
└── words.db            # SQLite database file (for development/testing)
```

This structure follows a typical Go project convention, separating commands (`cmd`), core logic (`internal`), and data/migration files (`db`).

## Database Schema
The project uses a single `words.db` SQLite database. Despite its simplicity, it can store a rich set of user progress data.

**Tables**:

- **words**
  - `id`: integer (primary key)
  - `chinese`: string (Chinese word or phrase)
  - `pinyin`: string (romanized spelling of the Chinese word)
  - `english`: string (English translation)
  - `parts`: json (extra metadata about the word, e.g. part of speech)

- **words_groups** (Many-to-Many association table)
  - `id`: integer (primary key)
  - `word_id`: integer (foreign key -> words.id)
  - `group_id`: integer (foreign key -> groups.id)

- **groups**
  - `id`: integer (primary key)
  - `name`: string (e.g. "Basic Greetings", "Numbers")

- **study_sessions**
  - `id`: integer (primary key)
  - `group_id`: integer (foreign key -> groups.id)
  - `created_at`: datetime
  - `study_activity_id`: integer (linking to a specific activity type)

- **study_activities**
  - `id`: integer (primary key)
  - `study_session_id`: integer (foreign key -> study_sessions.id)
  - `group_id`: integer (foreign key -> groups.id)
  - `created_at`: datetime

- **word_review_items**
  - `word_id`: integer (foreign key -> words.id)
  - `study_session_id`: integer (foreign key -> study_sessions.id)
  - `correct`: boolean (true if answered correctly, false otherwise)
  - `created_at`: datetime


## API Endpoints
All endpoints output JSON.

### Dashboard
1. **GET /api/dashboard/last_study_session**
   - Retrieves details of the most recent study session.
   - **Response**:
     ```json
     {
       "id": 123,
       "group_id": 456,
       "created_at": "2025-02-08T17:20:23-05:00",
       "study_activity_id": 789,
       "group_name": "Basic Greetings"
     }
     ```

2. **GET /api/dashboard/study_progress**
   - Returns study progress statistics (e.g., total words studied, total vocabulary available).
   - **Response**:
     ```json
     {
       "total_words_studied": 12,
       "total_available_words": 200
     }
     ```

3. **GET /api/dashboard/quick-stats**
   - Provides a quick overview (e.g., success rate, total study sessions, active groups).
   - **Response**:
     ```json
     {
       "success_rate": 80.0,
       "total_study_sessions": 4,
       "total_active_groups": 3,
       "study_streak_days": 4
     }
     ```

### Study Activities
1. **GET /api/study_activities/:id**
   - Retrieves activity-specific data (like a quiz name, description).
   - **Response**:
     ```json
     {
       "id": 1,
       "name": "Vocabulary Quiz",
       "thumbnail_url": "https://example.com/thumbnail.jpg",
       "description": "Practice your vocabulary with flashcards"
     }
     ```

2. **GET /api/study_activities/:id/study_sessions**
   - Lists all study sessions for a specific activity (100 items/page).
   - **Response**:
     ```json
     {
       "items": [
         {
           "id": 123,
           "activity_name": "Vocabulary Quiz",
           "group_name": "Basic Greetings",
           "start_time": "2025-02-08T17:20:23-05:00",
           "end_time": "2025-02-08T17:30:23-05:00",
           "review_items_count": 20
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 5,
         "total_items": 100,
         "items_per_page": 20
       }
     }
     ```

3. **POST /api/study_activities**
   - Creates a new study activity session. Typically requires parameters such as `group_id` and `study_activity_id`.
   - **Response**:
     ```json
     {
       "id": 124,
       "group_id": 123
     }
     ```

### Words
1. **GET /api/words**
   - Retrieves paginated list of words (defaults to 100 items per page).
   - **Response**:
     ```json
     {
       "items": [
         {
           "chinese": "你好",
           "pinyin": "nǐ hǎo",
           "english": "hello",
           "correct_count": 5,
           "wrong_count": 2
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 5,
         "total_items": 500,
         "items_per_page": 100
       }
     }
     ```

2. **GET /api/words/:id**
   - Shows a single word with usage statistics and group membership.
   - **Response**:
     ```json
     {
       "chinese": "你好",
       "pinyin": "nǐ hǎo",
       "english": "hello",
       "stats": {
         "correct_count": 5,
         "wrong_count": 2
       },
       "groups": [
         {
           "id": 1,
           "name": "Basic Greetings"
         }
       ]
     }
     ```

### Groups
1. **GET /api/groups**
   - Returns a list of groups (100 items/page).
   - **Response**:
     ```json
     {
       "items": [
         {
           "id": 1,
           "name": "Basic Greetings",
           "word_count": 20
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 1,
         "total_items": 10,
         "items_per_page": 100
       }
     }
     ```

2. **GET /api/groups/:id**
   - Shows group details, including total word count.
   - **Response**:
     ```json
     {
       "id": 1,
       "name": "Basic Greetings",
       "stats": {
         "total_word_count": 20
       }
     }
     ```

3. **GET /api/groups/:id/words**
   - Lists words within a specific group.
   - **Response**:
     ```json
     {
       "items": [
         {
           "chinese": "你好",
           "pinyin": "nǐ hǎo",
           "english": "hello",
           "correct_count": 5,
           "wrong_count": 2
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 1,
         "total_items": 20,
         "items_per_page": 100
       }
     }
     ```

4. **GET /api/groups/:id/study_sessions**
   - Retrieves study sessions associated with the given group.
   - **Response**:
     ```json
     {
       "items": [
         {
           "id": 123,
           "activity_name": "Vocabulary Quiz",
           "group_name": "Basic Greetings",
           "start_time": "2025-02-08T17:20:23-05:00",
           "end_time": "2025-02-08T17:30:23-05:00",
           "review_items_count": 20
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 1,
         "total_items": 5,
         "items_per_page": 100
       }
     }
     ```

### Study Sessions
1. **GET /api/study_sessions**
   - Lists all study sessions.
   - **Response**:
     ```json
     {
       "items": [
         {
           "id": 123,
           "activity_name": "Vocabulary Quiz",
           "group_name": "Basic Greetings",
           "start_time": "2025-02-08T17:20:23-05:00",
           "end_time": "2025-02-08T17:30:23-05:00",
           "review_items_count": 20
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 5,
         "total_items": 100,
         "items_per_page": 100
       }
     }
     ```

2. **GET /api/study_sessions/:id**
   - Shows information about a single study session.
   - **Response**:
     ```json
     {
       "id": 123,
       "activity_name": "Vocabulary Quiz",
       "group_name": "Basic Greetings",
       "start_time": "2025-02-08T17:20:23-05:00",
       "end_time": "2025-02-08T17:30:23-05:00",
       "review_items_count": 20
     }
     ```

3. **GET /api/study_sessions/:id/words**
   - Lists words reviewed in the specified study session.
   - **Response**:
     ```json
     {
       "items": [
         {
           "chinese": "你好",
           "pinyin": "nǐ hǎo",
           "english": "hello",
           "correct_count": 5,
           "wrong_count": 2
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 1,
         "total_items": 20,
         "items_per_page": 100
       }
     }
     ```

### System Reset Endpoints
1. **POST /api/reset_history**
   - Resets study history (e.g., clears `word_review_items`).
   - **Response**:
     ```json
     {
       "success": true,
       "message": "Study history has been reset"
     }
     ```

2. **POST /api/full_reset**
   - Completely resets the entire system (e.g., words, groups, sessions) to a default state.
   - **Response**:
     ```json
     {
       "success": true,
       "message": "System has been fully reset"
     }
     ```

3. **POST /api/study_sessions/:id/words/:word_id/review**
   - Records correctness of a user’s response for a specific word in a study session.
   - **Request Payload**:
     ```json
     {
       "correct": true
     }
     ```
   - **Response**:
     ```json
     {
       "success": true,
       "word_id": 1,
       "study_session_id": 123,
       "correct": true,
       "created_at": "2025-02-08T17:33:07-05:00"
     }
     ```


## Task Runner Tasks (Mage)

### `init_db`
Initializes the SQLite database (`words.db`). If the file doesn’t exist, create it.

### `migrate_db`
Runs migration scripts from the `migrations` folder in ascending order (e.g., `0001_init.sql`, `0002_create_words_table.sql`). Creates or updates the database schema.

### `seed_data`
Imports JSON seed data from the `seeds` folder. Example data structure:
```json
[
  {
    "chinese": "学习",
    "pinyin": "xuéxí",
    "english": "study"
  }
]
```

This data is then inserted into the `words` table (and optionally assigned to relevant groups).

## Future Enhancements
1. **Vocabulary Richness**: Expand words table to include advanced grammar rules, example sentences, or audio pronunciations.
2. **User Management**: Introduce authentication/authorization if multiple user profiles are desired.
3. **Analytics & Reporting**: Add endpoints for generating performance overviews across multiple sessions or larger time spans.
4. **Microservice Approach**: As usage scales, consider splitting the LRS (Learning Record Store) into a separate service.
5. **Internationalization**: Expand or rename fields to accommodate multiple languages beyond Chinese.