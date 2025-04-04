from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
import joblib
import os
from pathlib import Path

# Ensure models directory exists
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

# Load trained model and scaler
try:
    model = joblib.load("models/asl_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
except FileNotFoundError:
    print(" Model files not found. Please train the model first.")
    model = None
    scaler = None

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict ASL letter from an uploaded image.
    
    Returns:
        JSON response with prediction or error message
    """
    # Check if model is loaded
    if model is None or scaler is None:
        return jsonify({"error": "Model not loaded"}), 500
        
    # Validate request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
        
    file = request.files['image']
    
    try:
        # Read and decode image
        image_data = file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
            
        # Process image with MediaPipe
        with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7
        ) as hands:
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.multi_hand_landmarks:
                return jsonify({"error": "No hand detected"}), 200

            # Extract hand landmarks
            for hand_landmarks in results.multi_hand_landmarks:
                data = []
                for landmark in hand_landmarks.landmark:
                    data.append(landmark.x)
                    data.append(landmark.y)

                # Scale and predict
                X_input = scaler.transform([data])
                prediction = model.predict(X_input)[0]
                confidence = max(model.predict_proba(X_input)[0])
                
                return jsonify({
                    "prediction": prediction,
                    "confidence": float(confidence),
                    "success": True
                })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None and scaler is not None
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)