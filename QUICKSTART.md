# Quick Start - Library Management System

## 🚀 Get Started in 5 Minutes!

### Step 1: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 2: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
python database.py  # Initialize database (first time only)
python app.py       # Start backend server
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev         # Start frontend server
```

### Step 3: Access the Application

Open browser: **http://localhost:3000**

Login with:
- **Email**: `admin@library.com`
- **Password**: `admin123`

---

## 📋 What You Can Do

### As Admin:
✓ View system statistics
✓ Browse and search books
✓ Borrow and return books
✓ Add/Edit/Delete books
✓ Manage user roles

### As Student:
✓ Browse books
✓ Search and filter
✓ Borrow books
✓ View loan history
✓ Return books

---

## 🎯 Quick Test Checklist

- [ ] Login with admin credentials
- [ ] View Dashboard
- [ ] Browse Books page
- [ ] Search for "Python"
- [ ] Borrow a book
- [ ] Go to "My Loans"
- [ ] Return the book
- [ ] Go to Admin Dashboard
- [ ] Add a new book
- [ ] View Manage Users

---

## 🆘 Quick Troubleshooting

**Backend won't start?**
```bash
pip install -r requirements.txt
```

**Frontend won't start?**
```bash
npm install
```

**Database errors?**
```bash
cd backend
python database.py
```

**Can't login?**
- Email: `admin@library.com`
- Password: `admin123`
- Make sure backend is running!

---

## 📁 Project Files Overview

```
📦 Library System
├── 📄 README.md              ← Full documentation
├── 📄 SETUP_GUIDE.md         ← Detailed setup
├── 📄 PROJECT_SUMMARY.md     ← Technical overview
├── 📄 QUICKSTART.md          ← This file!
│
├── 📁 backend/               ← Flask API
│   ├── app.py               ← Main API server
│   ├── database.py          ← DB initialization
│   └── requirements.txt     ← Python packages
│
└── 📁 frontend/              ← React App
    ├── src/
    │   ├── pages/           ← UI pages
    │   ├── components/      ← Reusable UI
    │   └── services/        ← API calls
    └── package.json         ← Node packages
```

---

## 💡 Useful Commands

**Backend:**
```bash
python app.py              # Start server
python database.py         # Reset database
```

**Frontend:**
```bash
npm run dev               # Development server
npm run build             # Production build
npm run preview           # Preview build
```

**Git:**
```bash
git status               # Check status
git log --oneline        # View commits
git add .                # Stage changes
git commit -m "message"  # Commit changes
```

---

## 🔗 Important URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Docs**: See README.md

---

## 📚 Sample Data Included

**Default Admin:**
- Email: `admin@library.com`
- Password: `admin123`

**Sample Books:**
- Clean Code
- Design Patterns
- Clean Architecture
- The Pragmatic Programmer
- Python Crash Course

All books are initially available for borrowing!

---

## 🎓 Learning Resources

For more details, see:
- **[README.md](README.md)** - Complete documentation
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation help
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture details

---

**Ready to go? Start with Step 1 above!** 🚀
