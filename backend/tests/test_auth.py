"""
Unit tests for authentication endpoints
"""
import pytest


class TestAuthentication:
    """Test authentication functionality"""

    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_register_new_user(self, client, sample_user):
        """Test registering a new user"""
        response = client.post('/api/auth/register', json=sample_user)
        assert response.status_code == 201
        data = response.get_json()
        assert 'access_token' in data
        assert data['user']['email'] == sample_user['email']
        assert data['user']['role'] == 'student'

    def test_register_duplicate_email(self, client, sample_user):
        """Test registering with an already existing email"""
        # Register first time
        client.post('/api/auth/register', json=sample_user)

        # Try to register again with same email
        response = client.post('/api/auth/register', json=sample_user)
        assert response.status_code == 400
        data = response.get_json()
        assert 'already exists' in data['error'].lower()

    def test_login_success(self, client):
        """Test successful login with default admin credentials"""
        response = client.post('/api/auth/login', json={
            'email': 'admin@library.com',
            'password': 'admin123'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert data['user']['email'] == 'admin@library.com'
        assert data['user']['role'] == 'admin'

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'email': 'admin@library.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
        data = response.get_json()
        assert 'invalid' in data['error'].lower()

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })
        assert response.status_code == 401

    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information"""
        response = client.get('/api/auth/me', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'admin@library.com'
        assert data['role'] == 'admin'

    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get('/api/auth/me')
        assert response.status_code == 401
