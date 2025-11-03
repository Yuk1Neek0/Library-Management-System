# Troubleshooting Guide

## Issue: Getting 422 or 401 Errors on API Calls

### Symptoms
- Frontend shows errors like "422 UNPROCESSABLE ENTITY"
- Can't fetch books, loans, or stats
- API calls fail after login

### Solution Steps

#### Step 1: Restart the Backend Server

The backend code has been updated with JWT error handlers and CORS fixes. You need to restart it:

1. **Stop the current backend server**:
   - Press `Ctrl+C` in the terminal running the backend

2. **Start it again**:
   ```bash
   cd backend
   python app.py
   ```

3. **You should see**:
   ```
   Default admin user created: admin@library.com / admin123
   Added 5 sample books
   Database initialized successfully!
    * Serving Flask app 'app'
    * Debug mode: on
    * Running on http://127.0.0.1:5000
   ```

#### Step 2: Clear Browser Storage and Reload

1. **Open Browser Developer Tools** (F12)
2. **Go to Application tab** (Chrome) or Storage tab (Firefox)
3. **Clear Local Storage**:
   - Find `localhost:3000` in the left sidebar
   - Right-click on Local Storage → Clear
4. **Reload the page** (Ctrl+R or F5)

#### Step 3: Login Again

1. Go to http://localhost:3000
2. Login with:
   - Email: `admin@library.com`
   - Password: `admin123`
3. You should now be able to access all features!

---

## What Was Fixed

### Backend Updates ([app.py](backend/app.py)):

1. **Added JWT Error Handlers**:
   ```python
   @jwt.expired_token_loader
   @jwt.invalid_token_loader
   @jwt.unauthorized_loader
   ```
   These properly handle JWT authentication errors.

2. **Updated CORS Configuration**:
   ```python
   CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
   ```
   Allows cross-origin requests from the frontend.

### Config Updates ([config.py](backend/config.py)):

3. **Added JWT Configuration**:
   ```python
   JWT_TOKEN_LOCATION = ['headers']
   JWT_HEADER_NAME = 'Authorization'
   JWT_HEADER_TYPE = 'Bearer'
   JWT_COOKIE_CSRF_PROTECT = False
   ```
   Configures JWT to work with Bearer tokens in headers.

---

## Testing the Fix

### Quick Test Commands

**Test 1: Health Check** (should work without auth):
```bash
curl http://localhost:5000/health
```
Expected: `{"status": "healthy", ...}`

**Test 2: Login**:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"admin@library.com","password":"admin123"}' \
  http://localhost:5000/api/auth/login
```
Expected: JSON with `access_token` and `user` data

**Test 3: Get Books** (after getting token from Test 2):
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:5000/api/books
```
Expected: Array of books

---

## Common Issues and Solutions

### Issue: "Module not found" errors

**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "Port already in use"

**Solution for Backend (port 5000)**:
1. Find the process:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F

   # Mac/Linux
   lsof -i :5000
   kill -9 <PID>
   ```

2. Or change the port in `backend/app.py`:
   ```python
   app.run(debug=True, port=5001)
   ```
   Don't forget to update `frontend/vite.config.js` proxy target!

**Solution for Frontend (port 3000)**:
1. Change in `frontend/vite.config.js`:
   ```javascript
   server: {
     port: 3001,
     ...
   }
   ```

### Issue: Database errors

**Solution**:
```bash
cd backend
# Delete the old database
rm library.db  # or del library.db on Windows

# Reinitialize
python database.py
```

### Issue: CORS errors in browser console

**Solution**: Make sure backend is running and CORS is configured (already fixed in the updates above). Restart backend.

### Issue: Can't login / Invalid credentials

**Default credentials**:
- Email: `admin@library.com`
- Password: `admin123`

Make sure you're using the exact email and password.

### Issue: Frontend shows blank page

**Solution**:
1. Check browser console (F12) for errors
2. Make sure both servers are running:
   - Backend: http://localhost:5000
   - Frontend: http://localhost:3000
3. Try accessing backend directly: http://localhost:5000/health

---

## Complete Reset (Nuclear Option)

If nothing else works:

### Backend:
```bash
cd backend

# Remove database
rm library.db  # or del library.db on Windows

# Reinstall dependencies
pip install -r requirements.txt

# Reinitialize database
python database.py

# Start server
python app.py
```

### Frontend:
```bash
cd frontend

# Reinstall dependencies
rm -rf node_modules  # or rmdir /s node_modules on Windows
npm install

# Start server
npm run dev
```

### Browser:
1. Clear all site data (F12 → Application → Clear site data)
2. Clear cache (Ctrl+Shift+Delete)
3. Close and reopen browser
4. Go to http://localhost:3000

---

## Verifying Everything Works

After restart, test this flow:

1. ✓ Backend health check: http://localhost:5000/health
2. ✓ Frontend loads: http://localhost:3000
3. ✓ Login page appears
4. ✓ Login with admin@library.com / admin123
5. ✓ Dashboard shows (with stats if admin)
6. ✓ Books page loads with book list
7. ✓ Can search and filter books
8. ✓ Can borrow a book
9. ✓ My Loans shows the borrowed book
10. ✓ Can return the book
11. ✓ Admin pages work (if logged in as admin)

---

## Still Having Issues?

### Check Backend Logs

Look at the terminal where backend is running. You should see:
```
127.0.0.1 - - [timestamp] "GET /api/books HTTP/1.1" 200 -
```

If you see 422, 401, 500, or other error codes, that's the issue.

### Check Frontend Console

Press F12 in browser, look at Console tab for JavaScript errors.

### Check Network Tab

1. Press F12
2. Go to Network tab
3. Refresh the page
4. Click on failed requests (red)
5. Check Response tab to see actual error message

### Check Token in Browser

1. F12 → Application → Local Storage → localhost:3000
2. Check if `token` and `user` keys exist
3. If missing, login again

---

## Contact for Help

If you're still stuck:
1. Check the backend terminal for specific error messages
2. Check the browser console (F12) for frontend errors
3. Verify both servers are running on correct ports
4. Make sure you restarted backend after the code changes

## System Information for Bug Reports

When reporting issues, include:
- Operating System: Windows/Mac/Linux
- Python version: `python --version`
- Node version: `node --version`
- Browser: Chrome/Firefox/Safari/Edge
- Error messages from both backend and frontend
- Screenshots of error (if applicable)

---

**Most Common Fix**: Restart backend server after code changes!
