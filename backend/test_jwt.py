"""Test JWT configuration directly"""
from app import app, jwt
from flask_jwt_extended import create_access_token, decode_token
import sys

with app.app_context():
    print("Testing JWT Configuration")
    print("="*50)

    # Check configuration
    print("\nJWT Configuration:")
    print(f"JWT_TOKEN_LOCATION: {app.config.get('JWT_TOKEN_LOCATION')}")
    print(f"JWT_CSRF_IN_COOKIES: {app.config.get('JWT_CSRF_IN_COOKIES')}")
    print(f"JWT_COOKIE_CSRF_PROTECT: {app.config.get('JWT_COOKIE_CSRF_PROTECT')}")
    print(f"JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')[:20]}...")

    # Create a token
    print("\nCreating test token...")
    token = create_access_token(
        identity='1',
        additional_claims={'email': 'test@example.com', 'role': 'admin'}
    )
    print(f"Token created: {token[:50]}...")

    # Try to decode it
    print("\nDecoding token...")
    try:
        decoded = decode_token(token)
        print(f"Token decoded successfully!")
        print(f"Identity: {decoded.get('sub')}")
    except Exception as e:
        print(f"Error decoding token: {e}")
        sys.exit(1)

    print("\n✓ JWT is working correctly!")
