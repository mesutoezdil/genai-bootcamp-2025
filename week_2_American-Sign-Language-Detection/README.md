# American Sign Language Detection

This repository provides a **comprehensive, real-time** pipeline for **American Sign Language (ASL)** detection and recognition using **computer vision** (OpenCV, MediaPipe), **machine learning** (scikit-learn), and **Python**. From **data collection** to **model training** and **real-time inference**, the project integrates a wide range of features – including a REST API, optional GUI, and an example Go client – to streamline ASL detection for research, educational, or prototype applications.

---

## Table of Contents

1. [Project Overview](#1-project-overview)  
2. [Features & Capabilities](#2-features--capabilities)  
3. [Technical Stack](#3-technical-stack)  
4. [Project Structure](#4-project-structure)  
5. [Setup & Installation](#5-setup--installation)  
   1. [Cloning the Repository](#51-cloning-the-repository)  
   2. [Python Virtual Environment](#52-python-virtual-environment)  
   3. [Dependency Installation](#53-dependency-installation)  
6. [Data Collection](#6-data-collection)  
7. [Model Training](#7-model-training)  
8. [Real-Time Detection](#8-real-time-detection)  
9. [REST API (Flask)](#9-rest-api-flask)  
   1. [Endpoints](#91-endpoints)  
   2. [Testing the API](#92-testing-the-api)  
10. [GUI (Optional)](#10-gui-optional)  
11. [Go Client (Optional)](#11-go-client-optional)  
12. [Contributing](#12-contributing)  
13. [License](#13-license)  
14. [Future Enhancements](#14-future-enhancements)

---

## 1. Project Overview

The **American Sign Language Detection** project aims to **recognize hand gestures** representing ASL letters (A-Z) from video or static images. Key objectives include:

- Providing a **user-friendly** pipeline to **collect**, **train**, and **deploy** sign detection models.
- Delivering **real-time** predictions through a combination of **OpenCV**, **MediaPipe** for landmark extraction, and **scikit-learn** for classification.
- Offering multiple interfaces:
  - **Command-line** scripts (for direct usage and automation).
  - **REST API** (Flask-based) for integration with web or mobile applications.
  - **Desktop GUI** for an immediate, interactive preview of sign recognition.
  - **Go client** example (optional) to demonstrate how other languages can interact with the Flask API.

---

## 2. Features & Capabilities

1. **Real-time ASL Detection**  
   - Utilizes a webcam feed processed by **OpenCV** and **MediaPipe**.  
   - Detects hand landmarks in each frame to infer the ASL letter.

2. **Static Image Processing**  
   - Allows users to **send images** (via REST API or script) for classification.  
   - Outputs the most probable ASL letter.

3. **REST API**  
   - Powered by **Flask**, providing endpoints for image upload and sign inference.  
   - Supports JSON responses with classification details.

4. **GUI Interface (Tkinter, Streamlit, etc.)**  
   - Offers a graphical environment to visualize real-time predictions and camera feed.  
   - Enhances accessibility for non-technical users.

5. **Language Clients**  
   - **Python** as the primary environment.  
   - Example **Go** client to showcase cross-language integration.

6. **Model Training & Customization**  
   - Scripts for data collection and model training using **scikit-learn** (SVM or other classifiers).  
   - Stores trained models and scaler in `models/` for easy deployment.

---

## 3. Technical Stack

- **Python 3.x**  
  - Primary development language for scripts, API, and desktop GUI.
- **OpenCV**  
  - Captures video frames, performs image manipulation, and routes them to the detection pipeline.
- **MediaPipe**  
  - Extracts **hand landmarks** (x, y coordinates) to form the input feature vector for classification.
- **Flask**  
  - Hosts the REST API, handling image uploads and returning classification predictions.
- **scikit-learn & joblib**  
  - Provides classical ML algorithms (e.g., SVM) and serialization of trained models and scalers.
- **Go (optional)**  
  - Demonstrates how a non-Python language can interface with the Flask API.

> **Note**: Additional libraries (e.g., NumPy, Pandas) facilitate data processing, while `mediapipe` focuses on robust hand-detection.

---

## 4. Project Structure

A typical folder layout is provided below. Adjust as needed for your environment:

```plaintext
.
├── README.md               # Main documentation (this file)
├── asl_data_collector.py   # Script to collect ASL data from webcam for building your dataset
├── asl_model_trainer.py    # Script to train a classifier (e.g., SVM) based on collected data
├── asl_api.py              # Flask-based REST API for inference on images
├── script.py               # Main script for real-time detection via webcam
├── gui.py                  # Optional GUI interface (e.g., Tkinter, Streamlit)
├── client.go               # Optional Go client interacting with the Flask API
├── models/
│   ├── asl_model.pkl       # Sample pretrained SVM model
│   └── scaler.pkl          # Associated scaler (feature normalization)
├── asl_dataset.csv         # Dataset (CSV) storing extracted landmarks
├── .gitignore              # Git ignore file to exclude venv and large artifacts
└── venv/                   # Python virtual environment directory (recommended to exclude from version control)
```

---

## 5. Setup & Installation

### 5.1 Cloning the Repository

```bash
git clone https://github.com/mesutoezdil/American-Sign-Language-Detection.git
cd American-Sign-Language-Detection
```

### 5.2 Python Virtual Environment

1. **Create & Activate**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. Confirm the environment is active by checking `(venv)` in your shell prompt.

### 5.3 Dependency Installation

Install the primary libraries (OpenCV, MediaPipe, scikit-learn, Flask, etc.):

```bash
pip install opencv-python mediapipe flask scikit-learn joblib numpy
```

> **Tip**: For large-scale training or GPU-based acceleration, you may also install libraries like TensorFlow or PyTorch (optional if you plan advanced feature extraction).

---

## 6. Data Collection

Creating a robust dataset is essential for **high detection accuracy**:

1. **Launch the Data Collector**:
   ```bash
   python asl_data_collector.py
   ```
2. **Webcam Feed**: The script typically opens your webcam and detects hand landmarks in real-time using MediaPipe.
3. **Capture & Label**:
   - Position your hand in a clear view.  
   - Press **Enter** to capture the frame.  
   - Type the **corresponding ASL letter** (e.g., ‘A’, ‘B’, etc.) and press **Enter** again.  
   - The system records the (x, y) landmark coordinates plus the labeled letter.
4. **Output**:  
   - A CSV file (e.g., `asl_dataset.csv`) storing each data sample.  
   - Over multiple sessions, gather **consistent** samples across all letters for balanced performance.

> **Tip**: Collect data under varied lighting conditions and camera angles to improve generalization.

---

## 7. Model Training

Once you have accumulated enough labeled data (the `.csv` file), train your classification model:

1. **Run the Training Script**:
   ```bash
   python asl_model_trainer.py
   ```
2. **Process**:
   - Reads `asl_dataset.csv`, performing feature scaling (e.g., MinMax or StandardScaler).  
   - Trains a **scikit-learn** classifier (default: SVM).  
   - Evaluates accuracy on a validation split or cross-validation if configured.  
3. **Model Persistence**:
   - Saves `asl_model.pkl` and `scaler.pkl` under the `models/` directory.  
   - These files are loaded later for **real-time detection** or **API inference**.

> **Tip**: You can modify the script to use different classifiers (e.g., Random Forest) or to adjust hyperparameters for better accuracy.

---

## 8. Real-Time Detection

To perform **live** ASL detection via your webcam:

1. **Launch the Main Script**:
   ```bash
   python script.py
   ```
2. **What It Does**:
   - Captures frames using **OpenCV**.  
   - Extracts hand landmarks with **MediaPipe**.  
   - Normalizes features via the loaded `scaler.pkl`.  
   - Infers the ASL letter using `asl_model.pkl`.  
3. **On-Screen Overlay**:
   - Typically, the script overlays the predicted letter on the webcam feed for immediate feedback.  
   - Adjust code or thresholds if false positives occur frequently.

---

## 9. REST API (Flask)

The project includes a **Flask application** to classify static images (or potentially base64 data) for easy integration with other systems.

1. **Start the Flask Server**:
   ```bash
   python asl_api.py
   ```
2. **Default Endpoint**:
   - Launches at `http://127.0.0.1:5000` unless the script is configured to use another port.

### 9.1 Endpoints

- **`POST /predict`**  
  - **Request**: Multipart form containing an image under the key `"image"`.  
  - **Response**: A JSON object specifying the predicted letter or an error message.

Sample response:
```json
{
  "prediction": "C"
}
```

### 9.2 Testing the API

Using **curl**:

```bash
curl -X POST \
  -F "image=@/path/to/your_image.jpg" \
  http://127.0.0.1:5000/predict
```

You should receive a JSON response with `{"prediction": "C"}` or another recognized letter.

> **Tip**: Tools like **Postman** or **Insomnia** can also be used to debug or test the endpoints interactively.

---

## 10. GUI (Optional)

For a **desktop or kiosk-style** interface:

1. **Run `gui.py`**:
   ```bash
   python gui.py
   ```
2. **Features**:
   - Live camera feed displayed in a UI window (e.g., Tkinter, PyQt, or Streamlit).  
   - Overlaid predictions and control buttons (start/stop detection, choose model, etc.).  
3. **Customizing**:
   - You can adapt the layout, add logging info, or embed advanced settings for the detection threshold.

---

## 11. Go Client (Optional)

This repository includes a **Go client** (`client.go`) to demonstrate cross-language usage:

1. **Edit Server URL**:
   - Update the `client.go` file to match your Flask API endpoint (e.g., `http://127.0.0.1:5000/predict`).
2. **Build & Run**:
   ```bash
   go build client.go
   ./client
   ```
3. **Usage**:
   - Typically reads an image path from the command line, sends it to the API, and prints the JSON response.

> **Note**: This is purely illustrative of how other languages/services can integrate with the ASL detection API.

---

## 12. Contributing

Contributions are welcome to enhance detection accuracy, add new features, or improve code quality.  
1. **Fork** the repository on GitHub.  
2. **Create a new branch** (`git checkout -b feature/new-feature`).  
3. **Commit** your changes with descriptive messages.  
4. **Push** to your fork (`git push origin feature/new-feature`).  
5. **Open a Pull Request** detailing changes and any relevant tests.

---

## 13. License

This project is licensed under the **MIT License**, granting permission to use, copy, modify, merge, publish, and distribute the software. See the `LICENSE` file for exact details.

---

## 14. Future Enhancements

Below are potential directions for expanding the system’s capabilities:

1. **Dynamic Gesture Recognition**  
   - Extend beyond static letters to words or phrases requiring motion (e.g., short gestures involving transitions).

2. **Multiple Hand Support**  
   - Adapt the pipeline to handle **two-hand** signs or track multiple users at once.

3. **Neural Network Integration**  
   - Replace classical SVM with **deep learning** models (TensorFlow, PyTorch) for higher accuracy and advanced feature extraction.

4. **Mobile or Edge Deployment**  
   - Export or convert the model for on-device inference on **Android** or **iOS**.  
   - Use frameworks like TensorFlow Lite or ONNX for optimized mobile performance.

5. **Data Augmentation & Validation**  
   - Incorporate augmentation (flips, rotations) in the data collection phase to bolster model robustness.  
   - Automate cross-validation to track model performance across different sessions or signers.

6. **Multilingual Gesture Recognition**  
   - Extend the approach to other sign languages (e.g., BSL, DGS) by collecting and labeling new datasets.
