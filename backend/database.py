import sqlite3
from datetime import datetime
import hashlib
import os

DATABASE = 'library.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Loans table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP NOT NULL,
            return_date TIMESTAMP,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')

    # Holds/Reservations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            hold_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'waiting',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')

    conn.commit()

    # Create default admin user if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@library.com',))
    if not cursor.fetchone():
        admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute(
            'INSERT INTO users (email, password, full_name, role) VALUES (?, ?, ?, ?)',
            ('admin@library.com', admin_password, 'Administrator', 'admin')
        )
        conn.commit()
        print("Default admin user created: admin@library.com / admin123")

    # Add sample books if database is empty
    cursor.execute('SELECT COUNT(*) as count FROM books')
    if cursor.fetchone()['count'] == 0:
        sample_books = [
            ('978-0-13-468599-1', 'Clean Code', 'Robert C. Martin', 'Programming', 3, 3, 'A handbook of agile software craftsmanship'),
            ('978-0-201-63361-0', 'Design Patterns', 'Gang of Four', 'Programming', 2, 2, 'Elements of reusable object-oriented software'),
            ('978-0-13-235088-4', 'Clean Architecture', 'Robert C. Martin', 'Programming', 2, 2, 'A craftsman\'s guide to software structure'),
            ('978-0-7356-6745-7', 'The Pragmatic Programmer', 'David Thomas', 'Programming', 3, 3, 'Your journey to mastery'),
            ('978-1-59327-928-8', 'Python Crash Course', 'Eric Matthes', 'Programming', 4, 4, 'A hands-on introduction to programming'),
        ]

        cursor.executemany(
            'INSERT INTO books (isbn, title, author, category, total_copies, available_copies, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            sample_books
        )
        conn.commit()
        print(f"Added {len(sample_books)} sample books")

    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
