# Chemical Visualizer - Desktop Application

A PyQt5-based desktop application for managing and analyzing chemical equipment data, seamlessly integrated with the Django backend API.

## Features

### 1. **Authentication**
- User registration with email
- Secure JWT token-based authentication
- Login/logout functionality
- Session management

### 2. **CSV Upload**
- Upload CSV files containing equipment data
- Support for columns: Equipment, Type, Flowrate, Pressure, Temperature
- Automatic data validation
- Real-time upload feedback

### 3. **Data Summary API**
- Retrieve total count of uploaded datasets
- View aggregated averages (Flowrate, Pressure, Temperature)
- Equipment type distribution across all datasets
- Last 5 datasets management

### 4. **Visualization**
- **Pie Charts**: Equipment type distribution visualization
- **Bar Charts**: Average metrics (Flowrate, Pressure, Temperature)
- **Data Tables**: Detailed view of dataset statistics
- Professional matplotlib-based charts

### 5. **History Management**
- Automatically stores last 5 uploaded datasets per user
- Dataset listing with upload timestamps
- Quick access to previous datasets
- Delete datasets as needed

### 6. **PDF Report Generation**
- Export dataset analysis as professional PDF reports
- Includes summary statistics and type distribution
- Branded formatting with colors and tables

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Install Dependencies**
   ```bash
   cd hybrid_desktop_visualizer
   pip install -r requirements.txt
   ```

2. **Ensure Backend is Running**
   ```bash
   # In the chemical_visualizer directory
   python manage.py runserver
   ```

3. **Run the Desktop Application**
   ```bash
   python main.py
   ```

## User Interface Overview

### Authentication Window
- Clean, modern login/registration interface
- Email validation for registration
- Clear error messages

### Dashboard
- **Header**: User welcome message and logout button
- **Upload Section**: File selection and upload
- **Dataset Table**: Shows last 5 uploaded datasets with actions
- **Three Analysis Tabs**:
  - **Dataset Analysis**: Charts and statistics for selected dataset
  - **Data Table**: Detailed statistics in table format
  - **Overall Summary**: Aggregated data across all datasets

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/accounts/register/` | POST | User registration |
| `/api/accounts/login/` | POST | User login |
| `/api/equipment/upload/` | POST | Upload CSV file |
| `/api/equipment/datasets/` | GET | List user's datasets |
| `/api/equipment/datasets/<id>/` | GET | Get dataset details |
| `/api/equipment/datasets/<id>/` | DELETE | Delete dataset |
| `/api/equipment/datasets/<id>/export-pdf/` | GET | Export as PDF |
| `/api/equipment/summary/` | GET | Get aggregated summary |

## CSV File Format

Required columns for CSV upload:
```
Equipment,Type,Flowrate,Pressure,Temperature
Pump1,Centrifugal,100.5,2.5,25.0
Pump2,Positive Displacement,80.0,3.2,28.5
```

## Features in Detail

### CSV Upload
1. Click "Select File" to browse for CSV
2. File name will appear in the selection field
3. Click "Upload" to submit
4. System validates file format and data
5. Dataset is stored and appears in the table

### Data Analysis
1. Click "Analyze" button for any dataset
2. View statistics: Total Equipment, Avg Flowrate, Avg Pressure, Avg Temperature
3. See pie chart of equipment type distribution
4. See bar chart of average metrics
5. Click "PDF" to export report

### History Management
- Dashboard shows last 5 uploaded datasets
- Each dataset shows filename, upload date, and equipment count
- Use "Analyze", "Table", "PDF", or "Delete" buttons for actions
- "Overall Summary" tab shows aggregated data

### PDF Export
1. Click "PDF" button on any dataset
2. Choose save location
3. Professional report generated with:
   - Dataset name and upload date
   - Summary statistics table
   - Equipment type distribution
   - Professional formatting

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open file dialog |
| Ctrl+Q | Quit application |
| Tab | Navigate between fields |

## Troubleshooting

### Backend Connection Error
- Ensure Django backend is running on `http://localhost:8000`
- Check firewall settings
- Verify backend URL in `api_client.py`

### CSV Upload Fails
- Verify CSV has required columns: Equipment, Type, Flowrate, Pressure, Temperature
- Check file encoding (UTF-8 recommended)
- Ensure no empty rows

### Charts Not Displaying
- Verify matplotlib is installed: `pip install matplotlib==3.8.2`
- Check that dataset has type distribution data

### Login Issues
- Clear browser cache if using web dashboard
- Verify username and password
- Check backend logs for authentication errors

## Configuration

### Changing Backend URL
Edit `api_client.py`:
```python
self.api_client = APIClient("http://your-server:8000/api")
```

### Customizing Theme
Modify `_apply_styles()` in `dashboard_window.py` to change colors and fonts.

## File Structure

```
hybrid_desktop_visualizer/
├── main.py                 # Application entry point
├── api_client.py           # Backend API communication
├── auth_window.py          # Authentication UI
├── dashboard_window.py     # Main dashboard UI
├── requirements.txt        # Python dependencies
└── README_DESKTOP.md       # This file
```

## Dependencies

- **PyQt5**: GUI framework
- **requests**: HTTP client for API calls
- **matplotlib**: Data visualization
- **pandas**: Data processing
- **numpy**: Numerical computations
- **reportlab**: PDF generation

## License

Proprietary - Chemical Visualizer Project

## Support

For issues or questions, contact the development team or refer to the main README.md in the project root.
