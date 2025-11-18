"""
Pytest configuration and fixtures for testing the Library Management System
"""
import os
import sys
import pytest
import tempfile

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from database import init_db
import sqlite3


@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()

    flask_app.config.update({
        'TESTING': True,
        'DATABASE': db_path,
        'JWT_SECRET_KEY': 'test-secret-key'
    })

    # Initialize the database
    with flask_app.app_context():
        init_db()

    yield flask_app

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):
    """Get authentication headers with admin token."""
    # Register and login as admin
    response = client.post('/api/auth/login', json={
        'email': 'admin@library.com',
        'password': 'admin123'
    })

    if response.status_code == 200:
        token = response.json.get('access_token')
        return {'Authorization': f'Bearer {token}'}

    return {}


@pytest.fixture
def sample_book():
    """Sample book data for testing."""
    return {
        'isbn': '978-0-123456-78-9',
        'title': 'Test Book',
        'author': 'Test Author',
        'category': 'Fiction',
        'total_copies': 5,
        'description': 'A test book for unit testing'
    }


@pytest.fixture
def sample_user():
    """Sample user data for testing."""
    return {
        'email': 'testuser@example.com',
        'password': 'password123',
        'full_name': 'Test User',
        'role': 'student'
    }
