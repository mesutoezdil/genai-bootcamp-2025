# Advanced Frontend Technical Specification (Chinese Learning Portal)

Below is a **detailed** frontend technical specification that integrates seamlessly with the advanced backend specification you already have. It places extra emphasis on supporting **Chinese language learning**, while also maintaining a robust, extensible architecture.

---

## High-Level Overview

### Key Goals:
1. **Consistency With Backend**: Adhere to the existing REST API design, ensuring each endpoint is correctly consumed.
2. **Chinese Language Focus**: Provide specialized UI support for Chinese text, including pinyin, possible tone markers, and expansions for advanced learning features.
3. **Scalability & Maintainability**: Organize components so that it’s easy to add new pages or adapt to more complex features (e.g., grammar lessons, audio playback, or advanced analytics).

### Recommended Technologies:
- **React** for the UI framework (preferably TypeScript for type safety).
- **React Router** for client-side routing.
- **Tailwind CSS** for rapid, consistent styling.
- **Axios or Fetch API** for data calls.
- **State Management** (e.g., React Context or Redux) for any cross-cutting data.
- **Bundler** (e.g., Vite or CRA) for local development and production builds.

> While these suggestions are typical, the actual tech stack can vary as long as it respects the REST endpoints and data structures defined in your backend.

---

## Suggested Directory Structure

```text
frontend_react/
├── public/
│   └── index.html
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Dashboard/
│   │   ├── Activities/
│   │   ├── Words/
│   │   ├── Groups/
│   │   └── Shared/       # Shared, generic components (e.g. pagination, layout)
│   ├── pages/            # Page-level components
│   │   ├── DashboardPage.tsx
│   │   ├── ActivitiesPage.tsx
│   │   ├── StudyActivityShowPage.tsx
│   │   ├── StudyActivityLaunchPage.tsx
│   │   ├── WordsPage.tsx
│   │   ├── WordShowPage.tsx
│   │   ├── GroupsPage.tsx
│   │   ├── GroupShowPage.tsx
│   │   ├── StudySessionsPage.tsx
│   │   ├── StudySessionShowPage.tsx
│   │   └── SettingsPage.tsx
│   ├── routes/           # Central route definitions
│   ├── services/         # API service layer (requests to backend)
│   │   ├── dashboard.service.ts
│   │   ├── activities.service.ts
│   │   ├── words.service.ts
│   │   ├── groups.service.ts
│   │   ├── studySessions.service.ts
│   │   └── ...
│   ├── utils/            # Utility functions (e.g., string formatting, date parsing)
│   ├── App.tsx           # Root application component
│   └── index.tsx         # Main entry point
├── package.json
└── tsconfig.json
```

- **components/**: Houses smaller building blocks that are reused across pages.
- **pages/**: Contains one file per route-level page.
- **services/**: Encapsulates all data fetching, ensuring a clean separation between UI and data access.

---

## Page-by-Page Specifications

### 1. Dashboard Page (`/dashboard`)

**Purpose**: Displays a broad summary of the user’s progress in learning Chinese.

**UI Features**:
- **Last Study Session Panel**
  - Shows last activity used and timestamp.
  - Summarizes correct vs. incorrect answers from that activity.
  - Provides a link to the associated group (e.g., "Basic Greetings").
  - Visual indicators (e.g., a small bar or pie chart) to highlight user performance in that session.
- **Study Progress**
  - Displays total words studied (e.g., `studyProgress.total_words_studied`) vs. total available words (`studyProgress.total_available_words`).
  - Progress bar indicating overall mastery percentage (like `(studied / total) * 100`).
- **Quick Stats**
  - **Success Rate** (percentage of correct vs. total attempts across all sessions).
  - **Total Study Sessions**.
  - **Total Active Groups**.
  - **Study Streak** in days (consecutive days studied).
- **Start Studying Button**
  - Redirects to `/study_activities`.

**API Endpoints**:
- `GET /api/dashboard/last_study_session`
- `GET /api/dashboard/study_progress`
- `GET /api/dashboard/quick_stats`

**Implementation Notes**:
- Consider using React’s `useEffect` to fetch all three endpoints in parallel upon mount.
- Use cards or small info boxes for readability.
- Offer a simple chart or colored text to visually convey stats.

---

### 2. Study Activities Index (`/study_activities`)

**Purpose**: Lists all study activities (e.g., "Vocabulary Quiz", "Flashcards").

**UI Features**:
- **Study Activity Card** (grid or list view):
  - Displays `thumbnail_url`, `name`, short `description`.
  - "Launch" button to go to a launch page: `/study_activities/:id/launch`.
  - "View More" button to see details: `/study_activities/:id`.

**API Endpoints**:
- Typically, you’ll need `GET /api/study_activities` to fetch an array of available activities. (The advanced backend references `GET /api/study_activities/:id` but you can create one for listing all as well.)

**Implementation Notes**:
- Provide pagination if the list grows too large.
- Alternatively, you could incorporate searching or filtering by activity name.

---

### 3. Study Activity Show (`/study_activities/:id`)

**Purpose**: Provides more in-depth information about a specific activity, including its past sessions.

**UI Features**:
- **Activity Details**
  - Name, thumbnail image, and `description`.
- **Launch Button**
  - Takes the user to `/study_activities/:id/launch`.
- **Past Study Sessions** (paginated)
  - For each session:
    - ID, group name, start/end time, # of review items.
    - Possibly clickable to see the session detail page.

**API Endpoints**:
- `GET /api/study_activities/:id` for the activity’s metadata.
- `GET /api/study_activities/:id/study_sessions` for associated sessions.

**Implementation Notes**:
- Display a brief summary chart of how many times each group was studied in this activity.
- If sessions are numerous, implement pagination.

---

### 4. Study Activity Launch (`/study_activities/:id/launch`)

**Purpose**: Allows the user to initiate a new study session under a chosen group.

**UI Features**:
- **Activity Information**: Reiterate the name, thumbnail, short description.
- **Form**:
  - Group dropdown (lists all groups or only relevant groups for that activity, if limited).
  - **Launch Now** button.
- **Behavior**:
  - On click, the frontend calls `POST /api/study_activities`, sending `group_id` and `study_activity_id`.
  - The backend responds with the new `study_session` ID.
  - The frontend may open a new tab with the actual activity content.
  - The original tab redirects to `/study_sessions/:newSessionId` (the newly created session’s detail page).

**Implementation Notes**:
- Use a controlled form to capture group selection.
- Consider a loading state or disabled button while the request is processed.
- If your actual study UI is separate, coordinate how the new session ID is passed.

---

### 5. Words Index (`/words`)

**Purpose**: Displays all words in the database, focusing on Chinese vocabulary.

**UI Features**:
- **Filter/Search Bar**: Optionally allow the user to filter by Chinese or English keywords.
- **Paginated Table** (up to 100 words/page):
  - Columns: `Chinese`, `Pinyin`, `English`, `Correct Count`, `Wrong Count`.
  - Each Chinese word is clickable, leading to `/words/:id`.
- **Possible Tone Color-Coding**:
  - (Optional) highlight pinyin tones in color for easy identification (requires additional logic in the UI).

**API Endpoints**:
- `GET /api/words` (the backend returns items and pagination info).

**Implementation Notes**:
- For large sets, ensure you store pagination metadata (`current_page`, `total_pages`, etc.).
- Provide next/previous page navigation, or numeric page controls.

---

### 6. Word Show (`/words/:id`)

**Purpose**: Displays detailed info for a single Chinese word.

**UI Features**:
- **Primary Info**:
  - **Chinese** (large font), **pinyin** (with tone marks if available), **English**.
- **Study Statistics**:
  - Correct count vs. wrong count (could be a small donut chart or just numeric text).
- **Groups**:
  - Render a row of “tag” components for each group.
  - Each tag is clickable and navigates to the group’s show page.

**API Endpoints**:
- `GET /api/words/:id`

**Implementation Notes**:
- Incorporate potential expansions like example sentences, audio playback icons, etc.
- Visual flags for user’s performance (e.g., if wrong_count is high, highlight it in red, etc.).

---

### 7. Groups Index (`/groups`)

**Purpose**: Displays all groups in the database.

**UI Features**:
- **Paginated Table**:
  - Columns: `Group Name`, `Word Count`.
  - Clicking on the group name navigates to `/groups/:id`.

**API Endpoints**:
- `GET /api/groups`

**Implementation Notes**:
- If the list grows large, add searching or pagination controls.
- Show group usage or activity stats in a future enhancement.

---

### 8. Group Show (`/groups/:id`)

**Purpose**: Shows comprehensive details about a specific group.

**UI Features**:
- **Group Name** in a large heading.
- **Group Statistics**:
  - e.g., `total_word_count`.
- **Words in This Group** (reuse the Words Index table structure but filtered to this group).  
- **Study Sessions** (reuse the Study Sessions structure but filtered to this group).  

**API Endpoints**:
- `GET /api/groups/:id` (basic info and stats).
- `GET /api/groups/:id/words` (paginated list of words in this group).
- `GET /api/groups/:id/study_sessions` (paginated list of relevant sessions).

**Implementation Notes**:
- Offer tabs to switch between "Words" and "Study Sessions" within the group.
- Provide pagination or infinite scroll if the group has many words.

---

### 9. Study Sessions Index (`/study_sessions`)

**Purpose**: Shows a global list of all study sessions.

**UI Features**:
- **Paginated Table**:
  - Columns: `ID`, `Activity Name`, `Group Name`, `Start Time`, `End Time`, `Review Items Count`.
  - Clicking on the session ID navigates to `/study_sessions/:id`.

**API Endpoints**:
- `GET /api/study_sessions`

**Implementation Notes**:
- Potential for search or filters by activity or group in the future.
- Time formatting can be done with a library like `date-fns`.

---

### 10. Study Session Show (`/study_sessions/:id`)

**Purpose**: Provides details on a single study session.

**UI Features**:
- **Session Info**:
  - Activity name, group name, start time, end time, total review items.
- **Words Reviewed** (paginated list)
  - Reuse the word table structure (Chinese, pinyin, English, correct/wrong counts), but with data filtered to the session.

**API Endpoints**:
- `GET /api/study_sessions/:id`
- `GET /api/study_sessions/:id/words`

**Implementation Notes**:
- If the session is still in progress, consider real-time updates or a refresh button.

---

### 11. Settings Page (`/settings`)

**Purpose**: Allows the user (or admin) to configure global portal settings.

**UI Features**:
- **Theme Selector**: Switch between Light, Dark, or System modes.
- **Reset History** Button
  - Issues a `POST /api/reset_history` to clear all study history.
- **Full Reset** Button
  - Calls `POST /api/full_reset` to remove all data and re-seed.
- **Confirmations**: Provide a warning modal or confirmation dialog before destructive actions.

**Implementation Notes**:
- Possibly restrict or hide these destructive actions behind an “Are you sure?” prompt.

---

## Detailed Data Flows & Additional Considerations

1. **Chinese-Specific UX**:
   - Tone Visualization: If feasible, highlight pinyin tones in color (e.g., 1st tone=blue, 2nd tone=green, etc.) to help learners.
   - Character Stroke Animations: Future enhancements might include stroke-order animations.
   - Audio Playback: Another enhancement could be a speaker icon next to words for TTS playback.
2. **Pagination Handling**:
   - Each listing endpoint (`/words`, `/study_sessions`, etc.) includes pagination info. The frontend must store and display `current_page`, `total_pages`, etc.
   - Provide next/previous navigation.
3. **Error & Loading States**:
   - Show a loading spinner or skeleton UI while data is being fetched.
   - If an error occurs (like a network or server error), display a relevant message.
4. **Localization / i18n** (Future):
   - The app might expand to support multiple languages in the UI. Currently, English is fine.
5. **Performance**:
   - For extremely large data sets (thousands of words), consider lazy loading or server-driven pagination.
   - If concurrency is required, ensure your backend can handle parallel requests.

---

## Conclusion

By following the above guidelines, your **Chinese Learning Portal**’s frontend will be fully aligned with the advanced backend:

1. **Detailed Pages** that match each backend endpoint.
2. **Chinese-Focused Features** like pinyin, correct/wrong stats, and possible expansions for advanced learning.
3. **Scalable Architecture** that accommodates new features with minimal refactoring.
4. **Extensible UI** design that can adopt more advanced interactions (e.g., stroke animations, audio playback).
