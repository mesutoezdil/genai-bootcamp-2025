# Chinese Learning App - Frontend Technical Spec

## Pages

### Dashboard `/dashboard`

**Purpose:**  
This page provides an overview of the user's learning progress and serves as the default landing page.

**Components:**
- **Recent Study Session**  
  - Displays details of the last study session (activity type, completion time, accuracy stats, etc.)
  - Quick link to resume learning from where the user left off
- **Progress Overview**  
  - Tracks total characters and words learned (e.g., 30/1000)
  - Displays HSK (Chinese Proficiency Test) level progression
- **Performance Stats**  
  - Learning accuracy (e.g., 85%)
  - Total study sessions completed
  - Active study groups
  - Daily learning streak indicator
- **Start Learning Button**  
  - Redirects to the study activities page

**Required API Endpoints:**
- GET /api/dashboard/last_study_session
- GET /api/dashboard/progress_overview
- GET /api/dashboard/performance_stats

---

### Study Activities Index `/study_activities`

**Purpose:**  
This page showcases available learning activities (e.g., flashcards, writing exercises, listening comprehension).

**Components:**
- **Study Activity Card**  
  - Displays a thumbnail for each activity
  - Shows the name and brief description
  - Buttons for "Start Activity" and "View Details"

**Required API Endpoints:**
- GET /api/study_activities

---

### Study Activity Details `/study_activities/:id`

**Purpose:**  
Shows an in-depth view of a study activity and past performance records.

**Components:**
- Name and description of the activity
- Thumbnail or preview
- "Start Activity" button
- **Past Sessions List (Paginated)**  
  - Activity name, session date, duration, accuracy, number of review items

**Required API Endpoints:**
- GET /api/study_activities/:id
- GET /api/study_activities/:id/study_sessions

---

### Study Activity Launch `/study_activities/:id/launch`

**Purpose:**  
Initiates a study session.

**Components:**
- Name of activity
- Select learning group
- "Start Session" button

**Behavior:**  
- Opens the study session in a new tab  
- Redirects to the session summary page upon completion

**Required API Endpoints:**
- POST /api/study_activities

---

### Words Index `/words`

**Purpose:**  
Displays a comprehensive list of Chinese characters and vocabulary available for learning.

**Components:**
- **Paginated Vocabulary List**  
  - Columns: **Simplified Chinese**, **Pinyin**, **English Meaning**, **Correct Attempts**, **Incorrect Attempts**
  - Clicking a word navigates to the word details page

**Required API Endpoints:**
- GET /api/words

---

### Word Details `/words/:id`

**Purpose:**  
Displays detailed information about a specific Chinese word or character.

**Components:**
- Simplified Chinese character(s)
- Pinyin pronunciation
- English meaning
- Usage examples
- Stroke order animation
- **Performance Stats**  
  - Correct vs incorrect attempts
  - Study history

**Required API Endpoints:**
- GET /api/words/:id

---

### Study Groups `/groups`

**Purpose:**  
Shows a list of study groups, such as "HSK 1 Vocabulary" or "Common Business Terms."

**Components:**
- **Paginated Group List**  
  - Group name
  - Number of words in each group

**Required API Endpoints:**
- GET /api/groups
