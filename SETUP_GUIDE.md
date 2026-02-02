# Chemical Visualizer - Setup & Troubleshooting Guide

## Quick Start (Make Login Page Appear)

### Step 1: Start the Django Backend
```bash
cd c:\Users\Surjeet Kumar\chemical_visualizer

# Activate virtual environment
venv\Scripts\activate

# Apply migrations
python manage.py migrate

# Start server on port 8000
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Open Frontend
**Important:** Do NOT open index.html with `file://` protocol!

Instead, use one of these methods:

#### Option A: Open via Django (Recommended for Development)
```
http://localhost:8000/
```
or
```
http://127.0.0.1:8000/
```

#### Option B: Serve from Local Web Server
```bash
# Using Python built-in server in the project root
python -m http.server 8080
```
Then visit: `http://localhost:8080/index.html`

#### Option C: Use VS Code Live Server Extension
- Right-click index.html → "Open with Live Server"

### Step 3: Test Login
1. You should see the login page with:
   - "⚗️ Chemical Visualizer" heading
   - Username field
   - Password field
   - Login button

2. Click "Register" to create an account
3. Then login with your credentials

---

## What Was Fixed

### Fix #1: CORS Middleware Position
**File:** `chemical_visualizer/settings.py`

**Problem:** CorsMiddleware was last in the middleware list, causing CORS headers not to be properly set.

**Solution:** Moved CorsMiddleware to the first position (right after SecurityMiddleware).

**Verification:**
```bash
# Test CORS headers
curl -i -X OPTIONS http://127.0.0.1:8000/api/auth/login/ \
  -H "Origin: http://localhost:3000"
```

Look for `Access-Control-Allow-Origin: http://localhost:3000` in response headers.

---

### Fix #2: PDF Export Authorization
**File:** `index.html`

**Problem:** PDF export used `window.location.href` which doesn't send Authorization header, causing authentication failure.

**Solution:** Changed to use `fetch()` with blob response, which properly sends the Bearer token.

**Testing:**
1. Login to the application
2. Upload a CSV file
3. Select dataset and click "Analyze"
4. Click "Export as PDF" button
5. PDF should download successfully

---

### Fix #3: Better Error Messages
**File:** `index.html`

**Problem:** Network errors showed vague messages like "Error: " with no context.

**Solution:** Added helpful error messages indicating "Make sure backend is running on http://localhost:8000"

**Testing:**
1. Stop the Django server
2. Try to login
3. Should see: `Error: [error]. Make sure backend is running on http://localhost:8000`

---

## Verification Checklist

- [ ] Django server running on port 8000
- [ ] Frontend accessed via http (not file://)
- [ ] Browser console (F12) shows no errors
- [ ] Network tab shows successful API responses
- [ ] Login page displays correctly
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Dashboard shows after login
- [ ] Can upload CSV file
- [ ] Can view uploaded datasets
- [ ] Can analyze datasets
- [ ] Can export PDF

---

## Common Issues & Solutions

### Issue 1: "Cannot GET /api/auth/login/"
**Cause:** Backend not running or wrong URL
**Solution:**
1. Ensure Django server is running: `python manage.py runserver`
2. Check that you're using `http://localhost:8000/` not `file://`

### Issue 2: "CORS Error: Request has been blocked by CORS policy"
**Cause:** CORS headers not being sent
**Solution:**
1. Check CORS middleware is first in MIDDLEWARE list
2. Verify CORS_ALLOWED_ORIGINS includes your frontend URL
3. Clear browser cache and reload

### Issue 3: Login button doesn't respond
**Cause:** JavaScript errors or fetch API failure
**Solution:**
1. Open Browser Console (F12)
2. Look for JavaScript errors
3. Check Network tab for failed requests
4. Try reloading page

### Issue 4: Login succeeds but dashboard doesn't appear
**Cause:** Token not stored properly or loadDatasets failing
**Solution:**
1. Check browser LocalStorage: Open DevTools → Application → LocalStorage
2. Should see `authToken` and `username` keys
3. If missing, registration/login failed

### Issue 5: File upload fails
**Cause:** CSV format wrong or backend not accepting file
**Solution:**
1. Verify CSV has these columns: Equipment, Type, Flowrate, Pressure, Temperature
2. Ensure numbers don't have quotes around them
3. Check backend logs for error details

### Issue 6: PDF export fails
**Cause:** Authorization not being sent or ReportLab not installed
**Solution:**
```bash
# Install ReportLab
pip install reportlab

# Restart Django server
python manage.py runserver
```

---

## Testing with Curl

### Test Registration
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

Expected response:
```json
{"message": "Registration successful"}
```

### Test Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

Expected response:
```json
{
  "message": "Login successful",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "username": "testuser"
}
```

### Test CORS
```bash
curl -i -X OPTIONS http://127.0.0.1:8000/api/auth/login/ \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```

Look for:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
```

---

## Browser Developer Tools Debugging

### Network Tab
1. Open DevTools (F12)
2. Click Network tab
3. Perform login action
4. Click on the `/api/auth/login/` request
5. Check:
   - **Status:** Should be 200
   - **Headers:** Look for Access-Control-Allow-Origin
   - **Response:** Should show access token

### Console Tab
- Check for JavaScript errors (red text)
- Look for CORS errors (yellow warnings)
- Type `localStorage` to check stored tokens

### Application Tab
- LocalStorage should contain:
  - `authToken`: Your JWT access token
  - `username`: Your username

---

## Important Note About chemical-frontend

The original request mentioned checking a `chemical-frontend` folder. This folder **does not exist** in the current workspace. 

If you have a separate React/Vue/Angular frontend project:
1. Copy it to the workspace
2. Update API endpoint URLs to match Django backend
3. Ensure CORS_ALLOWED_ORIGINS includes its serving URL
4. Run it on a different port (e.g., 3000, 3001)

For now, the single `index.html` file serves as the frontend.

---

## Production Deployment Notes

Before deploying to production:

1. **CORS Configuration**
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://yourdomain.com",
       "https://www.yourdomain.com",
   ]
   ```

2. **Security Settings**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   SECRET_KEY = 'your-secure-random-key'
   ```

3. **HTTPS Enforcement**
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

4. **Database Migration to PostgreSQL**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'chemical_visualizer',
           'USER': 'postgres',
           'PASSWORD': 'your-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

---

## Summary of Changes Made

| File | Change | Impact |
|------|--------|--------|
| `settings.py` | Moved CorsMiddleware to first position | CORS headers now properly set |
| `index.html` | Changed PDF export to use fetch API | PDF export now sends authorization header |
| `index.html` | Added better error messages | Users see helpful debug info |
| `index.html` | Added console logging | Easier debugging via DevTools |

All changes are **backward compatible** and improve the application without breaking existing functionality.

