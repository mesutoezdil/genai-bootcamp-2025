"""Configuration file for pytest."""
import pytest
import os
import tempfile
from app import app
from lib.db import init_db

@pytest.fixture
def app_context():
    """Create an application context for testing."""
    with app.app_context() as ctx:
        yield ctx

@pytest.fixture
def test_db():
    """Create a temporary database for testing."""
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    
    # Initialize the test database
    with app.app_context():
        init_db()
    
    yield db_path
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(test_db):
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
