# Chinese Learning App - Backend Technical Specs

## Business Goal
The app will act as:
1. A vocabulary repository for learning Mandarin Chinese
2. A **Learning Record Store (LRS)** to track user progress and accuracy
3. A launchpad for different types of interactive study activities

## Technical Stack
- **Backend Language:** Go
- **Database:** SQLite3
- **Framework:** Gin (for REST API)
- **Task Runner:** Mage
- **Authentication:** None (single-user prototype)
- **Response Format:** JSON

## Database Schema
- **words** (Stores vocabulary)
  - id (integer)
  - simplified (string)
  - pinyin (string)
  - english (string)
  - parts (json)
- **word_groups** (Links words to thematic groups, many-to-many relationship)
  - id (integer)
  - word_id (integer)
  - group_id (integer)
- **groups** (Vocabulary categories)
  - id (integer)
  - name (string)
- **study_sessions** (Tracks study attempts)
  - id (integer)
  - group_id (integer)
  - created_at (datetime)
  - study_activity_id (integer)
- **study_activities** (Records specific activities)
  - id (integer)
  - study_session_id (integer)
  - group_id (integer)
  - created_at (datetime)
- **word_review_items** (Logs correctness of word recall)
  - word_id (integer)
  - study_session_id (integer)
  - correct (boolean)
  - created_at (datetime)

## API Endpoints

### GET /api/dashboard/progress_overview
Returns progress statistics.

### GET /api/dashboard/performance_stats
Returns quick performance metrics.

### GET /api/study_activities/:id
Returns details of a learning activity.

### GET /api/words
Returns a paginated list of vocabulary words.

### GET /api/words/:id
Returns details of a specific word.

### GET /api/groups
Returns all vocabulary groups.

### GET /api/groups/:id
Returns group details, including word list and statistics.

### POST /api/study_activities
Creates a new study session.

### POST /api/study_sessions/:id/words/:word_id/review
Logs whether a user correctly or incorrectly recalled a word.

### POST /api/reset_history
Resets all study data.

### POST /api/full_reset
Wipes and reinitializes the database.

## Task Runner
### Initialize Database
Sets up `words.db`.

### Migrate Database
Runs SQL migration files.

### Seed Data
Loads JSON vocabulary files, mapping words to study groups.
