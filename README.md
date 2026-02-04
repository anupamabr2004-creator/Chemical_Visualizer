# Chemical Visualizer - Complete Setup Guide

## Overview
Chemical Visualizer is a Django-based hybrid application that allows users to:
- Register and authenticate with JWT tokens
- Upload CSV files containing equipment data
- Analyze data with interactive dashboards
- View history of last 5 uploaded datasets
- Export analysis results as PDF documents

## Features 

### 1. **Authentication System**
- User Registration with password hashing
- User Login with JWT token generation
- Persistent login using JWT tokens
- Session management
  <img width="1920" height="913" alt="image" src="https://github.com/user-attachments/assets/a73c296a-9fb0-44e5-ab9e-bbde8752fc22" />


### 2. **Dataset Management**
-  CSV upload with validation
-  User-specific dataset storage (each user only sees their own datasets)
-  Last 5 uploaded datasets kept per user (automatic cleanup of older ones)
-  Dataset metadata storage (flowrate, pressure, temperature, equipment count)
  <img width="1920" height="912" alt="image" src="https://github.com/user-attachments/assets/6dd9a823-6747-4783-98dc-839dfdaa1b47" />




### 3. **Data Analysis**
-  Real-time dataset analysis
-  Statistical calculations (averages, distributions)
-  Equipment type distribution breakdown
-  Interactive dropdown to select datasets for analysis
<img width="1920" height="787" alt="image" src="https://github.com/user-attachments/assets/b5cd6ee0-f8b7-4a19-9275-9a842d01c012" />
 <img width="1920" height="909" alt="image" src="https://github.com/user-attachments/assets/7b3223ae-d18e-4a55-8ac5-b4ae11928953" />




### 4. **PDF Export**
-  Generate professional PDF reports
-  Include all analysis metrics
-  Export equipment distribution charts
-  Formatted tables with styling
  <img width="1920" height="789" alt="image" src="https://github.com/user-attachments/assets/8258b8de-97d8-44ae-8eb0-567060d3e2e2" />


### 5. **Frontend UI**
-  Responsive design (mobile & desktop)
-  Clean, modern interface
-  Real-time form validation
-  Error and success messages
-  Loading indicators

## Installation & Setup 

Backend

### Prerequisites
- Python 3.8+
- pip
- Virtual Environment (recommended)

### Step 1: Clone and Setup Environment
First, clone the repository to your local machine.
```bash
cd chemical_visualizer
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
# Or manually install:
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers pandas reportlab
```

### Step 3: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 5: Start the Server
```bash
python manage.py runserver
```

The server will run at: **http://localhost:8000**

***Frontend (React.js)-***
```bash
cd chemical_visualizer
cd chemical-frontend
npm install
npm start
```

Web app runs at:
    http://localhost:3000

***Frontend ( Pyqt5)-***
```bash
cd chemical_visualizer
cd hybrid_desktop_visualizer
pip install -r requirements.txt
python main.py
```
<img width="1920" height="1016" alt="image" src="https://github.com/user-attachments/assets/154f7bb3-44be-4ec5-9c95-9acab8d3c20c" />



## API Endpoints

### Authentication
- **POST** `/api/auth/register/` - Register new user
  ```json
  {"username": "john", "password": "pass123"}
  ```

- **POST** `/api/auth/login/` - Login user
  ```json
  {"username": "john", "password": "pass123"}
  ```
  Returns: `{"access": "token...", "refresh": "token...", "username": "john"}`

### Equipment/Datasets
- **GET** `/api/equipment/datasets/` - Get user's datasets (last 5)
  - Header: `Authorization: Bearer {access_token}`

- **POST** `/api/equipment/upload/` - Upload CSV file
  - Header: `Authorization: Bearer {access_token}`
  - Body: multipart/form-data with file

- **GET** `/api/equipment/datasets/{id}/export-pdf/` - Download dataset PDF
  - Header: `Authorization: Bearer {access_token}`

## CSV File Format

Your CSV file should have these columns:
```csv
Equipment,Type,Flowrate,Pressure,Temperature
Pump-001,Centrifugal,150.5,2.5,45.2
Valve-001,Ball,0.0,2.5,46.3
...
```

**Required columns:**
- `Equipment - numeric
- `Flowrate` - numeric (L/min)
- `Pressure` - numeric (bar)
- `Temperature` - numeric (°C)
- `Type` - text (equipment type)

For example,
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/525df956-835c-46a8-bd7e-689769e77832" />


## Frontend Usage

### 1. Open the Application
Open `index.html` in your web browser (or serve it from a local server)

### 2. Register
- Click "Register"
- Enter username and password
- Click "Register" button
- You'll be redirected to login

### 3. Login
- Enter your credentials
- Click "Login"
- You'll see the dashboard

### 4. Upload CSV
- Click " Upload CSV"
- Select a CSV file matching the format
- Click "Upload" button
- File will be processed and added to your datasets

### 5. Analyze Dataset
- Select a dataset from the dropdown or click "Analyze" button
- See statistics: Total Equipment, Average Flowrate, Pressure, Temperature
- View equipment type distribution

### 6. Export to PDF
- After analyzing a dataset, click " Export as PDF"
- PDF will download with all analysis results



## Key Features Explained

### User Isolation
- Each user only sees their own datasets
- Datasets are linked to the user who uploaded them
- Old datasets are automatically cleaned up (keeping only last 5)

### JWT Authentication
- Secure token-based authentication
- Tokens valid for 60 minutes (access token)
- Refresh tokens for extended sessions
- No sessions stored on server

### PDF Generation
- Uses ReportLab library
- Creates professional, formatted reports
- Includes all analysis metrics
- Styled tables and sections

### Data Analysis
- Calculates mean (average) for numerical columns
- Creates distribution breakdown for equipment types
- Validates CSV format and content

## Troubleshooting

### "CORS Error"
- Ensure `CORS_ALLOWED_ORIGINS` in settings.py includes your frontend URL
- Update ALLOWED_HOSTS if needed

### "File Upload Failed"
- Verify CSV format matches required columns
- Check file size isn't too large
- Ensure all numeric columns have valid numbers

### "Login Not Working"
- Check that JWT is properly installed: `pip install djangorestframework-simplejwt`
- Verify token is being sent in Authorization header
- Check token hasn't expired

### "PDF Download Issues"
- Ensure ReportLab is installed: `pip install reportlab`
- Verify dataset exists and belongs to user
- Check browser allows file downloads

## Database Models

### User (from Django)
```python
- username (unique)
- password (hashed)
- first_name, last_name, email
```

### Dataset
```python
- id (auto)
- user (ForeignKey to User)
- filename (str)
- uploaded_at (datetime, auto)
- total_equipment (int)
- average_flowrate (float)
- average_pressure (float)
- average_temperature (float)
- type_distribution (JSON)
```

## Configuration

### settings.py Key Settings
```python
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['*']  # Restrict in production
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]  # Add frontend URL
SECRET_KEY = '...'  # Change in production
```

### JWT Configuration
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

## Environment Setup (Optional)

Create a `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Then update settings.py to use environment variables.



## Support

If you encounter any issues:
1. Check Django logs in terminal
2. Verify all dependencies are installed
3. Clear browser cache and localStorage
4. Ensure CSV file format is correct
5. Check database migrations are applied

## Version Info
- Django: 5.2.10
- Django REST Framework: Latest
- Simple JWT: Latest
- ReportLab: 4.0+
- Pandas: Latest
- Python: 3.8+
