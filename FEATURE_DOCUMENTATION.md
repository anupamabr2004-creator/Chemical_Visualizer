# Chemical Visualizer - Complete Feature Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│         Chemical Visualizer Desktop (PyQt5)         │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Authentication Module (JWT)                 │   │
│  │  - Register/Login                            │   │
│  │  - Token Management                          │   │
│  └──────────────────────────────────────────────┘   │
│                        ↕                             │
│  ┌──────────────────────────────────────────────┐   │
│  │  API Client (Requests)                       │   │
│  │  - File Upload                               │   │
│  │  - Data Retrieval                            │   │
│  │  - PDF Export                                │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│      Django REST API (chemical_visualizer)          │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Accounts Module                             │   │
│  │  - register() → User Creation                │   │
│  │  - login() → JWT Token Generation            │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Equipment Module                            │   │
│  │  - UploadCSV → Data Processing               │   │
│  │  - DatasetList → User's Datasets             │   │
│  │  - DataSummary → Aggregated Analytics        │   │
│  │  - ExportPDF → Report Generation             │   │
│  └──────────────────────────────────────────────┘   │
│                        ↕                             │
│  ┌──────────────────────────────────────────────┐   │
│  │  Database (SQLite/PostgreSQL)                │   │
│  │  - User Accounts (Django Auth)               │   │
│  │  - Datasets Storage                          │   │
│  │  - Statistics & Summaries                    │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Feature 1: User Authentication

### Registration Flow
```
User Input (Username, Email, Password)
            ↓
Validation (Frontend)
            ↓
POST /api/accounts/register/
            ↓
Django Creates User
            ↓
Success: User can now login
```

### Login Flow
```
User Input (Username, Password)
            ↓
POST /api/accounts/login/
            ↓
Django Authenticates User
            ↓
JWT Token Generated
            ↓
Token Stored in API Client
            ↓
All Subsequent Requests Use Token
```

### Implementation Details

**Frontend (PyQt5):**
- `AuthWindow` class handles UI
- Two tabs: Login and Register
- Beautiful gradient design
- Real-time validation

**Backend (Django):**
- `/accounts/register/` endpoint
- `/accounts/login/` endpoint
- JWT token generation via `djangorestframework-simplejwt`
- User isolation (each user only sees their data)

## Feature 2: CSV Upload

### Upload Process

```
User Selects CSV File
            ↓
File Validation (Client-side)
            ↓
POST /api/equipment/upload/
            ↓
Server Validates:
  - File Format (CSV)
  - Columns (Equipment, Type, Flowrate, Pressure, Temperature)
  - Data Types (Numeric values)
            ↓
pandas.read_csv() Processing
            ↓
Calculate Summaries:
  - Total Count
  - Averages (Flowrate, Pressure, Temperature)
  - Type Distribution
            ↓
Dataset Model Created
            ↓
Old Datasets Pruned (Keep Last 5)
            ↓
Success Response with Summary
```

### CSV Format Requirements

```csv
Equipment,Type,Flowrate,Pressure,Temperature
Pump-001,Centrifugal,125.5,3.2,28.5
Valve-001,Check Valve,140.0,2.8,25.0
Compressor-001,Rotary,85.0,5.5,45.0
```

**Required Columns:**
- `Equipment`: Equipment identifier (string)
- `Type`: Equipment type/category (string)
- `Flowrate`: Flow rate in L/min (numeric)
- `Pressure`: Pressure in bar (numeric)
- `Temperature`: Temperature in °C (numeric)

## Feature 3: Data Summary API

### Aggregated Statistics

```
GET /api/equipment/summary/
            ↓
Retrieve All User's Datasets
            ↓
Calculate Aggregations:
  - Total Datasets Count
  - Total Equipment Count
  - Weighted Average Flowrate
  - Weighted Average Pressure
  - Weighted Average Temperature
  - Aggregated Type Distribution
            ↓
Return JSON Response
```

### Response Format

```json
{
  "total_count": 3,
  "total_equipment": 45,
  "average_flowrate": 112.50,
  "average_pressure": 3.42,
  "average_temperature": 28.75,
  "type_distribution": {
    "Centrifugal": 12,
    "Positive Displacement": 8,
    "Rotary": 5,
    "Check Valve": 10,
    "Ball Valve": 10
  },
  "datasets_count": 3
}
```

## Feature 4: Visualization

### Chart Types

#### 1. Type Distribution Pie Chart
```
Equipment Types Distribution
├── Centrifugal (30%)
├── Positive Displacement (20%)
├── Rotary (15%)
├── Check Valve (20%)
└── Ball Valve (15%)
```

**Technology:** Matplotlib `pie()` function
**Data Source:** `type_distribution` from dataset

#### 2. Average Metrics Bar Chart
```
Average Equipment Metrics
├── Flowrate: 112.5 L/min
├── Pressure: 3.42 bar
└── Temperature: 28.75 °C
```

**Technology:** Matplotlib `bar()` function
**Data Source:** average_flowrate, average_pressure, average_temperature

### Visualization Features
- **Colors**: Professional color scheme
- **Labels**: Clear metric labels with units
- **Responsive**: Charts resize with window
- **Interactive**: Can zoom and pan (matplotlib toolbar)

## Feature 5: History Management

### Last 5 Datasets Storage

**Database Level:**
```sql
SELECT * FROM equipment_dataset 
WHERE user_id = ? 
ORDER BY uploaded_at DESC 
LIMIT 5
```

**Automatic Cleanup:**
```python
datasets = Dataset.objects.filter(user=user).order_by("-uploaded_at")
if datasets.count() > 5:
    for old in datasets[5:]:
        old.delete()  # Delete oldest datasets beyond 5
```

**User Interface:**
```
┌─ My Datasets (Last 5) ──────────────────────┐
│ Filename │ Uploaded   │ Equipment │ Actions │
├──────────┼────────────┼───────────┼─────────┤
│ data1.csv│ 2024-02-02 │ 15        │ [▼] [▼] │
│ data2.csv│ 2024-02-01 │ 20        │ [▼] [▼] │
│ data3.csv│ 2024-01-30 │ 10        │ [▼] [▼] │
│ data4.csv│ 2024-01-28 │ 25        │ [▼] [▼] │
│ data5.csv│ 2024-01-25 │ 18        │ [▼] [▼] │
└──────────┴────────────┴───────────┴─────────┘
```

**Dataset Operations:**
- **Analyze** - View charts and statistics
- **Table** - View detailed statistics
- **PDF** - Export as report
- **Delete** - Remove dataset

## Feature 6: PDF Report Generation

### Report Structure

```
┌─────────────────────────────────────────┐
│   Chemical Visualizer Report            │
│   Equipment Analysis Summary            │
├─────────────────────────────────────────┤
│                                         │
│  Dataset: sample_equipment_data.csv     │
│  Date: 2024-02-02 14:30:45             │
│                                         │
├─────────────────────────────────────────┤
│  Summary Statistics                     │
├─────────────────────────────────────────┤
│ Total Equipment    │ 15                 │
│ Average Flowrate   │ 112.50 L/min       │
│ Average Pressure   │ 3.42 bar           │
│ Average Temp       │ 28.75 °C           │
│ Uploaded Date      │ 2024-02-02 14:30   │
├─────────────────────────────────────────┤
│  Equipment Type Distribution            │
├─────────────────────────────────────────┤
│ Type               │ Count              │
│ Centrifugal        │ 4                  │
│ Positive Disp.     │ 3                  │
│ Rotary             │ 2                  │
│ Check Valve        │ 3                  │
│ Ball Valve         │ 3                  │
└─────────────────────────────────────────┘
```

### PDF Generation Process

```python
# Using reportlab
buffer = io.BytesIO()
pdf = SimpleDocTemplate(buffer, pagesize=letter)
elements = []

# Add title, tables, and formatting
pdf.build(elements)

# Return as HTTP response
response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
```

### Export Workflow

```
User Clicks "PDF" Button
            ↓
GET /api/equipment/datasets/{id}/export-pdf/
            ↓
Server Retrieves Dataset
            ↓
Generate PDF with reportlab
            ↓
Return PDF Bytes
            ↓
User Selects Save Location
            ↓
Save to File System
            ↓
Open with Default PDF Viewer
```

## API Endpoint Reference

### Authentication Endpoints

#### POST /accounts/register/
```json
Request:
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}

Response (201):
{
  "message": "Registration successful"
}
```

#### POST /accounts/login/
```json
Request:
{
  "username": "john_doe",
  "password": "securepass123"
}

Response (200):
{
  "message": "Login successful",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "john_doe"
}
```

### Equipment Endpoints

#### POST /equipment/upload/
```
Headers:
  Authorization: Bearer <token>
  Content-Type: multipart/form-data

Request:
  file: <CSV file>

Response (201):
{
  "total_equipment": 15,
  "average_flowrate": 112.50,
  "average_pressure": 3.42,
  "average_temperature": 28.75,
  "type_distribution": {
    "Centrifugal": 4,
    "Check Valve": 3
  }
}
```

#### GET /equipment/datasets/
```
Headers:
  Authorization: Bearer <token>

Response (200):
[
  {
    "id": 1,
    "filename": "data.csv",
    "uploaded_at": "2024-02-02T14:30:45Z",
    "total_equipment": 15,
    "average_flowrate": 112.50,
    "average_pressure": 3.42,
    "average_temperature": 28.75,
    "type_distribution": {
      "Centrifugal": 4
    }
  }
]
```

#### GET /equipment/datasets/{id}/
```
Headers:
  Authorization: Bearer <token>

Response (200):
{
  "id": 1,
  "filename": "data.csv",
  "uploaded_at": "2024-02-02T14:30:45Z",
  "total_equipment": 15,
  "average_flowrate": 112.50,
  "average_pressure": 3.42,
  "average_temperature": 28.75,
  "type_distribution": {
    "Centrifugal": 4
  }
}
```

#### DELETE /equipment/datasets/{id}/
```
Headers:
  Authorization: Bearer <token>

Response (204): No Content
```

#### GET /equipment/datasets/{id}/export-pdf/
```
Headers:
  Authorization: Bearer <token>

Response (200):
<PDF Binary Data>

Headers:
  Content-Type: application/pdf
  Content-Disposition: attachment; filename="data.csv.pdf"
```

#### GET /equipment/summary/
```
Headers:
  Authorization: Bearer <token>

Response (200):
{
  "total_count": 3,
  "total_equipment": 45,
  "average_flowrate": 112.50,
  "average_pressure": 3.42,
  "average_temperature": 28.75,
  "type_distribution": {
    "Centrifugal": 12,
    "Check Valve": 10
  },
  "datasets_count": 3
}
```

## Data Models

### User Model (Django Built-in)
```python
class User:
    id: int
    username: str
    email: str
    password: str (hashed)
    is_active: bool
    date_joined: datetime
```

### Dataset Model
```python
class Dataset:
    id: int
    user: ForeignKey(User)  # One-to-Many relationship
    filename: str
    uploaded_at: datetime
    total_equipment: int
    average_flowrate: float
    average_pressure: float
    average_temperature: float
    type_distribution: JSON
```

## Security Features

1. **JWT Authentication**
   - Token-based authentication
   - Tokens expire after 5 minutes (access token)
   - Refresh tokens for long-term sessions

2. **User Data Isolation**
   - Users only see their own datasets
   - Enforced at database level with `user=request.user`
   - No cross-user data access

3. **CSRF Protection**
   - Django's CSRF middleware
   - Token validation on state-changing operations

4. **Password Security**
   - Passwords hashed with Django's default hasher
   - Never stored in plain text
   - No password in API responses

## Performance Considerations

1. **Database Queries**
   - Datasets limited to last 5 per user
   - Aggregation done in Python (could use SQL for scale)
   - Indexed by user and upload date

2. **File Upload**
   - CSV parsed in memory (suitable for < 100MB files)
   - Automatic cleanup of old datasets
   - Multipart form handling

3. **PDF Generation**
   - Done server-side to reduce client load
   - Cached in memory until download
   - No disk storage required

## Error Handling

### Client-Side
```python
try:
    success, message, data = api_client.get_datasets()
    if success:
        # Display data
    else:
        # Show error message
except requests.exceptions.ConnectionError:
    # Handle connection errors
except Exception as e:
    # Handle unexpected errors
```

### Server-Side
```python
try:
    df = pd.read_csv(file)
    # Process file
except Exception as e:
    return Response(
        {"error": f"Failed to process CSV: {str(e)}"},
        status=status.HTTP_400_BAD_REQUEST
    )
```

## Testing

### Unit Tests
- Backend API endpoints
- CSV processing logic
- PDF generation

### Integration Tests
- Full upload workflow
- Authentication flow
- End-to-end data analysis

### Manual Tests
- Desktop application UI
- File upload with various formats
- Chart rendering
- PDF export

## Deployment Notes

1. **Production Configuration**
   - Change SECRET_KEY in Django settings
   - Set DEBUG=False
   - Configure ALLOWED_HOSTS
   - Use environment variables for sensitive data

2. **Database**
   - Use PostgreSQL instead of SQLite
   - Implement proper backup strategy
   - Monitor disk space

3. **API Server**
   - Use Gunicorn/uWSGI instead of development server
   - Use Nginx as reverse proxy
   - Enable SSL/TLS for HTTPS

4. **Desktop Client**
   - Update API URL to production server
   - Add SSL certificate verification
   - Implement offline caching

## Conclusion

The Chemical Visualizer provides a complete, integrated solution for:
- Secure user authentication
- Equipment data management
- Advanced analytics and visualization
- Professional report generation
- Historical data tracking

All features work seamlessly together to provide a comprehensive chemical equipment analysis platform.
