"""Test suite for the words module."""
import pytest
from app import app
import json

@pytest.fixture
def client():
    """Create a test client for our app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_words(client):
    """Test getting the list of words."""
    response = client.get('/api/words')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_word(client):
    """Test getting a specific word."""
    # First create a word
    word_data = {
        "character": "你",
        "pinyin": "nǐ",
        "meaning": "you",
        "level": "HSK1"
    }
    post_response = client.post('/api/words', json=word_data)
    assert post_response.status_code == 201
    word_id = json.loads(post_response.data)['id']
    
    # Then retrieve it
    get_response = client.get(f'/api/words/{word_id}')
    assert get_response.status_code == 200
    data = json.loads(get_response.data)
    assert data['character'] == "你"
    assert data['pinyin'] == "nǐ"

def test_create_word(client):
    """Test creating a new word."""
    word_data = {
        "character": "好",
        "pinyin": "hǎo",
        "meaning": "good",
        "level": "HSK1"
    }
    response = client.post('/api/words', json=word_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['character'] == "好"

def test_update_word(client):
    """Test updating a word."""
    # First create a word
    word_data = {
        "character": "是",
        "pinyin": "shì",
        "meaning": "to be",
        "level": "HSK1"
    }
    post_response = client.post('/api/words', json=word_data)
    assert post_response.status_code == 201
    word_id = json.loads(post_response.data)['id']
    
    # Then update it
    update_data = {
        "meaning": "is/are/am",
        "level": "HSK2"
    }
    put_response = client.put(f'/api/words/{word_id}', json=update_data)
    assert put_response.status_code == 200
    data = json.loads(put_response.data)
    assert data['meaning'] == "is/are/am"
    assert data['level'] == "HSK2"

def test_delete_word(client):
    """Test deleting a word."""
    # First create a word
    word_data = {
        "character": "再见",
        "pinyin": "zàijiàn",
        "meaning": "goodbye",
        "level": "HSK1"
    }
    post_response = client.post('/api/words', json=word_data)
    assert post_response.status_code == 201
    word_id = json.loads(post_response.data)['id']
    
    # Then delete it
    delete_response = client.delete(f'/api/words/{word_id}')
    assert delete_response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f'/api/words/{word_id}')
    assert get_response.status_code == 404
