# Chinese Learning App – Technical Specifications

This document describes a robust and scalable **Chinese learning application** designed to generate beginner-friendly sentences in **Mandarin**, allow learners to practice their handwriting or typing skills, and provide real-time feedback. By leveraging AI components—such as a language model for sentence generation and an OCR/LLM-based grading system—the application aims to improve user engagement and learning outcomes.

---

## Table of Contents

1. [Introduction & Vision](#1-introduction--vision)  
2. [Core Features](#2-core-features)  
3. [System Architecture](#3-system-architecture)  
   1. [Frontend Architecture](#31-frontend-architecture)  
   2. [Backend Services](#32-backend-services)  
   3. [AI & Third-Party Integrations](#33-ai--third-party-integrations)  
4. [User Workflow & States](#4-user-workflow--states)  
   1. [Setup State](#41-setup-state)  
   2. [Practice State](#42-practice-state)  
   3. [Review State](#43-review-state)  
5. [Error Handling, Security, & Scalability](#5-error-handling-security--scalability)  
6. [API Definitions & Data Models](#6-api-definitions--data-models)  
   1. [Vocabulary API](#61-vocabulary-api)  
   2. [Sentence Generation API](#62-sentence-generation-api)  
   3. [Grading System API](#63-grading-system-api)  
7. [Future Enhancements & Roadmap](#7-future-enhancements--roadmap)  
8. [Conclusion](#8-conclusion)

---

## 1. Introduction & Vision

### 1.1 Purpose

The primary goal of this application is to facilitate **effective Chinese language learning**. It accomplishes this by generating **simple, beginner-level sentences** and enabling users to **upload images or typed text** that the app can then **transcribe, translate, and grade** using advanced AI models. Through iterative practice and feedback loops, learners can steadily improve their reading and writing skills.

### 1.2 Vision

- **Adaptive Learning Experience**  
  Evolve the difficulty level of generated sentences based on each user’s performance trends.
- **Accessible & Engaging**  
  Provide interactive features that keep users motivated—ranging from real-time guidance on stroke order to gamified achievements.
- **Scalable & Future-Proof**  
  Employ a microservices architecture to accommodate new features (e.g., advanced conversation simulations, listening exercises) without disrupting existing services.

---

## 2. Core Features

1. **Dynamic Sentence Generation**  
   - Generates Chinese sentences using HSK 1-2 grammar and vocabulary.  
   - Incorporates simple phrases and contexts (e.g., “I went to the store today” or “I ate an apple yesterday”).

2. **Interactive Practice Mode**  
   - Allows users to upload images (handwritten or printed text) or typed submissions.  
   - Processes the input using OCR or text analysis, evaluating correctness, vocabulary usage, and grammar.

3. **Comprehensive Feedback & Grading**  
   - Transcribes the user’s submission and provides literal translations.  
   - Issues a **letter grade** (S-Rank scale: S, A, B, C, etc.) reflecting the accuracy of the transcription.  
   - Offers tips for improvement—such as stroke order corrections, vocabulary expansions, or simplified grammar clarifications.

4. **Robust Architecture**  
   - Ensures **security** through HTTPS, token-based auth, and role-based access control (if needed).  
   - Delivers **scalability** through containerized microservices (Docker + orchestration with Kubernetes or similar).

---

## 3. System Architecture

A **hybrid** of microservices and AI components underpins this application, ensuring modularity and scalability.

### 3.1 Frontend Architecture

- **Framework Choice**  
  The frontend is developed as a **Single-Page Application (SPA)** in either **React** or **Vue.js**, chosen for their large ecosystem and strong community support.

- **State Management**  
  - **Redux** (for React) or **Vuex** (for Vue) to centralize user session data, practice states, and progress tracking.  
  - **Context API** or advanced libraries (e.g., Recoil, Pinia) can be substituted based on complexity and preference.

- **UI/UX Components**  
  - **Sentence Display**: Shows the AI-generated Chinese sentence at the top of the screen.  
  - **Upload/Submission Panel**: Drag-and-drop or file selector for images; typed submission field for typed text.  
  - **Feedback/Grading Panel**: Displays transcribed text, direct translations, and letter-grade feedback.

- **Client-Side Routing**  
  - Although a single-page, separate views or sections exist: “Home/Setup,” “Practice,” and “Review.”  
  - Implements transitions that maintain app context without full-page reloads.

---

### 3.2 Backend Services

1. **API Gateway**  
   - Receives all incoming requests from the frontend, applying authentication and rate-limiting policies if needed.  
   - Routes calls to the appropriate internal microservices.

2. **Word Bank / Vocabulary Service**  
   - **Endpoint**: `GET /api/groups/:id/words`  
   - Returns curated vocabulary sets from a database, cached to reduce subsequent access latency.  
   - May optionally track difficulty levels or HSK classification.

3. **Sentence Generation Service**  
   - **Endpoint**: `POST /api/sentence/generate`  
   - Receives a payload specifying a target vocabulary word or theme.  
   - Interacts with an LLM to produce an HSK 1-2 level sentence.

4. **Grading System Service**  
   A multi-stage pipeline that integrates different models and processes:
   1. **OCR**  
      - Processes the uploaded image with an OCR engine specialized for Chinese characters (e.g., **MangaOCR** or Tesseract tuned for Chinese).  
   2. **Translation**  
      - Uses an LLM or a standard translation API to produce a literal translation.  
   3. **Comparison & Grading**  
      - Compares the user’s transcribed text with the **target sentence**.  
      - Outputs a letter grade (S, A, B, C, etc.) plus improvement suggestions.

5. **Logging & Monitoring**  
   - Integrates with services like **Prometheus** for monitoring metrics (CPU, memory usage) and **Grafana** for visual dashboards.  
   - Uses **Sentry** or a similar tool for real-time error tracking and alerting.

---

### 3.3 AI & Third-Party Integrations

- **Sentence Generator LLM**  
  - A curated prompt ensures generated sentences adhere to the correct **HSK grammar and vocabulary scope**.
- **OCR Engine**  
  - **MangaOCR** or **Tesseract** (trained for Chinese) can be employed.  
  - The engine should handle varied handwriting styles and text orientations.
- **Translation & Grading Models**  
  - A single advanced model or multiple specialized models can handle literal translations and grading logic.  
  - **S-Rank** grading logic might factor in word order, character accuracy, and vocabulary completeness.

---

## 4. User Workflow & States

The application’s UI transitions the user seamlessly through three main states: **Setup**, **Practice**, and **Review**.

### 4.1 Setup State

1. **Display**  
   - A minimal screen with a “Generate Sentence” button.  
   - Basic instructions on how to proceed.

2. **Actions**  
   - On page load, the app fetches vocabulary words from the Word Bank service and caches them.  
   - Users press “Generate Sentence,” triggering the Sentence Generation Service to create a new Chinese sentence.

3. **Error Handling**  
   - In case of unreachable endpoints or timeouts, a modal is displayed with a “Retry” option or link to offline resources.

---

### 4.2 Practice State

1. **Display**  
   - Shows the newly generated Chinese sentence in large text for easy viewing.  
   - Provides an upload control for images or a text field for typed submissions.

2. **Actions**  
   - Users can upload an **image** (handwriting sample) or type their response.  
   - A “Submit for Review” button sends data to the Grading System service.

3. **Engagement & Guidance**  
   - The interface may show loading spinners (“Processing…”) or progress bars while the grading system is analyzing the input.  
   - May provide **tips** or sample references (like stroke animations) if needed.

---

### 4.3 Review State

1. **Display**  
   - The original Chinese sentence remains visible as reference.  
   - A **feedback panel** presents:
     - **Transcription**: OCR-derived or typed text.  
     - **Literal Translation**: Word-for-word breakdown of user’s text.  
     - **Grade & Feedback**: S-rank letter grade plus a short explanation highlighting errors or missed elements.

2. **Actions**  
   - **Next Question**: Returns user to the Setup State to request a new sentence.  
   - **Retry**: Lets the user resubmit if the grade is below a threshold (e.g., B or lower).

3. **User Feedback Mechanism**  
   - An optional button for “Report Issue” if the user suspects incorrect grading or translation.  
   - This data can feed into a system that fine-tunes or updates the grading model for better accuracy over time.

---

## 5. Error Handling, Security, & Scalability

### 5.1 Error Handling & Notifications

- **Client-Side Alerts**  
  - **Toast Notifications** or **Modals** inform the user about connectivity issues, server downtime, or incorrect file formats.  
- **Retry Logic**  
  - Automatic retries for minor network blips.  
  - Manual “Try Again” prompts for repeated failures.

### 5.2 Security Measures

1. **HTTPS Everywhere**  
   - All endpoints require SSL/TLS to protect user data.  
2. **Authentication & Authorization**  
   - For advanced features, implement **OAuth 2.0**, **JWT**, or a custom session token approach.  
3. **Access Control**  
   - Ensure roles (e.g., admin vs. standard user) or rate limiting to prevent abuse.  

### 5.3 Scalability & Load Handling

- **Microservices**  
  - Containerize each service (sentence generation, grading, vocabulary) and orchestrate horizontally (Kubernetes or Docker Swarm).  
- **Caching**  
  - Use a caching layer (like Redis) for frequently accessed data (e.g., vocabulary sets).  
- **Load Balancing**  
  - Distribute traffic among multiple instances of the same service to handle high user volume.

---

## 6. API Definitions & Data Models

### 6.1 Vocabulary API

- **Endpoint**  
  `GET /api/groups/:id/words`
- **Sample Response**  
  ```json
  {
    "groupId": "basic-hsk1",
    "words": [
      { "chinese": "汉字", "english": "character" },
      { "chinese": "苹果", "english": "apple" }
    ]
  }
  ```
- **Notes**  
  - Potentially grouped by HSK level or topic-based sets (e.g., food, travel, daily routine).

---

### 6.2 Sentence Generation API

- **Endpoint**  
  `POST /api/sentence/generate`
- **Request Body**  
  ```json
  {
    "word": "汉字"
  }
  ```
- **Response Body**  
  ```json
  {
    "sentence": "今天我学了一个新汉字。",
    "word": "汉字"
  }
  ```
- **Logic**  
  - The server prompts an LLM with a context that restricts grammar and vocabulary to HSK 1-2 levels.

---

### 6.3 Grading System API

- **Endpoint**  
  `POST /api/grade`
- **Request Body**  
  ```json
  {
    "targetSentence": "今天我学了一个新汉字。",
    "uploadedImage": "<base64-encoded image data>"
  }
  ```
- **Response Body**  
  ```json
  {
    "transcription": "今天我学了一个新汉字",
    "translation": "Today I learned a new Chinese character",
    "grade": "S",
    "feedback": "Excellent writing accuracy! Great job with stroke order."
  }
  ```
- **Workflow**  
  1. **OCR** extracts text from `uploadedImage`.  
  2. LLM compares `transcription` to `targetSentence`.  
  3. A letter grade is computed based on similarity and correctness.

---

## 7. Future Enhancements & Roadmap

1. **Adaptive Learning & Personalization**  
   - Dynamically adjust sentence complexity based on each user’s performance history.  
   - Personalized tips highlighting repeated errors or frequent mistakes.

2. **Gamification & Social Features**  
   - Leaderboards, daily streaks, and user achievements to drive engagement.  
   - Peer reviews or collaborative practice sessions.

3. **Expanded Language Support**  
   - Incorporate **Traditional Chinese** or other dialects.  
   - Potentially extend to other languages by changing the vocabulary bank and generation model constraints.

4. **Offline or Low-Bandwidth Mode**  
   - Cache essential resources on the client side to allow continued practice in areas with limited connectivity.

---

## 8. Conclusion

This **Chinese Learning App** combines advanced AI capabilities, a user-friendly frontend, and a robust backend architecture to deliver an immersive and effective language learning experience. By generating HSK 1-2 level sentences, providing real-time OCR-based grading, and offering structured feedback, it empowers learners to improve their Chinese reading and writing skills in an interactive, scalable environment.

The roadmap for future development includes **adaptive learning**, **community features**, and **multi-dialect support**, reflecting the app’s commitment to continuous innovation and responsiveness to user needs. With a well-defined microservices architecture, developers and stakeholders can seamlessly introduce new features, enhance performance, and ensure the platform remains secure and user-focused.
