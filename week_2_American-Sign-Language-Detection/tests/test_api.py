"""
Unit tests for ASL API functionality.
"""

import os
import pytest
from flask import Flask
import cv2
import numpy as np
from asl_api import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_predict_endpoint_no_image(client):
    """Test /predict endpoint without an image."""
    response = client.post('/predict')
    assert response.status_code == 400
    assert b'No image file provided' in response.data

def test_predict_endpoint_invalid_image(client):
    """Test /predict endpoint with invalid image data."""
    data = {'image': (b'invalid_image_data', 'test.jpg')}
    response = client.post('/predict', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'Invalid image data' in response.data

def test_predict_endpoint_no_hand(client):
    """Test /predict endpoint with image containing no hand."""
    # Create a blank image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    _, img_encoded = cv2.imencode('.jpg', img)
    data = {'image': (img_encoded.tobytes(), 'test.jpg')}
    
    response = client.post('/predict', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'No hand detected' in response.data

def test_predict_endpoint_with_hand(client):
    """Test /predict endpoint with valid hand image."""
    # Skip if test image doesn't exist
    if not os.path.exists('data/test_hand.jpg'):
        pytest.skip("Test hand image not found")
        
    with open('data/test_hand.jpg', 'rb') as f:
        data = {'image': (f, 'test_hand.jpg')}
        response = client.post('/predict', data=data, content_type='multipart/form-data')
        
    assert response.status_code == 200
    assert 'prediction' in response.json
