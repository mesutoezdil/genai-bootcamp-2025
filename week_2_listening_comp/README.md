# Chinese Listening Comprehension Practice

Welcome to the Chinese Listening Comprehension Practice app! This interactive platform is designed to help learners improve their listening skills through dynamic exercises and real-time feedback. The application uses cutting-edge AWS services to generate natural-sounding Mandarin audio and generate relevant practice questions, making your study sessions both engaging and effective.

## Overview

The Chinese Listening Comprehension Practice app leverages Streamlit for an intuitive and interactive frontend, while the backend is responsible for generating both audio and questions using AWS Polly and Bedrock services. Whether you’re a beginner or an advanced learner, this app is designed to adapt to your pace and provide a seamless learning experience.

## Key Features

- **Dynamic Audio Generation:**  
  Uses AWS Polly and Bedrock to synthesize natural-sounding Mandarin audio for authentic listening practice.
  
- **Automated Question Generation:**  
  The backend creates context-specific questions to test your understanding and retention.
  
- **Interactive Learning Interface:**  
  A user-friendly Streamlit interface lets you select practice types and topics, view explanations, and receive instant feedback.
  
- **Session Persistence:**  
  Your progress and generated questions are stored locally, enabling you to revisit and review past exercises.

## System Requirements

- **Python Version:**  
  Python 3.8 or newer.

- **AWS Configuration:**  
  Valid AWS credentials must be configured on your system to access Polly and Bedrock services.  
  *Tip: Verify your AWS CLI configuration using `aws configure` before running the app.*

## Installation Guide

1. **Clone the Repository**

   Open your terminal and run:
   ```sh
   git clone <repository-url>
   cd listening-comp-main
   ```

2. **Backend Dependencies**

   Navigate to the backend directory and install dependencies:
   ```sh
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Frontend Dependencies**

   Install Streamlit (if not already installed):
   ```sh
   pip install streamlit
   ```

## Running the Application

### Starting the Frontend

Launch the interactive learning interface by running:
```sh
streamlit run frontend/main.py
```
This command opens the Streamlit app in your default web browser, where you can start practicing listening comprehension immediately.

### Running the Backend

If you need to run or debug backend processes separately, execute:
```sh
python backend/main.py
```
This ensures that all necessary services for audio and question generation are active.

## Project Structure

```
listening-comp-main/
├── backend/
│   ├── data/
│   │   └── stored_questions.json   # Persistent storage for generated questions
│   ├── audio_generator.py          # Audio synthesis using AWS services
│   ├── question_generator.py       # Question creation logic
│   ├── main.py                     # Backend entry point
│   └── requirements.txt            # Python dependencies for the backend
├── frontend/
│   ├── main.py                     # Streamlit app entry point
│   └── assets/                     # Images, icons, or other static assets
└── README.md                       # This file
```

## Usage and Tips

- **Selecting Practice Mode:**  
  Choose between dialogue-based or phrase matching exercises to target different listening skills.

- **Review Past Exercises:**  
  Use the sidebar to access your saved questions and review feedback to monitor your progress.

- **Audio Generation:**  
  If audio generation fails, ensure your AWS credentials are correctly configured and that your system meets the requirements.

## Troubleshooting

- **Audio File Not Generated:**  
  Verify that the AWS services are reachable and your credentials are valid. Check the logs printed in the terminal for detailed error messages.

- **Streamlit App Issues:**  
  Ensure that all frontend dependencies are installed. If you encounter issues, try running:
  ```sh
  pip install --upgrade streamlit
  ```

- **General Debugging:**  
  The app includes logging that writes detailed error messages to the console. Review these messages to help diagnose any issues.

## Contributing

We welcome contributions to improve the app further! If you’d like to contribute, please:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Ensure your code follows the existing style and add tests if possible.
- Submit a pull request with a clear description of your changes.

For any major changes, please open an issue first to discuss what you would like to change.
