# Chinese Learning App – Technical Specifications

This document outlines a robust, scalable, and user-centric design for a Chinese learning application that leverages advanced AI capabilities for sentence generation, character transcription, translation, and performance grading. The app is designed to deliver an interactive learning experience while ensuring authenticity, security, and responsiveness.

---

## 1. Introduction

### 1.1. Purpose & Vision
- **Objective:**  
  Empower users to learn Chinese effectively by generating simple, beginner-level sentences and allowing them to practice writing Chinese characters with real-time feedback.
- **Vision:**  
  Create a highly engaging learning tool that adapts to user performance and supports continuous improvement through intelligent AI feedback, personalized analytics, and gamification elements.

### 1.2. Key Features
- **Dynamic Sentence Generation:**  
  Uses an AI-driven LLM to create sentences that adhere to HSK 1-2 grammar and vocabulary.
- **Interactive Practice Mode:**  
  Users can upload images of their handwritten or printed attempts, which are then processed by OCR and graded against the generated sentence.
- **Comprehensive Feedback:**  
  Provides transcription, literal translation, and detailed grading (using an S-Rank scale) along with actionable improvement suggestions.
- **Scalable and Secure Architecture:**  
  Ensures user data protection, real-time performance tracking, and seamless integration with external AI services.

---

## 2. System Architecture

### 2.1. Frontend Architecture
- **Framework:**  
  Developed as a Single-Page Application (SPA) using frameworks such as React or Vue.js.
- **State Management:**  
  Leverages Redux or Context API to manage state transitions across different user flows (Setup, Practice, Review).
- **UI/UX Components:**  
  Custom components for:
  - **Action Buttons:** “Generate Sentence”, “Submit for Review”, “Next Question”
  - **Upload Interface:** Image upload with drag-and-drop support and mobile responsiveness.
  - **Feedback Panels:** Detailed display of transcription, translation, and grading.
- **Routing & Navigation:**  
  Although a SPA, the app uses client-side routing for smooth transitions between states.

### 2.2. Backend Services
- **API Gateway:**  
  A centralized REST API gateway handling all client requests and coordinating between microservices.
- **Word Bank API:**  
  - **Endpoint:** `GET http://localhost:5000/api/groups/:id/words`  
  - **Function:** Returns a JSON array of Chinese words with English translations, which is cached in-memory to speed up subsequent accesses.
- **Sentence Generation Service:**  
  - **Endpoint:** `POST http://localhost:5000/api/sentence/generate`  
  - **Payload:** A JSON object including a randomly selected vocabulary word.  
  - **Response:** A generated Chinese sentence using controlled HSK-level grammar.
- **Grading System Service:**  
  A multi-stage pipeline:
  1. **Image Transcription:**  
     Uses an OCR engine (e.g., MangaOCR tuned for Chinese characters) to extract text from the uploaded image.
  2. **Literal Translation:**  
     Calls an LLM to provide a word-for-word translation of the transcribed text.
  3. **Performance Grading:**  
     A dedicated LLM or algorithm compares the transcribed text with the target sentence, assigning an S-Rank grade along with detailed feedback.
  - **Endpoint:** `POST http://localhost:5000/api/grade`
- **Logging & Monitoring:**  
  Integrates with tools like Sentry for error tracking and Prometheus/Grafana for performance monitoring.

### 2.3. AI and Third-Party Integrations
- **Sentence Generator LLM:**  
  Uses a controlled prompt to ensure generated sentences are simple, correct, and appropriate for beginners.
  - **Example Prompt:**  
    “Generate a simple Chinese sentence using the vocabulary word: **{{word}}**. Ensure the sentence uses HSK 1-2 grammar, incorporates basic vocabulary (e.g., book, car, apple), and includes simple temporal expressions (today, tomorrow, yesterday).”
- **OCR Engine:**  
  Integrates MangaOCR (or a similar high-accuracy service) specifically tuned for recognizing Chinese characters in varied handwriting styles.
- **Translation & Grading LLMs:**  
  Two distinct pipelines (or a combined model with dual functionality) that ensure:
  - A faithful literal translation.
  - A robust grading mechanism providing a letter grade (S-Rank scale) and improvement tips.

---

## 3. User Flow & Page States

The application is designed to guide the user through three main states with smooth transitions and responsive feedback.

### 3.1. Setup State
- **Display:**  
  A clean interface featuring a central “Generate Sentence” button.
- **Actions:**  
  - On initialization, the app fetches the vocabulary list.
  - When the button is pressed, a randomly selected word is used to generate a Chinese sentence via the Sentence Generation Service.
- **Error Handling:**  
  If the vocabulary fetch or sentence generation fails, an error modal with retry options is displayed.

### 3.2. Practice State
- **Display:**  
  - The generated Chinese sentence is prominently displayed.
  - An upload field is available below the sentence, allowing users to submit an image of their handwritten version.
  - A “Submit for Review” button is provided to initiate grading.
- **Actions:**  
  - Users capture or upload their attempt.
  - The image is immediately previewed to confirm selection.
  - On clicking “Submit for Review,” the app sends the image to the Grading System Service.
- **User Guidance:**  
  Real-time status indicators (e.g., “Uploading…”, “Processing…”) are shown to maintain user engagement.

### 3.3. Review State
- **Display:**  
  - The original Chinese sentence remains visible alongside an optional English reference.
  - A review panel presents:
    - **Transcription:** OCR-derived text from the uploaded image.
    - **Literal Translation:** An AI-generated word-for-word translation.
    - **Grading Details:**  
      - A letter grade on an S-Rank scale.
      - A detailed breakdown highlighting mistakes, character accuracy, and actionable tips.
- **Actions:**  
  - A “Next Question” button resets the interface and initiates a new practice session.
  - Option to “Retry” the current sentence if the grading score is below a predefined threshold.
- **Feedback Loop:**  
  Users can optionally submit feedback on the grading accuracy, aiding continuous improvement of the AI models.

---

## 4. Error Handling, Security, and Scalability

### 4.1. Error Handling & User Notifications
- **API Failures:**  
  Clear, user-friendly error messages are displayed in case of API timeouts or failures, with automatic retries where appropriate.
- **Input Validation:**  
  The app validates image formats and sizes before submission, ensuring optimal performance for OCR.
- **Fallbacks:**  
  In case of service outages, the system provides offline modes or cached content to prevent disruption of user learning.

### 4.2. Security Measures
- **Data Encryption:**  
  All data exchanges (API calls, image uploads) use HTTPS to ensure secure transmission.
- **Authentication & Authorization:**  
  (For future versions) Integration with OAuth or JWT-based authentication to manage user sessions and protect personal progress data.
- **Access Controls:**  
  Backend APIs enforce strict access control to prevent unauthorized data access or manipulation.

### 4.3. Scalability & Performance
- **Caching Strategy:**  
  - In-memory caching (e.g., Redis) for vocabulary lists and frequently used sentences.
  - API rate limiting to protect backend services during high load.
- **Microservices Architecture:**  
  Each service (sentence generation, grading, OCR) is containerized (e.g., Docker) and orchestrated (e.g., Kubernetes) for horizontal scaling.
- **Monitoring & Analytics:**  
  Real-time analytics dashboards track user engagement, error rates, and system performance, informing proactive optimizations.

---

## 5. API Definitions & Data Models

### 5.1. Vocabulary API
- **Endpoint:** `GET /api/groups/:id/words`
- **Response Format:**
  ```json
  {
    "groupId": "string",
    "words": [
      {
        "chinese": "汉字",
        "english": "character"
      },
      ...
    ]
  }
  ```

### 5.2. Sentence Generation API
- **Endpoint:** `POST /api/sentence/generate`
- **Request Body:**
  ```json
  {
    "word": "汉字"
  }
  ```
- **Response Body:**
  ```json
  {
    "sentence": "今天我在书店买了一本书。",
    "word": "汉字"
  }
  ```

### 5.3. Grading System API
- **Endpoint:** `POST /api/grade`
- **Request Body:**
  ```json
  {
    "targetSentence": "今天我在书店买了一本书。",
    "uploadedImage": "<base64-encoded image data>"
  }
  ```
- **Response Body:**
  ```json
  {
    "transcription": "今天我在书店买了一本书",
    "translation": "Today I bought a book at the bookstore",
    "grade": "A",
    "feedback": "Great accuracy! Watch out for stroke order in some characters."
  }
  ```

---

## 6. Future Enhancements & Roadmap

### 6.1. Adaptive Learning & Personalization
- **Dynamic Difficulty Adjustment:**  
  Adapt sentence complexity based on user performance trends.
- **Personalized Feedback:**  
  Use machine learning to analyze common mistakes over time and tailor future feedback.

### 6.2. Community & Social Features
- **Peer Reviews:**  
  Allow users to share their attempts and receive community feedback.
- **Gamification:**  
  Introduce achievements, leaderboards, and streak rewards to incentivize daily practice.

### 6.3. Extended Language Support
- **Multi-Dialect Support:**  
  Explore support for traditional Chinese characters and regional dialects.
- **Additional Learning Modules:**  
  Extend the system to cover vocabulary drills, listening exercises, and cultural notes.