# Chinese Learning App – Frontend Technical Specification

This document outlines the **core pages** and **features** of the Chinese Learning App’s frontend. The app aims to help users systematically build and maintain their Chinese vocabulary, track study progress, and engage in interactive learning activities. Each page description includes the **purpose**, **key components**, **UI behaviors**, and **required API endpoints**.

---

## Table of Contents

1. [Introduction](#1-introduction)  
2. [Dashboard (`/dashboard`)](#2-dashboard-dashboard)  
3. [Study Activities Index (`/study_activities`)](#3-study-activities-index-study_activities)  
4. [Study Activity Details (`/study_activities/:id`)](#4-study-activity-details-study_activitiesid)  
5. [Study Activity Launch (`/study_activities/:id/launch`)](#5-study-activity-launch-study_activitiesidlaunch)  
6. [Words Index (`/words`)](#6-words-index-words)  
7. [Word Details (`/words/:id`)](#7-word-details-wordsid)  
8. [Study Groups (`/groups`)](#8-study-groups-groups)

---

## 1. Introduction

The **Chinese Learning App** frontend is built to provide a **seamless user experience**, offering:

- **Progress Tracking**: Summaries of study sessions, word mastery, and performance statistics.
- **Vocabulary Management**: Rich detail on Chinese words/phrases, including usage examples and stroke order.
- **Interactive Activities**: Varied exercises (flashcards, writing, listening) that cater to different learning preferences.
- **Grouping & Thematic Learning**: Organizing vocabulary by themes (HSK levels, daily topics, or custom sets).

Each page’s **UI** aims to be intuitive and informative, while the **API integration** ensures up-to-date data. The pages below detail the primary user journeys and associated endpoints.

---

## 2. Dashboard (`/dashboard`)

### Purpose
The **Dashboard** provides a high-level overview of the user’s learning progress and serves as the home or landing page.

### Components

1. **Recent Study Session**  
   - Shows summary details of the user’s latest session:  
     - Activity type (e.g., Flashcards, Writing Practice)  
     - Completion time, accuracy stats (e.g., 15 correct out of 20)  
     - Quick link/button to **Resume** or **View Details**

2. **Progress Overview**  
   - Displays milestones such as total characters or words learned (`30 / 1000`)  
   - Highlights the user’s HSK level progression or equivalent skill tier

3. **Performance Stats**  
   - Overall accuracy (e.g., 85%)  
   - Count of completed study sessions  
   - Active study groups or modules  
   - **Daily Streak** indicator (e.g., how many consecutive days studied)

4. **Start Learning Button**  
   - Takes the user to the **Study Activities** page or a relevant next-step flow

### Required API Endpoints

- **GET** `/api/dashboard/last_study_session`  
  Returns info about the user’s most recent study session.
- **GET** `/api/dashboard/progress_overview`  
  Provides data on overall progress, total words learned, etc.
- **GET** `/api/dashboard/performance_stats`  
  Offers summary performance metrics (accuracy, sessions completed, daily streak).

---

## 3. Study Activities Index (`/study_activities`)

### Purpose
Displays all available **learning activities**, offering different ways to practice (flashcards, writing, listening, etc.).

### Components

1. **Study Activity Card**  
   - For each activity:
     - A small **thumbnail** image or icon representing the exercise type
     - Title (e.g., “Flashcards”) and brief description
     - Action buttons for **Start Activity** or **View Details**

### Required API Endpoints

- **GET** `/api/study_activities`  
  Lists all the available activity types, possibly with short descriptions or usage counts.

---

## 4. Study Activity Details (`/study_activities/:id`)

### Purpose
Provides an **in-depth view** of a specific learning activity, plus historical performance data.

### Components

1. **Activity Overview**  
   - Displays the activity’s name and a more detailed description or set of instructions.
   - A **thumbnail** or preview graphic indicating its nature (e.g., writing, listening).

2. **Start Activity Button**  
   - Initiates a new session.

3. **Past Sessions List** (Paginated)  
   - Each item includes:
     - **Session date** and duration
     - **Accuracy** or score
     - Number of **review items** encountered or completed

### Required API Endpoints

- **GET** `/api/study_activities/:id`  
  Fetches the activity’s core information.
- **GET** `/api/study_activities/:id/study_sessions`  
  Returns a list of past sessions related to this activity, including stats.

---

## 5. Study Activity Launch (`/study_activities/:id/launch`)

### Purpose
A page to **configure and start** a new study session under a specific activity.

### Components

1. **Activity Name**  
   - Reinforces which activity the user is about to begin.

2. **Select Learning Group**  
   - A dropdown or selection list of available groups (HSK 1, Travel vocab, etc.) the user can practice.

3. **Start Session Button**  
   - On click, triggers an API call to create a new study session.

### Behavior

- Once the session is created, it may **open in a new tab** (especially if the activity is a full-screen interactive module).  
- Upon completion, the user is typically **redirected** to a session summary or results page.

### Required API Endpoints

- **POST** `/api/study_activities`  
  Initiates a study session (with references to chosen group/activity type). Returns a session ID or relevant metadata.

---

## 6. Words Index (`/words`)

### Purpose
Shows a **comprehensive vocabulary list** for the user to browse, search, and filter.

### Components

1. **Paginated Vocabulary Table**  
   - Columns:  
     - **Simplified Chinese**  
     - **Pinyin**  
     - **English Meaning**  
     - **Correct Attempts / Incorrect Attempts**  
   - A row click or dedicated button leads to the **Word Details** page.

2. (Optional) **Search/Filter**  
   - A search bar for looking up specific characters or English meanings.  
   - Filters by group or part-of-speech (if supported by the API).

### Required API Endpoints

- **GET** `/api/words`  
  Fetches the word list, possibly with query parameters like `page`, `limit`, or `search`.

---

## 7. Word Details (`/words/:id`)

### Purpose
Displays **detailed information** about a particular Chinese word or phrase, assisting users in deeper exploration.

### Components

1. **Word Header**  
   - **Simplified Chinese** text  
   - **Pinyin** and **English** meaning

2. **Usage Examples**  
   - One or more example sentences.  
   - Possibly show pinyin + English translation side-by-side.

3. **Stroke Order Animation**  
   - (Optional) Interactive or GIF-based demonstration of character stroke order.

4. **Performance Stats**  
   - Shows how many times the user has encountered this word in study sessions.  
   - **Correct vs. incorrect** attempt counts.  
   - Links to further review items or activity logs.

### Required API Endpoints

- **GET** `/api/words/:id`  
  Returns complete data for the specified word, including usage examples and any performance stats from the user’s study history.

---

## 8. Study Groups (`/groups`)

### Purpose
Allows the user to browse **study groups**, such as HSK levels, thematic sets (food, travel), or custom categories.

### Components

1. **Group List** (Paginated)  
   - Displays each group’s **name** and (optionally) a **description**.  
   - Shows **word count** or coverage stats within that group.

2. (Optional) **View Group** button  
   - Could lead to a group detail page if required (e.g., listing only the words in that group).

### Required API Endpoints

- **GET** `/api/groups`  
  Returns a list of all available groups (with possible pagination or sorting).

---

## Final Notes

This **Frontend Technical Spec** provides a structured foundation for building a user-friendly, goal-oriented learning interface. By mapping each page to **clear API endpoints**, developers can streamline both UI components and data flows, ensuring consistency and clarity across the application.

- **Responsive Design**: Consider a **mobile-first** approach, especially for pages like **Words Index** or **Study Activities**, which may require custom layouts for smaller screens.
- **Accessibility**: Implement best practices (keyboard navigation, ARIA labels, etc.) to make the app accessible to a broader user base.
- **Testing**: Embrace **end-to-end** tests (e.g., Cypress) for crucial flows like session creation or word review logging.
