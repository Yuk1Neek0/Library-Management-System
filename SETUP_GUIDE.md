# Quick Setup Guide

This guide will help you get the Library Management System running on your machine in just a few steps.

## Prerequisites Check

Before starting, make sure you have these installed:

1. **Python 3.8+**
   ```bash
   python --version
   ```
   If not installed, download from: https://www.python.org/downloads/

2. **Node.js 16+**
   ```bash
   node --version
   npm --version
   ```
   If not installed, download from: https://nodejs.org/

3. **Git** (optional, for version control)
   ```bash
   git --version
   ```

## Step-by-Step Setup

### Option 1: Using Batch Files (Windows - Easiest)

1. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Start Backend Server**
   - Double-click `start-backend.bat`
   - Or run in terminal: `start-backend.bat`
   - Backend will run on http://localhost:5000

4. **Start Frontend Server** (in a new terminal)
   - Double-click `start-frontend.bat`
   - Or run in terminal: `start-frontend.bat`
   - Frontend will run on http://localhost:3000

5. **Access the Application**
   - Open your browser and go to: http://localhost:3000
   - Login with admin credentials:
     - Email: `admin@library.com`
     - Password: `admin123`

### Option 2: Manual Setup (All Platforms)

#### Backend Setup

1. Open terminal/command prompt
2. Navigate to backend folder:
   ```bash
   cd backend
   ```

3. (Optional) Create virtual environment:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize database:
   ```bash
   python database.py
   ```
   You should see:
   - "Default admin user created: admin@library.com / admin123"
   - "Added 5 sample books"
   - "Database initialized successfully!"

6. Start Flask server:
   ```bash
   python app.py
   ```
   Server should start on http://localhost:5000

#### Frontend Setup

1. Open a **new** terminal/command prompt
2. Navigate to frontend folder:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```
   This may take a few minutes.

4. Start development server:
   ```bash
   npm run dev
   ```
   Server should start on http://localhost:3000

#### Access the Application

1. Open your web browser
2. Go to: http://localhost:3000
3. You should see the login page

## First Login

### Admin Account (Full Access)
- **Email**: `admin@library.com`
- **Password**: `admin123`
- **Can do**: Everything (manage books, users, view stats)

### Create Student Account
1. Click "Register here" on login page
2. Fill in your details
3. Select "Student" as role
4. Click "Register"

## Testing the System

Once logged in, try these:

### As Admin:
1. ✓ View Dashboard with statistics
2. ✓ Browse Books - Search and filter books
3. ✓ Borrow a book
4. ✓ View "My Loans"
5. ✓ Return a book
6. ✓ Go to Admin Dashboard
7. ✓ Manage Books - Add/Edit/Delete books
8. ✓ Manage Users - Change user roles

### As Student:
1. ✓ View Dashboard
2. ✓ Browse and search books
3. ✓ Borrow available books
4. ✓ View active loans and history
5. ✓ Return borrowed books

## Troubleshooting

### "Module not found" error (Backend)
```bash
cd backend
pip install -r requirements.txt
```

### "Cannot find module" error (Frontend)
```bash
cd frontend
npm install
```

### Port already in use

**Backend (Port 5000):**
1. Open `backend/app.py`
2. Change last line to:
   ```python
   app.run(debug=True, port=5001)
   ```
3. Update `frontend/vite.config.js` proxy target to `http://localhost:5001`

**Frontend (Port 3000):**
1. Open `frontend/vite.config.js`
2. Change port:
   ```javascript
   server: {
     port: 3001,
     ...
   }
   ```

### Database errors
Delete `backend/library.db` and run:
```bash
cd backend
python database.py
```

### API connection errors
1. Make sure backend is running (http://localhost:5000)
2. Check browser console for error details
3. Verify CORS is enabled in backend

### Can't see changes after editing code

**Backend**: Restart the Flask server (Ctrl+C, then run again)
**Frontend**: Vite auto-reloads, but if not working, restart with Ctrl+C and `npm run dev`

## Project Structure Overview

```
Library System/
│
├── backend/               # Flask API server
│   ├── app.py            # Main application
│   ├── database.py       # Database setup
│   ├── config.py         # Configuration
│   └── library.db        # SQLite database (auto-created)
│
├── frontend/             # React application
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── components/  # Reusable components
│   │   └── services/    # API calls
│   └── package.json
│
├── README.md            # Full documentation
├── SETUP_GUIDE.md      # This file
└── start-*.bat         # Quick start scripts
```

## Next Steps

1. Read the full [README.md](README.md) for:
   - Complete API documentation
   - Database schema details
   - Development guidelines
   - CI/CD and distributed computing strategies

2. Explore the codebase:
   - Backend API endpoints in `backend/app.py`
   - Frontend pages in `frontend/src/pages/`
   - Database schema in `backend/database.py`

3. Try implementing new features:
   - Add book categories
   - Implement search filters
   - Add user profile pages
   - Create reports

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review error messages in terminal/console
- Check browser Developer Tools (F12) for frontend errors
- Ensure both backend and frontend servers are running

## Sample Data

The system comes with:
- 1 Admin user: `admin@library.com` / `admin123`
- 5 Sample books in the Programming category
- All books initially available for borrowing

You can add more books through the Admin interface!

---

**Happy Coding!** 🎉

If everything is working, you should be able to browse books, borrow them, and manage the library system.
