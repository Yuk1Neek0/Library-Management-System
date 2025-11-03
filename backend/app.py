from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import hashlib
from database import get_db, init_db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
jwt = JWTManager(app)

# Initialize database
init_db()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password') or not data.get('full_name'):
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    password = hashlib.sha256(data['password'].encode()).hexdigest()
    full_name = data['full_name']
    role = data.get('role', 'student')

    # Validate role
    if role not in ['student', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO users (email, password, full_name, role) VALUES (?, ?, ?, ?)',
            (email, password, full_name, role)
        )
        conn.commit()
        user_id = cursor.lastrowid

        access_token = create_access_token(identity={'user_id': user_id, 'email': email, 'role': role})

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': full_name,
                'role': role
            }
        }), 201
    except Exception as e:
        return jsonify({'error': 'Email already exists'}), 409
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    email = data['email']
    password = hashlib.sha256(data['password'].encode()).hexdigest()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={
        'user_id': user['id'],
        'email': user['email'],
        'role': user['role']
    })

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user['role']
        }
    }), 200

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    current_user = get_jwt_identity()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id, email, full_name, role FROM users WHERE id = ?', (current_user['user_id'],))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user['id'],
        'email': user['email'],
        'full_name': user['full_name'],
        'role': user['role']
    }), 200

# Book endpoints
@app.route('/api/books', methods=['GET'])
@jwt_required()
def get_books():
    """Get all books with optional search and filter"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    available_only = request.args.get('available_only', 'false').lower() == 'true'

    conn = get_db()
    cursor = conn.cursor()

    query = 'SELECT * FROM books WHERE 1=1'
    params = []

    if search:
        query += ' AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])

    if category:
        query += ' AND category = ?'
        params.append(category)

    if available_only:
        query += ' AND available_copies > 0'

    query += ' ORDER BY title'

    cursor.execute(query, params)
    books = cursor.fetchall()
    conn.close()

    return jsonify([dict(book) for book in books]), 200

@app.route('/api/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    """Get a specific book by ID"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify(dict(book)), 200

@app.route('/api/books', methods=['POST'])
@jwt_required()
def add_book():
    """Add a new book (admin only)"""
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()

    if not data or not data.get('title') or not data.get('author'):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''INSERT INTO books (isbn, title, author, category, total_copies, available_copies, description)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                data.get('isbn'),
                data['title'],
                data['author'],
                data.get('category'),
                data.get('total_copies', 1),
                data.get('available_copies', 1),
                data.get('description')
            )
        )
        conn.commit()
        book_id = cursor.lastrowid

        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()

        return jsonify(dict(book)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """Update a book (admin only)"""
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    # Check if book exists
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Book not found'}), 404

    # Build update query dynamically
    update_fields = []
    params = []

    for field in ['isbn', 'title', 'author', 'category', 'total_copies', 'available_copies', 'description']:
        if field in data:
            update_fields.append(f'{field} = ?')
            params.append(data[field])

    if not update_fields:
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400

    params.append(book_id)
    query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = ?"

    cursor.execute(query, params)
    conn.commit()

    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()

    return jsonify(dict(book)), 200

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """Delete a book (admin only)"""
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Book not found'}), 404

    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Book deleted successfully'}), 200

# Loan endpoints
@app.route('/api/loans', methods=['GET'])
@jwt_required()
def get_loans():
    """Get loans (all for admin, own for students)"""
    current_user = get_jwt_identity()

    conn = get_db()
    cursor = conn.cursor()

    if current_user['role'] == 'admin':
        cursor.execute('''
            SELECT l.*, b.title, b.author, u.email, u.full_name
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            ORDER BY l.borrow_date DESC
        ''')
    else:
        cursor.execute('''
            SELECT l.*, b.title, b.author
            FROM loans l
            JOIN books b ON l.book_id = b.id
            WHERE l.user_id = ?
            ORDER BY l.borrow_date DESC
        ''', (current_user['user_id'],))

    loans = cursor.fetchall()
    conn.close()

    return jsonify([dict(loan) for loan in loans]), 200

@app.route('/api/loans', methods=['POST'])
@jwt_required()
def borrow_book():
    """Borrow a book"""
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('book_id'):
        return jsonify({'error': 'Missing book_id'}), 400

    book_id = data['book_id']

    conn = get_db()
    cursor = conn.cursor()

    # Check if book is available
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if not book:
        conn.close()
        return jsonify({'error': 'Book not found'}), 404

    if book['available_copies'] <= 0:
        conn.close()
        return jsonify({'error': 'Book is not available'}), 400

    # Check if user already has this book
    cursor.execute(
        'SELECT * FROM loans WHERE user_id = ? AND book_id = ? AND status = ?',
        (current_user['user_id'], book_id, 'active')
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'You already have this book borrowed'}), 400

    # Create loan
    due_date = datetime.now() + timedelta(days=14)  # 2 weeks loan period

    cursor.execute(
        'INSERT INTO loans (user_id, book_id, due_date) VALUES (?, ?, ?)',
        (current_user['user_id'], book_id, due_date)
    )

    # Update available copies
    cursor.execute(
        'UPDATE books SET available_copies = available_copies - 1 WHERE id = ?',
        (book_id,)
    )

    conn.commit()
    loan_id = cursor.lastrowid

    cursor.execute('''
        SELECT l.*, b.title, b.author
        FROM loans l
        JOIN books b ON l.book_id = b.id
        WHERE l.id = ?
    ''', (loan_id,))
    loan = cursor.fetchone()
    conn.close()

    return jsonify(dict(loan)), 201

@app.route('/api/loans/<int:loan_id>/return', methods=['POST'])
@jwt_required()
def return_book(loan_id):
    """Return a borrowed book"""
    current_user = get_jwt_identity()

    conn = get_db()
    cursor = conn.cursor()

    # Get loan
    cursor.execute('SELECT * FROM loans WHERE id = ?', (loan_id,))
    loan = cursor.fetchone()

    if not loan:
        conn.close()
        return jsonify({'error': 'Loan not found'}), 404

    # Check if user owns this loan or is admin
    if loan['user_id'] != current_user['user_id'] and current_user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403

    if loan['status'] == 'returned':
        conn.close()
        return jsonify({'error': 'Book already returned'}), 400

    # Update loan
    cursor.execute(
        'UPDATE loans SET return_date = ?, status = ? WHERE id = ?',
        (datetime.now(), 'returned', loan_id)
    )

    # Update available copies
    cursor.execute(
        'UPDATE books SET available_copies = available_copies + 1 WHERE id = ?',
        (loan['book_id'],)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Book returned successfully'}), 200

# User management endpoints (admin only)
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id, email, full_name, role, created_at FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    conn.close()

    return jsonify([dict(user) for user in users]), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user role (admin only)"""
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()

    if not data or 'role' not in data:
        return jsonify({'error': 'Missing role field'}), 400

    if data['role'] not in ['student', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET role = ? WHERE id = ?', (data['role'], user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User updated successfully'}), 200

# Statistics endpoint
@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get system statistics (admin only)"""
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as count FROM books')
    total_books = cursor.fetchone()['count']

    cursor.execute('SELECT SUM(available_copies) as count FROM books')
    available_books = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM users')
    total_users = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM loans WHERE status = ?', ('active',))
    active_loans = cursor.fetchone()['count']

    conn.close()

    return jsonify({
        'total_books': total_books,
        'available_books': available_books or 0,
        'total_users': total_users,
        'active_loans': active_loans
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
