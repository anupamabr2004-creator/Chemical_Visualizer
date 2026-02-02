# How to Run Chemical Visualizer (Frontend + Backend)

## Quick Start (Recommended)

### Terminal 1 - Backend
```bash
cd c:\Users\Surjeet Kumar\chemical_visualizer
venv\Scripts\activate
python manage.py runserver
```

### Terminal 2 - Frontend
```bash
cd c:\Users\Surjeet Kumar\chemical_visualizer\chemical-frontend
npm install  # First time only
npm start
```

### Browser
Open: **http://localhost:3000**

---

## File Structure

```
chemical_visualizer/
├── chemical-frontend/          ← React Frontend
│   ├── package.json
│   ├── .env                    (API_URL=http://localhost:8000/api)
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       ├── index.js
│       └── components/
│           ├── AuthPage.js     (Login/Register)
│           └── Dashboard.js    (Main App)
│
├── accounts/                   ← Django Auth App
│   ├── views.py               (login, register)
│   └── urls.py
│
├── equipment/                  ← Django Equipment App
│   ├── views.py               (upload, analysis, PDF)
│   └── urls.py
│
├── chemical_visualizer/        ← Django Config
│   └── settings.py            (CORS, JWT, etc)
│
├── start_backend.bat          ← Quick start backend
├── start_frontend.bat         ← Quick start frontend
├── start_all.sh              ← Start both (Linux/Mac)
├── manage.py
└── db.sqlite3                 (Database)
```

---

## Configuration

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
BROWSER=none
```

### Backend (settings.py)
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React Frontend
    "http://127.0.0.1:3000",
]
```

---

## Ports

- **Frontend (React):** http://localhost:3000
- **Backend (Django):** http://localhost:8000
- **API Endpoints:** http://localhost:8000/api

---

## Common Issues

### "Cannot connect to backend"
- Make sure backend is running on port 8000
- Check CORS_ALLOWED_ORIGINS includes http://localhost:3000

### "npm start fails"
- Make sure Node.js is installed: `node --version`
- Clear cache: `npm cache clean --force`
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

### "Port 3000/8000 already in use"
Change ports in:
- Backend: `python manage.py runserver 8001`
- Frontend: `PORT=3001 npm start`
- Update frontend .env with new backend URL

---

## API Integration

The React frontend communicates with Django backend via:
- **Base URL:** http://localhost:8000/api
- **Authentication:** JWT tokens in localStorage
- **Headers:** Authorization: Bearer {token}

Endpoints:
- `POST /auth/register/` - Register new user
- `POST /auth/login/` - Login user
- `GET /equipment/datasets/` - Get user's datasets
- `POST /equipment/upload/` - Upload CSV
- `GET /equipment/datasets/{id}/export-pdf/` - Export PDF

---

## Next Steps

1. Start Backend: `python manage.py runserver`
2. Start Frontend: `npm start` (in chemical-frontend)
3. Open http://localhost:3000 in browser
4. Register and login
5. Upload sample_data.csv
6. Analyze and export!

