# Chinese Listening Comprehension Practice

This application offers an **interactive** and **flexible** environment to enhance your **Chinese listening skills**. Combining a **Streamlit**-powered user interface with **AWS** (Polly and Bedrock) services, it generates **natural-sounding Mandarin audio** and context-specific questions, providing immediate feedback to accelerate your learning progress.

---

## Table of Contents

1. [Introduction & Vision](#1-introduction--vision)  
2. [Key Features](#2-key-features)  
3. [System Requirements](#3-system-requirements)  
4. [Installation & Setup](#4-installation--setup)  
5. [Running the Application](#5-running-the-application)  
   1. [Frontend (Streamlit)](#51-frontend-streamlit)  
   2. [Backend Processes](#52-backend-processes)  
6. [Project Structure](#6-project-structure)  
7. [Usage Tips](#7-usage-tips)  
8. [Troubleshooting](#8-troubleshooting)  
9. [Contributing](#9-contributing)  
10. [Future Roadmap](#10-future-roadmap)

---

## 1. Introduction & Vision

### 1.1 What Is It?

The **Chinese Listening Comprehension Practice** application provides a **dynamic** and **personalized** approach to mastering Mandarin listening skills. By generating on-the-fly audio content and questions tailored to different proficiency levels, this tool helps learners systematically improve through **focused exercises**.

### 1.2 Why Use It?

- **Adaptive Learning**: Offers exercises and practice modes that can scale from simple phrases to advanced dialogues.
- **Immediate Feedback**: Delivers near-instant evaluations of comprehension, ensuring users learn efficiently.
- **User-Centric Design**: Relies on a straightforward Streamlit front-end, making the experience approachable for learners at all levels.

---

## 2. Key Features

1. **Dynamic Audio Generation**  
   - Integrates **AWS Polly** and **Amazon Bedrock** to produce human-like Mandarin audio.  
   - Adjust speech parameters (speed, tone) for various listening drills.

2. **Automated Question Generation**  
   - The backend creates contextually relevant comprehension questions to test retention and understanding.  
   - Supports multiple question formats (multiple choice, fill-in-the-blank, open-ended) for varied practice.

3. **Interactive Streamlit Interface**  
   - Easy-to-use GUI enables quick switching between different exercise modes (dialogues, short phrases, etc.).  
   - Immediate results and explanations enhance the user’s learning loop.

4. **Session Persistence**  
   - Stores generated questions locally so learners can revisit previous drills and gauge progress over time.  
   - Ensures continuity across sessions, even if the application restarts.

---

## 3. System Requirements

- **Python Environment**  
  - Python **3.8** or newer recommended.

- **AWS Configuration**  
  - Valid **AWS credentials** with permissions for **Amazon Polly** and **Bedrock**.  
  - Confirm credentials by running `aws configure` and checking your AWS CLI profile.

- **Internet Connectivity**  
  - Required to connect to AWS services and fetch any remote libraries or dependencies.

---

## 4. Installation & Setup

### 4.1 Clone the Repository

1. Open a terminal in your desired installation directory.
2. Run:
   ```bash
   git clone <repository-url>
   cd listening-comp-main
   ```

### 4.2 Backend Dependencies

1. Navigate to the **backend** folder:
   ```bash
   cd backend
   ```
2. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Return to the root folder:
   ```bash
   cd ..
   ```

### 4.3 Frontend Dependencies

Install **Streamlit** and any additional libraries (if not already installed):

```bash
pip install streamlit
```

---

## 5. Running the Application

### 5.1 Frontend (Streamlit)

Launch the user-friendly **Streamlit** interface:

```bash
streamlit run frontend/main.py
```

Upon execution, Streamlit will open a new tab in your default web browser, displaying the listening comprehension app interface. Users can immediately select topics, exercise types, and begin practicing.

### 5.2 Backend Processes

If necessary (for debugging or separate testing), run:

```bash
python backend/main.py
```
This command starts the backend services that handle **audio generation** and **question creation**. If you don’t need to debug backend processes, the Streamlit app typically orchestrates them automatically.

---

## 6. Project Structure

A suggested layout for logical organization of files and directories:

```
listening-comp-main/
├── backend/
│   ├── data/
│   │   └── stored_questions.json   # Persistent storage of previously generated questions
│   ├── audio_generator.py          # AWS Polly / Bedrock-based audio generation logic
│   ├── question_generator.py       # Logic for dynamic question creation
│   ├── main.py                     # Backend entry point orchestrating generation tasks
│   └── requirements.txt            # Python dependencies for backend services
├── frontend/
│   ├── main.py                     # Streamlit app entry point
│   └── assets/                     # Static files (icons, images, CSS, etc.)
└── README.md                       # Main documentation
```

> **Note**: You can adapt this structure to your own project style – for example, placing `assets/` in the `backend` folder if the media files relate to data generation.

---

## 7. Usage Tips

1. **Choosing a Practice Mode**  
   - **Dialogue Mode**: Offers longer audio segments simulating short conversations. Best for advanced learners focusing on context clues.  
   - **Phrase Matching**: Targets shorter phrases or vocabulary sets, ideal for beginners building fundamental listening skills.

2. **Reviewing Past Exercises**  
   - Use the sidebar in the Streamlit app to revisit previously generated questions and your recorded answers.  
   - Compare your new results to old ones for an at-a-glance progress snapshot.

3. **AWS Considerations**  
   - If you experience slow audio generation or question creation, check your network connection or AWS region settings.  
   - Some AWS services may have region-specific constraints for new features like Amazon Bedrock.

---

## 8. Troubleshooting

### 8.1 Audio File Not Generated

- **Check AWS Connectivity**  
  Ensure your AWS credentials are correctly configured and have the required permissions (`Polly:*`, `Bedrock:*`).  
- **Inspect Logs**  
  Both the backend and Streamlit console logs may display error messages. Look for timeouts, credential errors, or missing libraries.

### 8.2 Streamlit App Issues

- **Dependency Mismatch**  
  If the app fails to load, verify that you installed **Streamlit** and other packages with the same Python environment.  
- **Update Streamlit**  
  Try running:
  ```bash
  pip install --upgrade streamlit
  ```
  to get the latest bug fixes and features.

### 8.3 General Debugging

- **Logs & Console Output**  
  Detailed logs are printed to the terminal. Always check the console for errors or stack traces.  
- **Verbose Mode**  
  You can add verbose flags or logging levels in your Python code to reveal more detailed error messages.

---

## 9. Contributing

We welcome contributions to further enhance this learning tool. To contribute:

1. **Fork** the repository.  
2. **Create a branch** for your feature or bug fix.  
3. **Add or modify tests** in your branch if applicable.  
4. **Open a Pull Request** with a clear description of your changes, screenshots, or logs demonstrating the feature or fix.

For major changes, please open an **issue** first to discuss the proposed feature with the community and maintainers.

---

## 10. Future Roadmap

1. **Customization of Audio Parameters**  
   - Expose more control (e.g., pitch, prosody, speaker selection) to enrich listening practice for different accents and speeds.

2. **Adaptive Difficulty**  
   - Dynamically adjust audio complexity and question depth based on user performance, gradually increasing the challenge.

3. **Community & Sharing**  
   - Implement user profiles, leaderboards, or shared practice sessions for collaborative learning.

4. **Expanded Format Support**  
   - Add video-based comprehension tasks or incorporate additional languages for bilingual or multilingual learning experiences.
