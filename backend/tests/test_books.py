"""
Unit tests for book management endpoints
"""
import pytest


class TestBooks:
    """Test book management functionality"""

    def test_get_books_list(self, client, auth_headers):
        """Test retrieving the list of books"""
        response = client.get('/api/books', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

    def test_get_books_unauthorized(self, client):
        """Test getting books without authentication"""
        response = client.get('/api/books')
        assert response.status_code == 401

    def test_create_book_as_admin(self, client, auth_headers, sample_book):
        """Test creating a new book as admin"""
        response = client.post('/api/books', json=sample_book, headers=auth_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data['isbn'] == sample_book['isbn']
        assert data['title'] == sample_book['title']
        assert data['available_copies'] == sample_book['total_copies']

    def test_create_book_missing_fields(self, client, auth_headers):
        """Test creating a book with missing required fields"""
        incomplete_book = {
            'title': 'Incomplete Book'
            # Missing required fields
        }
        response = client.post('/api/books', json=incomplete_book, headers=auth_headers)
        assert response.status_code == 400

    def test_get_single_book(self, client, auth_headers, sample_book):
        """Test retrieving a single book by ID"""
        # First create a book
        create_response = client.post('/api/books', json=sample_book, headers=auth_headers)
        assert create_response.status_code == 201
        book_data = create_response.get_json()
        assert book_data is not None
        assert 'id' in book_data
        book_id = book_data['id']

        # Then retrieve it
        response = client.get(f'/api/books/{book_id}', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == book_id
        assert data['title'] == sample_book['title']

    def test_get_nonexistent_book(self, client, auth_headers):
        """Test retrieving a book that doesn't exist"""
        response = client.get('/api/books/99999', headers=auth_headers)
        assert response.status_code == 404

    def test_update_book(self, client, auth_headers, sample_book):
        """Test updating an existing book"""
        # Create a book first
        create_response = client.post('/api/books', json=sample_book, headers=auth_headers)
        assert create_response.status_code == 201
        book_data = create_response.get_json()
        assert book_data is not None
        assert 'id' in book_data
        book_id = book_data['id']

        # Update the book
        update_data = {
            'title': 'Updated Test Book',
            'total_copies': 10
        }
        response = client.put(f'/api/books/{book_id}', json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Test Book'
        assert data['total_copies'] == 10

    def test_delete_book(self, client, auth_headers, sample_book):
        """Test deleting a book"""
        # Create a book first
        create_response = client.post('/api/books', json=sample_book, headers=auth_headers)
        assert create_response.status_code == 201
        book_data = create_response.get_json()
        assert book_data is not None
        assert 'id' in book_data
        book_id = book_data['id']

        # Delete the book
        response = client.delete(f'/api/books/{book_id}', headers=auth_headers)
        assert response.status_code == 200

        # Verify it's deleted
        get_response = client.get(f'/api/books/{book_id}', headers=auth_headers)
        assert get_response.status_code == 404

    def test_search_books(self, client, auth_headers, sample_book):
        """Test searching for books"""
        # Create a book first
        client.post('/api/books', json=sample_book, headers=auth_headers)

        # Search for it
        response = client.get('/api/books?search=Test', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0
        assert any(book['title'] == 'Test Book' for book in data)
