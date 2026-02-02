# Hybrid Desktop Visualizer - PyQt5 Application

A desktop application for chemical equipment visualization using PyQt5 and matplotlib, powered by the Django backend.

## Features

- **Authentication**: Login and registration with JWT tokens
- **Dataset Management**: Upload, view, and manage CSV datasets
- **Data Analysis**: Interactive charts and statistics
  - Equipment type distribution (pie chart)
  - Average metrics visualization (bar chart)
- **Data Table**: View detailed equipment data
- **PDF Export**: Generate and download analysis reports
- **Light Theme UI**: Professional and elegant user interface

## Prerequisites

- Python 3.8+
- Django backend running on `http://localhost:8000/api`
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project**:
   ```bash
   cd hybrid_desktop_visualizer
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Make sure the Django backend is running on `http://localhost:8000`, then:

```bash
python main.py
```

## Project Structure

```
hybrid_desktop_visualizer/
├── main.py                 # Application entry point
├── api_client.py          # API communication with Django backend
├── auth_window.py         # Login and registration UI
├── dashboard_window.py    # Main dashboard with analysis
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## API Endpoints Used

The application communicates with the following Django API endpoints:

- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `GET /equipment/datasets/` - List all datasets
- `GET /equipment/datasets/{id}/` - Get dataset details
- `POST /equipment/upload/` - Upload CSV file
- `DELETE /equipment/datasets/{id}/` - Delete dataset

## Usage

### First Time Setup

1. Click "Sign Up" to create a new account
2. Fill in username, email, and password
3. Click "Create Account"

### Login

1. Enter your username and password
2. Click "Login"

### Upload Dataset

1. Click "Select File" to choose a CSV file
2. Click "Upload" to upload
3. Your datasets will appear in the table

### View Analysis

1. Click "Analyze" next to a dataset
2. View pie chart and bar charts
3. Click "Export as PDF" to generate a report

### View Data Table

1. Click "Table" next to a dataset
2. View detailed statistics and equipment breakdown

## CSV File Format

Your CSV files should contain the following columns:

- **Equipment**: Equipment name/identifier
- **Type**: Type of equipment
- **Flowrate**: Flow rate in L/min
- **Pressure**: Pressure in bar
- **Temperature**: Temperature in °C

Example:

```csv
Equipment,Type,Flowrate,Pressure,Temperature
Pump-01,Centrifugal,50.5,3.2,45.2
Pump-02,Reciprocating,35.2,4.1,48.5
Compressor-01,Screw,120.0,6.5,52.3
```

## Keyboard Shortcuts

- `Ctrl+Q` - Quit application

## Troubleshooting

### Connection Error to Backend

Ensure the Django backend is running:
```bash
cd ../chemical_visualizer
python manage.py runserver
```

### Import Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### FileNotFoundError for CSV

Ensure the CSV file path is correct and the file exists.

## License

This project is part of the Chemical Visualizer suite.

## Support

For issues or questions, refer to the main project documentation or contact support.
