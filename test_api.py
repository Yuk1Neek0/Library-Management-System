#!/usr/bin/env python
"""Test script to verify API is working correctly"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_health():
    """Test health endpoint"""
    response = requests.get('http://localhost:5000/health')
    print(f"Health check: {response.status_code}")
    print(response.json())
    print()

def test_login():
    """Test login and return token"""
    data = {
        'email': 'admin@library.com',
        'password': 'admin123'
    }
    response = requests.post(f'{BASE_URL}/auth/login', json=data)
    print(f"Login: {response.status_code}")
    result = response.json()
    print(f"User: {result.get('user')}")
    token = result.get('access_token')
    print(f"Token: {token[:50]}..." if token else "No token")
    print()
    return token

def test_get_books(token):
    """Test getting books with token"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{BASE_URL}/books', headers=headers)
    print(f"Get Books: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"Found {len(books)} books")
    else:
        print(f"Error: {response.json()}")
    print()

def test_get_loans(token):
    """Test getting loans with token"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{BASE_URL}/loans', headers=headers)
    print(f"Get Loans: {response.status_code}")
    if response.status_code == 200:
        loans = response.json()
        print(f"Found {len(loans)} loans")
    else:
        print(f"Error: {response.json()}")
    print()

if __name__ == '__main__':
    print("Testing Library API")
    print("="*50)
    print()

    test_health()
    token = test_login()

    if token:
        test_get_books(token)
        test_get_loans(token)
    else:
        print("Login failed, cannot test authenticated endpoints")
