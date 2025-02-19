# American Sign Language Detection

A comprehensive, real-time American Sign Language (ASL) detection system using computer vision and machine learning.

## Features

- **Real-time ASL Detection** via webcam (OpenCV + MediaPipe)
- **Static Image Processing** for ASL signs (API or script-based)
- **REST API** (Flask) for sign language prediction
- **GUI Interface** for easier interaction (Tkinter, Streamlit, etc.)
- **Python & Go** clients (optional Go client example)
- **Model Training** scripts to build your own classifier

---

## Technical Stack

- **Python 3.x**
- **OpenCV** for video capture and frame processing
- **MediaPipe** for hand (and optional face/pose) landmark detection
- **Flask** for RESTful API endpoints
- **scikit-learn** for machine learning (SVM, etc.)
- **Go** (optional) for a client implementation
- **joblib** for saving/loading models
- **numpy** for numeric operations

---

## Project Structure

```plaintext
.
├── README.md               # This documentation
├── asl_data_collector.py   # Data collection utility
├── asl_model_trainer.py    # Model training script
├── asl_api.py              # Flask API for ASL prediction
├── script.py               # Main script for real-time detection
├── gui.py                  # Graphical User Interface
├── client.go               # Optional Go client
├── models/
│   ├── asl_model.pkl       # Trained SVM model (example)
│   └── scaler.pkl          # Saved scaler
├── asl_dataset.csv         # Collected dataset for training
├── .gitignore              # Ignore rules (e.g. venv, large files)
└── venv/                   # Python virtual environment (ignored)
```

---

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mesutoezdil/American-Sign-Language-Detection.git
   cd American-Sign-Language-Detection
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install opencv-python mediapipe numpy flask scikit-learn joblib
   ```

---

## Data Collection

1. **Run the data collector**:
   ```bash
   python asl_data_collector.py
   ```
2. **Press enter** to capture a frame, type the corresponding ASL letter (A-Z), and press enter again.  
3. This saves the x,y landmark coordinates to `asl_dataset.csv`.

---

## Model Training

1. **Train the model**:
   ```bash
   python asl_model_trainer.py
   ```
2. This reads `asl_dataset.csv`, trains a scikit-learn SVM model, and saves:
   - `asl_model.pkl` (the classifier)
   - `scaler.pkl` (feature scaler)
   
Both are placed in the `models/` directory by default.

---

## Real-Time Detection

1. **Run the main detection script**:
   ```bash
   python script.py
   ```
2. It uses **OpenCV** for webcam input, **MediaPipe** for hand landmarks, and loads the SVM model from `models/asl_model.pkl`.

---

## REST API

1. **Start the Flask server**:
   ```bash
   python asl_api.py
   ```
2. By default, it runs on `http://127.0.0.1:5000` (or `5001` if port conflict).
3. **Test with `curl`**:
   ```bash
   curl -X POST -F "image=@/path/to/your_image.jpg" http://127.0.0.1:5000/predict
   ```
4. **API Endpoints**:
   - **POST** `/predict`
     - **Request**: Multipart form with key `"image"` for file upload.
     - **Response**: JSON with `"prediction": <letter>` or error message.

---

## GUI (Optional)

1. **Run the GUI**:
   ```bash
   python gui.py
   ```
2. Provides a desktop-based interface to visualize camera feed and predictions in real-time (implementation may vary).

---

## Go Client (Optional)

- `client.go` is an example for interacting with the Flask API in Go.
  - Edit the URL to match your local server address.
  - Build and run:
    ```bash
    go build client.go
    ./client
    ```

---

## Contributing

- Fork this repository
- Create a new branch (`git checkout -b feature/awesome-feature`)
- Commit your changes (`git commit -m 'Add awesome feature'`)
- Push to the branch (`git push origin feature/awesome-feature`)
- Open a Pull Request

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
