"""
Unit tests for ASL model functionality.
"""

import os
import pytest
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import joblib

def test_model_file_exists():
    """Test if model file exists in the models directory."""
    assert os.path.exists("models/asl_model.pkl"), "Model file not found"
    assert os.path.exists("models/scaler.pkl"), "Scaler file not found"

def test_model_loading():
    """Test if model and scaler can be loaded."""
    try:
        model = joblib.load("models/asl_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
        assert isinstance(model, SVC), "Model is not an SVC instance"
        assert isinstance(scaler, StandardScaler), "Scaler is not a StandardScaler instance"
    except Exception as e:
        pytest.fail(f"Failed to load model: {e}")

def test_model_prediction():
    """Test if model can make predictions with sample data."""
    model = joblib.load("models/asl_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    
    # Create sample hand landmark data (42 features: 21 x,y coordinates)
    sample_data = np.random.rand(1, 42)
    
    # Scale the data
    scaled_data = scaler.transform(sample_data)
    
    # Make prediction
    prediction = model.predict(scaled_data)
    
    # Check if prediction is a valid ASL letter
    assert prediction[0] in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), "Invalid prediction"

def test_scaler_transformation():
    """Test if scaler can transform data correctly."""
    scaler = joblib.load("models/scaler.pkl")
    
    # Create sample data
    sample_data = np.random.rand(5, 42)
    
    # Transform data
    scaled_data = scaler.transform(sample_data)
    
    # Check if scaled data has zero mean and unit variance (approximately)
    assert np.abs(scaled_data.mean()) < 0.1, "Scaled data mean is not close to 0"
    assert np.abs(scaled_data.std() - 1) < 0.1, "Scaled data std is not close to 1"
