# Library Management System

A comprehensive web-based Library Management System with user authentication, book management, and loan tracking capabilities.

## Team Members
- Sikai Han (Backend Development)
- Pritika Pritika (Frontend Development)
- Jeremiah Agbebi (DevOps Pipeline)
- Jakaran Singh (Monitoring & Maintenance)

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Default Credentials](#default-credentials)
- [CI/CD Strategy](#cicd-strategy)
- [Distributed Computing Approach](#distributed-computing-approach)
- [Team Challenge Requirements](#team-challenge-requirements)

## Features

### User Features
- **Authentication**: Secure registration and login system with JWT tokens
- **Book Browsing**: Search and filter books by title, author, ISBN, and category
- **Book Borrowing**: Borrow available books with automatic due date calculation (14 days)
- **Loan Management**: View active loans and loan history
- **Return Books**: Easy book return process

### Admin Features
- **Dashboard**: View system statistics (total books, users, active loans)
- **Book Management**: Add, edit, and delete books
- **User Management**: Manage user roles (student/admin)
- **Loan Tracking**: Monitor all active loans across the system

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Authentication**: JWT (Flask-JWT-Extended)
- **API**: RESTful API with JSON responses
- **CORS**: Flask-CORS for cross-origin requests

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios
- **Styling**: Custom CSS with responsive design

### Development Tools
- **IDE**: VS Code (recommended)
- **Version Control**: Git
- **Package Managers**: pip (Python), npm (Node.js)

## Project Structure

```
Library System/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── database.py            # Database initialization and setup
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   └── library.db            # SQLite database (auto-generated)
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable components (Navbar)
│   │   ├── pages/            # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Books.jsx
│   │   │   ├── MyLoans.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── AdminBooks.jsx
│   │   │   └── AdminUsers.jsx
│   │   ├── services/         # API services
│   │   │   └── api.js
│   │   ├── App.jsx           # Main app component
│   │   ├── App.css           # Global styles
│   │   └── main.jsx          # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── .gitignore
└── Documentation files
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Git

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python database.py
```

This will create:
- Database tables (users, books, loans, holds)
- Default admin account
- Sample books for testing

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend Server

1. Navigate to backend directory:
```bash
cd backend
```

2. Run the Flask application:
```bash
python app.py
```

The backend server will start at `http://localhost:5000`

### Start the Frontend Development Server

1. Open a new terminal and navigate to frontend directory:
```bash
cd frontend
```

2. Run the Vite development server:
```bash
npm run dev
```

The frontend will start at `http://localhost:3000`

### Access the Application

Open your web browser and go to: `http://localhost:3000`

## API Documentation

### Authentication Endpoints

#### POST /api/auth/register
Register a new user.
```json
Request Body:
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "student"
}

Response:
{
  "message": "User registered successfully",
  "access_token": "jwt_token_here",
  "user": {...}
}
```

#### POST /api/auth/login
Login an existing user.
```json
Request Body:
{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "jwt_token_here",
  "user": {...}
}
```

#### GET /api/auth/me
Get current user information (requires authentication).

### Book Endpoints

#### GET /api/books
Get all books with optional filters.
Query Parameters: `search`, `category`, `available_only`

#### GET /api/books/:id
Get a specific book by ID.

#### POST /api/books (Admin only)
Add a new book.

#### PUT /api/books/:id (Admin only)
Update a book.

#### DELETE /api/books/:id (Admin only)
Delete a book.

### Loan Endpoints

#### GET /api/loans
Get all loans (own loans for students, all loans for admin).

#### POST /api/loans
Borrow a book.
```json
Request Body:
{
  "book_id": 1
}
```

#### POST /api/loans/:id/return
Return a borrowed book.

### User Management Endpoints (Admin only)

#### GET /api/users
Get all users.

#### PUT /api/users/:id
Update user role.

### Statistics Endpoint (Admin only)

#### GET /api/stats
Get system statistics.

### Health Check

#### GET /health
Check system health status.

## Default Credentials

### Admin Account
- Email: `admin@library.com`
- Password: `admin123`
- Role: Administrator

You can use this account to:
- Access admin dashboard
- Manage books (add, edit, delete)
- Manage users and roles
- View system statistics

### Creating Student Accounts
Use the registration page to create new student accounts.

## CI/CD Strategy

### Overview
Although not implemented in this phase, the system is designed with CI/CD in mind following DevOps best practices.

### Proposed CI/CD Pipeline (using Jenkins)

1. **Source Control**
   - Git repository with main and development branches
   - Feature branches for new development
   - Pull request workflow for code review

2. **Continuous Integration**
   - Automated builds triggered on commits
   - Unit tests for backend APIs
   - Frontend component tests
   - Code quality checks (linting, formatting)

3. **Continuous Deployment**
   - Automated deployment to staging environment
   - Smoke tests on deployed application
   - Manual approval for production deployment
   - Rollback capability for failed deployments

4. **Pipeline Stages**
   ```
   Source → Build → Test → Package → Deploy → Verify
   ```

### Benefits
- Faster delivery of features
- Early bug detection
- Consistent build and deployment process
- Reduced manual errors
- Better collaboration

## Distributed Computing Approach

### Chosen Paradigm: Message Queue (RabbitMQ/Redis)

### Why Message Queue?
A message queue system is ideal for this library management application because:

1. **Asynchronous Processing**: Handle time-consuming tasks without blocking user requests
2. **Scalability**: Easy to scale individual components independently
3. **Reliability**: Messages are persisted until successfully processed
4. **Decoupling**: Frontend, backend, and services can evolve independently

### Potential Applications

1. **Email Notifications**
   - Queue: `email_notifications`
   - Publisher: Backend API
   - Consumer: Email service
   - Use cases: Overdue book reminders, reservation availability

2. **Book Reservation System**
   - Queue: `book_holds`
   - Publisher: Return book endpoint
   - Consumer: Notification service
   - Process: Notify next user when book becomes available

3. **Report Generation**
   - Queue: `report_jobs`
   - Publisher: Admin dashboard
   - Consumer: Report generator service
   - Use cases: Monthly statistics, user activity reports

4. **Search Indexing**
   - Queue: `search_index`
   - Publisher: Book management endpoints
   - Consumer: Search indexer
   - Purpose: Update search index when books are added/modified

### Architecture Diagram
```
                    ┌─────────────┐
                    │   Frontend  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Flask API  │
                    └──┬───────┬──┘
                       │       │
        ┌──────────────┘       └──────────────┐
        │                                     │
   ┌────▼────┐                        ┌──────▼──────┐
   │ SQLite  │                        │Message Queue│
   │   DB    │                        │(RabbitMQ)   │
   └─────────┘                        └──────┬──────┘
                                             │
                        ┌────────────────────┼────────────────┐
                        │                    │                │
                  ┌─────▼──────┐      ┌─────▼──────┐  ┌─────▼──────┐
                  │Email Worker│      │Report Worker│  │Index Worker│
                  └────────────┘      └────────────┘  └────────────┘
```

### Scalability Benefits
- Multiple worker instances can process queue messages in parallel
- Load balancing across workers
- Horizontal scaling based on queue depth
- Independent scaling of services

## Team Challenge Requirements

### Git Repository & Version Control ✓
- Initialized Git repository
- Main branch with all project files
- Clear commit history with meaningful messages
- .gitignore configured for Python and Node.js

### IDE Choice: VS Code
**Reasons for choosing VS Code:**
1. **Multi-language Support**: Excellent support for both Python and JavaScript/React
2. **Extensions**: Rich ecosystem (Python, ES7 React snippets, Prettier, ESLint)
3. **Integrated Terminal**: Easy to run both backend and frontend servers
4. **Git Integration**: Built-in Git commands and visual diff tools
5. **Free and Open Source**: Available for all team members
6. **Cross-platform**: Works on Windows, macOS, and Linux
7. **IntelliSense**: Smart code completion for both Python and JavaScript

### Distributed Computing Paradigm: Message Queue
As detailed in the [Distributed Computing Approach](#distributed-computing-approach) section above.

### CI/CD Description
As detailed in the [CI/CD Strategy](#cicd-strategy) section above.

## Database Schema

### Users Table
```sql
- id (INTEGER, Primary Key)
- email (TEXT, Unique)
- password (TEXT, Hashed)
- full_name (TEXT)
- role (TEXT: 'student' or 'admin')
- created_at (TIMESTAMP)
```

### Books Table
```sql
- id (INTEGER, Primary Key)
- isbn (TEXT, Unique)
- title (TEXT)
- author (TEXT)
- category (TEXT)
- total_copies (INTEGER)
- available_copies (INTEGER)
- description (TEXT)
- created_at (TIMESTAMP)
```

### Loans Table
```sql
- id (INTEGER, Primary Key)
- user_id (INTEGER, Foreign Key)
- book_id (INTEGER, Foreign Key)
- borrow_date (TIMESTAMP)
- due_date (TIMESTAMP)
- return_date (TIMESTAMP, nullable)
- status (TEXT: 'active' or 'returned')
```

### Holds Table
```sql
- id (INTEGER, Primary Key)
- user_id (INTEGER, Foreign Key)
- book_id (INTEGER, Foreign Key)
- hold_date (TIMESTAMP)
- status (TEXT: 'waiting' or 'notified')
```

## Security Features

1. **Password Hashing**: SHA-256 encryption for stored passwords
2. **JWT Authentication**: Secure token-based authentication
3. **Role-Based Access Control**: Different permissions for students and admins
4. **Input Validation**: Server-side validation for all inputs
5. **CORS Configuration**: Controlled cross-origin requests
6. **SQL Injection Protection**: Parameterized queries using SQLite

## Future Enhancements

1. **Email Notifications**: Send reminders for overdue books
2. **Book Reservations**: Hold system for unavailable books
3. **Fine Calculation**: Automatic late fee calculation
4. **Advanced Search**: Full-text search with filters
5. **Book Reviews**: User ratings and reviews
6. **Export Reports**: CSV/PDF export for admin reports
7. **Multi-library Support**: Support for multiple library branches
8. **Barcode Scanner**: Mobile app with barcode scanning
9. **Monitoring Dashboard**: Nagios integration for system health
10. **Jenkins Pipeline**: Automated CI/CD implementation

## Development Guidelines

### Backend Development
- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings for functions
- Handle errors gracefully with appropriate HTTP status codes
- Validate all inputs before processing

### Frontend Development
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful prop names
- Handle loading and error states
- Follow consistent naming conventions

### Git Workflow
1. Create feature branches from main
2. Make small, focused commits
3. Write clear commit messages
4. Create pull requests for code review
5. Merge to main after approval

## Troubleshooting

### Backend Issues

**Database not found:**
```bash
cd backend
python database.py
```

**Port 5000 already in use:**
Change the port in `backend/app.py`:
```python
app.run(debug=True, port=5001)
```

**Module not found:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Dependencies not installed:**
```bash
cd frontend
npm install
```

**Port 3000 already in use:**
Change the port in `frontend/vite.config.js`:
```javascript
server: {
  port: 3001,
  ...
}
```

**API connection error:**
Ensure backend is running on port 5000

## Testing

### Backend Testing
```bash
# Install pytest
pip install pytest

# Run tests (to be implemented)
pytest
```

### Frontend Testing
```bash
# Run tests (to be implemented)
npm test
```

### Manual Testing Checklist
- [ ] User registration with validation
- [ ] User login with correct/incorrect credentials
- [ ] Book search and filtering
- [ ] Book borrowing (available books only)
- [ ] Book return
- [ ] Admin: Add new book
- [ ] Admin: Edit book details
- [ ] Admin: Delete book
- [ ] Admin: Change user roles
- [ ] Admin: View statistics

## License

This project is developed for educational purposes as part of a software engineering course.

## Support

For questions or issues, please contact the team members or create an issue in the repository.

---

**Developed by Team: Sikai Han, Pritika Pritika, Jeremiah Agbebi, Jakaran Singh**

**Course**: Software Engineering

**Date**: 2024
