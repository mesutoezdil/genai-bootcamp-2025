"""Test suite for the study sessions module."""
import pytest
from app import app
import json
from datetime import datetime

@pytest.fixture
def client():
    """Create a test client for our app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_sessions(client):
    """Test getting the list of study sessions."""
    response = client.get('/api/sessions')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_session(client):
    """Test creating a new study session."""
    session_data = {
        "start_time": datetime.now().isoformat(),
        "duration_minutes": 30,
        "focus_area": "vocabulary",
        "notes": "Focused on HSK1 vocabulary"
    }
    response = client.post('/api/sessions', json=session_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['duration_minutes'] == 30
    assert data['focus_area'] == "vocabulary"

def test_get_session(client):
    """Test getting a specific study session."""
    # First create a session
    session_data = {
        "start_time": datetime.now().isoformat(),
        "duration_minutes": 45,
        "focus_area": "grammar",
        "notes": "Practiced basic sentence structures"
    }
    post_response = client.post('/api/sessions', json=session_data)
    assert post_response.status_code == 201
    session_id = json.loads(post_response.data)['id']
    
    # Then retrieve it
    get_response = client.get(f'/api/sessions/{session_id}')
    assert get_response.status_code == 200
    data = json.loads(get_response.data)
    assert data['duration_minutes'] == 45
    assert data['focus_area'] == "grammar"

def test_update_session(client):
    """Test updating a study session."""
    # First create a session
    session_data = {
        "start_time": datetime.now().isoformat(),
        "duration_minutes": 20,
        "focus_area": "listening",
        "notes": "Initial notes"
    }
    post_response = client.post('/api/sessions', json=session_data)
    assert post_response.status_code == 201
    session_id = json.loads(post_response.data)['id']
    
    # Then update it
    update_data = {
        "duration_minutes": 25,
        "notes": "Updated notes after completion"
    }
    put_response = client.put(f'/api/sessions/{session_id}', json=update_data)
    assert put_response.status_code == 200
    data = json.loads(put_response.data)
    assert data['duration_minutes'] == 25
    assert data['notes'] == "Updated notes after completion"

def test_delete_session(client):
    """Test deleting a study session."""
    # First create a session
    session_data = {
        "start_time": datetime.now().isoformat(),
        "duration_minutes": 15,
        "focus_area": "reading",
        "notes": "Quick reading practice"
    }
    post_response = client.post('/api/sessions', json=session_data)
    assert post_response.status_code == 201
    session_id = json.loads(post_response.data)['id']
    
    # Then delete it
    delete_response = client.delete(f'/api/sessions/{session_id}')
    assert delete_response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f'/api/sessions/{session_id}')
    assert get_response.status_code == 404

def test_get_session_statistics(client):
    """Test getting study session statistics."""
    response = client.get('/api/sessions/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_sessions' in data
    assert 'total_minutes' in data
    assert 'average_duration' in data
