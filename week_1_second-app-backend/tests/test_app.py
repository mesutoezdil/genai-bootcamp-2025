"""Test suite for the main application module."""
import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for our app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route returns welcome message."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Extended Chinese Learning App' in response.data

def test_error_handler(client):
    """Test the global error handler."""
    # Test a non-existent route to trigger 404
    response = client.get('/non-existent-route')
    assert response.status_code == 404
    
    # The response should be JSON
    assert response.content_type == 'application/json'
