# Quick Start Guide for Chemical Visualizer Desktop

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Backend**: Django server running on `http://localhost:8000`

## Windows Users

### Step 1: Open Command Prompt
Navigate to the project folder:
```cmd
cd C:\Users\Surjeet Kumar\chemical_visualizer\hybrid_desktop_visualizer
```

### Step 2: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 3: Start the Django Backend
Open a **new** Command Prompt window and run:
```cmd
cd C:\Users\Surjeet Kumar\chemical_visualizer
python manage.py runserver
```
Wait for the message: "Starting development server at http://127.0.0.1:8000/"

### Step 4: Test Backend Connection (Optional)
In the desktop app folder, run:
```cmd
python test_backend.py
```

### Step 5: Run the Desktop Application
```cmd
python main.py
```

Or use the batch script:
```cmd
run_desktop.bat
```

## macOS/Linux Users

### Step 1: Open Terminal
Navigate to the project:
```bash
cd ~/chemical_visualizer/hybrid_desktop_visualizer
```

### Step 2: Create and Activate Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start Django Backend
Open a **new** terminal and run:
```bash
cd ~/chemical_visualizer
python manage.py runserver
```

### Step 5: Test Connection (Optional)
```bash
python test_backend.py
```

### Step 6: Run Desktop Application
```bash
python main.py
```

## Quick Test with Sample Data

1. Start the application
2. **Register** with test credentials:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`

3. **Login** with the credentials above

4. **Upload Sample CSV**:
   - Click "Select File"
   - Choose `sample_equipment_data.csv`
   - Click "Upload"

5. **View Analysis**:
   - Click "Analyze" to see charts
   - Click "Table" to see statistics
   - Click "Overall Summary" for aggregated data

## Troubleshooting

### Backend Connection Error
```
Error: Connection error: Backend server not running
```
**Solution**: 
- Make sure Django is running in a separate terminal
- Check URL: http://localhost:8000
- Verify no firewall is blocking port 8000

### Module Not Found Errors
```
ModuleNotFoundError: No module named 'PyQt5'
```
**Solution**:
- Run: `pip install -r requirements.txt`
- Ensure you're using the correct Python (check with `python --version`)

### CSV Upload Fails
```
Error: Failed to process CSV: ...
```
**Solution**:
- Verify CSV has columns: Equipment, Type, Flowrate, Pressure, Temperature
- Check file is not corrupted
- Ensure proper UTF-8 encoding

### Authentication Issues
**Solution**:
- Try registering with new username
- Clear any cached tokens
- Check backend logs for errors

## Features Overview

### Authentication ✓
- Register new account
- Secure login with JWT tokens
- Session management

### CSV Upload ✓
- Upload equipment data
- Automatic validation
- Data storage (last 5 datasets)

### Data Analysis ✓
- View summary statistics
- Pie chart: Equipment type distribution
- Bar chart: Average metrics
- Data table view

### PDF Export ✓
- Generate professional reports
- Includes all statistics and charts
- Save to any location

### History ✓
- Last 5 uploads stored
- Per-user data isolation
- Quick dataset access
- Delete old datasets

## API Endpoints

All API calls are made to `http://localhost:8000/api`:

- `POST /accounts/register/` - Register new user
- `POST /accounts/login/` - Login user
- `POST /equipment/upload/` - Upload CSV
- `GET /equipment/datasets/` - List datasets
- `GET /equipment/summary/` - Get aggregated summary
- `GET /equipment/datasets/{id}/` - Get dataset details
- `DELETE /equipment/datasets/{id}/` - Delete dataset
- `GET /equipment/datasets/{id}/export-pdf/` - Export PDF

## Next Steps

1. **Explore the Dashboard**: Familiarize yourself with all features
2. **Upload Your Data**: Use CSV format with required columns
3. **Generate Reports**: Export analysis as PDF
4. **Manage History**: Keep track of last 5 uploads

## Support

For issues, check:
- README_DESKTOP.md - Detailed documentation
- test_backend.py - Verify backend connectivity
- Django logs - Backend errors
- Application logs - Desktop app errors

## Additional Resources

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Matplotlib Visualization](https://matplotlib.org/)

Enjoy using Chemical Visualizer!


### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Ensure Django Backend is Running
In a separate terminal:
```bash
cd ~/chemical_visualizer
python manage.py runserver
```

### Step 6: Run the Application
```bash
python main.py
```

## Features Overview

1. **Authentication Panel**
   - Register new account or login
   - Secure JWT-based authentication

2. **Dashboard**
   - View all uploaded datasets
   - Upload new CSV files
   - Manage datasets

3. **Analysis View**
   - Type distribution pie chart
   - Average metrics bar chart
   - Export to PDF

4. **Data Table**
   - View all statistics
   - Equipment breakdown
   - Detailed metrics

## Common Issues & Solutions

### "ModuleNotFoundError: No module named 'PyQt5'"
```bash
pip install PyQt5
```

### "Connection refused" error
Make sure Django backend is running on http://localhost:8000

### "API request failed"
Check that the backend is accessible and you're connected to the internet

## CSV Upload Format

Your CSV file must have these columns:
- Equipment
- Type  
- Flowrate
- Pressure
- Temperature

## Support

For more details, see README.md in this folder.
