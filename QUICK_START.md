#  Quick Setup Checklist - Charts & Features Edition

##  Pre-Install Checks

- [ ] Node.js installed? (`node --version`)
- [ ] npm installed? (`npm --version`)
- [ ] Python venv activated? (See `venv\Scripts\activate`)
- [ ] Django running on port 8000? (`python manage.py runserver`)

##  Step 1: Install New Dependencies

```bash
cd c:\Users\Surjeet Kumar\chemical_visualizer\chemical-frontend
npm install
```

**What gets installed:**
- chart.js - Chart visualization
- react-chartjs-2 - React charts component
- jspdf - PDF generation
- html2canvas - Chart to image conversion

**Expected time:** 2-3 minutes
**Expected output:** "added X packages, up to date..."

##  Step 2: Start Backend (Terminal 1)

```bash
cd c:\Users\Surjeet Kumar\chemical_visualizer
venv\Scripts\activate
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
```

 **Backend ready when you see the message above**

##  Step 3: Start Frontend (Terminal 2)

```bash
cd c:\Users\Surjeet Kumar\chemical_visualizer\chemical-frontend
npm start
```

**Expected output:**
```
Compiled successfully!
You can now view chemical-visualizer-frontend in the browser.
Local: http://localhost:3000
```

 **Frontend ready when you see "Compiled successfully!"**

##  Step 4: Open Browser

**URL:** http://localhost:3000

You should see the login page with:
-  Chemical Visualizer title
- Username/Password input fields
- Login and Register buttons

##  Step 5: Test New Features

### Test 1: Upload CSV
```
1. Register new account (or use existing)
2. Click "Upload" button
3. Select sample_data.csv from project root
4. Wait for success message
```

 **Pass if:** File appears in "My Datasets" list

### Test 2: View Charts
```
1. Click " Analyze" on the uploaded dataset
2. Look for statistics cards (4 cards with metrics)
3. Look for two charts:
   - Doughnut chart (Equipment Distribution)
   - Bar chart (Average Parameters)
```

 **Pass if:** Charts render with data and colors

### Test 3: View Data Table
```
1. Click "📋 Table" on the dataset
2. Look for table with metrics and equipment breakdown
```

 **Pass if:** Table displays all metrics correctly

### Test 4: View History
```
1. Click " History (N)" button (N = number of datasets)
2. Dropdown menu appears showing recent uploads
```

 **Pass if:** List shows up to 5 recent uploads

### Test 5: Export PDF
```
1. After analyzing, click "📥 Export as PDF (with Charts)"
2. Wait 2-3 seconds for generation
3. Check Downloads folder
```

 **Pass if:** PDF file appears in Downloads with charts

##  Troubleshooting

### Issue: npm install fails
```bash
# Clear cache and try again
npm cache clean --force
npm install
```

### Issue: Charts not showing
```bash
# Restart frontend
npm start
```

### Issue: Port 3000 already in use
```bash
# Use different port
PORT=3001 npm start
# Update .env file:
# REACT_APP_API_URL=http://localhost:8000/api
```

### Issue: Backend connection error
```bash
# Check backend is running
http://localhost:8000/api/auth/login/
# Should show API response, not connection refused
```

##  Feature Summary

| Feature | Button | What It Does |
|---------|--------|------------|
| Analyze |  Analyze | Shows charts & statistics |
| Table |  Table | Shows data in table format |
| History |  History | Shows last 5 uploads |
| PDF Export |  PDF | Downloads PDF report |
| Full PDF |  Export PDF (with Charts) | PDF with all visualizations |

##  Files Modified

```
chemical-frontend/
├── package.json          Updated dependencies
├── src/components/
│   ├── Dashboard.js      Added charts & features
│   └── Dashboard.css      New styles
```

##  Documentation Files

- `CHARTS_FEATURES.md` - Detailed feature documentation
- `RUN_NOW.md` - Complete setup guide
- `FRONTEND_SETUP.md` - Frontend installation guide
- `README_FRONTEND.md` - Quick reference

##  What's New

 Chart.js integration for visualizations
 Doughnut chart for equipment distribution
 Bar chart for average parameters
 Data table view for all metrics
 History dropdown showing last 5 uploads
 Enhanced PDF export with charts
 Responsive design for mobile/tablet
 Professional styling with colors and animations

##  Success Criteria

You'll know everything works when:

1.  Login/Register works
2.  Can upload CSV file
3.  Clicking "Analyze" shows 2 charts
4.  Clicking "Table" shows data table
5.  Clicking "History" shows dropdown with datasets
6.  Clicking "Export PDF" downloads PDF with charts
7.  All buttons respond with no console errors
8.  Charts look colorful and properly formatted

##  Ready to Go!

```bash
# One final check - run these commands:

# Terminal 1: Backend
python manage.py runserver

# Terminal 2: Frontend
npm start

# Browser: Open http://localhost:3000
```

**Everything is set up and ready to use!**

---

**Need help?** Check the error messages in:
- Browser console (F12)
- Terminal output
- Network tab (F12 > Network)

**Duration:** Setup should take ~5 minutes total
**Status:** ✅ Production Ready
