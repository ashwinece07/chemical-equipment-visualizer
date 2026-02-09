# 🧪 POTASH - Chemical Equipment Parameter Visualizer

A production-ready hybrid web + desktop application for chemical equipment data visualization and intelligent analytics powered by AI.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![React](https://img.shields.io/badge/React-19.2.0-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📖 About

POTASH is an enterprise-grade data analytics platform designed for chemical engineers to visualize, analyze, and monitor equipment parameters in real-time. Built with modern technologies, it offers both web and desktop interfaces with AI-powered insights from Google Gemini.

---

## ✨ Key Features

### 🔐 Core Functionality
- **JWT Authentication** - Secure login/signup with access & refresh tokens
- **CSV Upload** - Drag & drop interface with 10MB file size limit
- **Real-time Analysis** - Instant statistical analysis with progress tracking
- **AI-Powered Insights** - Google Gemini API integration for intelligent summaries
- **Interactive Visualizations** - 7 chart types (Bar, Scatter, Pie, 3D, Heatmap, Box Plot, Histogram)
- **Dataset Comparison** - Side-by-side comparison of two datasets
- **Upload History** - Last 10 uploads with metadata
- **Password-Protected Exports** - Encrypted PDF & Excel reports
- **Dark/Light Theme** - Professional UI with theme switching
- **User Profile Management** - Edit profile, change password, view statistics

### 📊 Advanced Analytics
- **Health Score Algorithm** - 0-100 rating based on parameter deviations
- **Outlier Detection** - Z-score method (>3σ flagged)
- **Correlation Matrix** - Pearson correlation heatmap
- **Distribution Analysis** - Box plots with quartiles and outliers
- **Frequency Analysis** - Histograms for parameter distribution
- **Equipment Type Statistics** - Breakdown by category
- **Anomaly Alerts** - Visual indicators for equipment issues
- **3D Visualization** - Interactive 3D scatter plots (Desktop exclusive)

### 🔒 Security & Performance
- **Rate Limiting** - 100 requests/hour per authenticated user
- **File Validation** - MIME type + extension checks
- **Optimized Queries** - Efficient database operations
- **Auto Cleanup** - Keeps only last 10 files per user
- **CORS Protection** - Configured for frontend origins

---

## 🖥️ Platform Support

- **Web Application**: Chrome, Firefox, Safari, Edge (latest versions)
- **Desktop Application**: Windows 10/11, macOS 12+, Ubuntu 20.04+

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/downloads/)
- **Google Gemini API Key** - [Get API Key](https://makersuite.google.com/app/apikey)

---

## 🚀 Quick Start Guide

### Option 1: Clone from GitHub

```bash
git clone https://github.com/YOUR_USERNAME/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

### Option 2: Download ZIP

1. Download the project ZIP file
2. Extract to your desired location
3. Open terminal/command prompt in the extracted folder

---

## 🔧 Installation & Setup

### STEP 1: Backend Setup (Required for Both Web & Desktop)

#### 1.1 Navigate to Backend Directory

```bash
cd backend
```

#### 1.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your command line.

#### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install Django, Pandas, NumPy, Matplotlib, and other required packages.

#### 1.4 Configure Environment Variables

The `.env` file already exists in the `backend/` folder with your Gemini API key. If you need to modify it:

**backend/.env:**
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SECRET_KEY=django-insecure-your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 1.5 Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 1.6 (Optional) Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

#### 1.7 Start Backend Server

```bash
python manage.py runserver
```

✅ **Backend is now running at:** `http://127.0.0.1:8000`

**Keep this terminal window open!**

---

### STEP 2A: Web Application Setup

#### 2A.1 Open New Terminal

Open a **NEW** terminal/command prompt window (keep backend running).

#### 2A.2 Navigate to Frontend Directory

```bash
cd frontend-web
```

#### 2A.3 Install Node Dependencies

```bash
npm install
```

This will install React, Vite, Chart.js, and other frontend packages. This may take a few minutes.

#### 2A.4 Configure Environment Variables

The `.env` file already exists in the `frontend-web/` folder. If you need to modify it:

**frontend-web/.env:**
```env
VITE_API_URL=http://127.0.0.1:8000/api/
```

#### 2A.5 Start Development Server

```bash
npm run dev
```

✅ **Web app is now running at:** `http://localhost:5173`

**Keep this terminal window open!**

#### 2A.6 Access the Web Application

1. Open your web browser
2. Go to: `http://localhost:5173`
3. You should see the POTASH home page
4. Click "Sign Up" to create an account
5. Login with your credentials
6. Upload the `sample_equipment_data.csv` file to test

---

### STEP 2B: Desktop Application Setup (Alternative to Web)

#### 2B.1 Open New Terminal

Open a **NEW** terminal/command prompt window (keep backend running).

#### 2B.2 Navigate to Desktop Directory

```bash
cd frontend-desktop
```

#### 2B.3 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2B.4 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install PyQt5, Matplotlib, and other desktop app packages.

#### 2B.5 Start Desktop Application

```bash
python src/main.py
```

✅ **Desktop application window will open automatically**

#### 2B.6 Windows Quick Launch (Alternative)

Double-click `START_DESKTOP.bat` in the project root folder.

---

## 📝 Step-by-Step Usage Guide

### Using the Web Application

#### Step 1: Create Account
1. Open `http://localhost:5173` in your browser
2. Click "Sign Up" button
3. Enter username, email, and password
4. Click "Create Account"
5. You'll be redirected to the dashboard

#### Step 2: Upload CSV File
1. Click the "Choose File" button or drag & drop a CSV file
2. Or press `Ctrl+U` for quick upload
3. Select `sample_equipment_data.csv` from the project root
4. Wait for the upload and analysis to complete (progress bar will show)

#### Step 3: View Analysis Results
1. See AI-powered insights at the top
2. View key metrics: Total Equipment, Avg Pressure, Avg Temperature, Health Score
3. Scroll down to see interactive charts:
   - Equipment Types Distribution (Pie Chart)
   - Health Score Distribution (Bar Chart)
   - Parameter Correlations (Scatter Plot)
   - Average Metrics (Bar Chart)

#### Step 4: Export Reports
1. Click "Export PDF" or "Export Excel" button
2. Enter a password for encryption
3. Click OK
4. File will download automatically
5. Open the file and enter the password you set

#### Step 5: Compare Datasets
1. Upload at least 2 CSV files
2. Click the compare icon (⚖️) in the history sidebar
3. Select exactly 2 files from history
4. Click "Compare Selected"
5. View side-by-side comparison

#### Step 6: Manage Profile
1. Click the profile icon in the navbar
2. View your upload statistics
3. Click "Edit Profile" to update information
4. Change password if needed
5. Logout when done

### Using the Desktop Application

#### Step 1: Login
1. Launch the desktop app
2. Enter your username and password (same as web app)
3. Or click "Create Account" if you don't have one
4. Click "Login"

#### Step 2: Upload CSV File
1. Click "📁 Upload CSV" button
2. Or press `Ctrl+U`
3. Select `sample_equipment_data.csv`
4. Wait for analysis to complete

#### Step 3: Explore Visualizations
1. Use the chart type dropdown to switch between:
   - **Bar Chart** - Equipment type distribution
   - **Scatter Plot** - Parameter correlations
   - **Pie Chart** - Health score breakdown
   - **3D Plot** - Interactive 3D visualization (drag to rotate, scroll to zoom)
   - **Heatmap** - Correlation matrix
   - **Box Plot** - Distribution analysis
   - **Histogram** - Frequency distribution

#### Step 4: Export Reports
1. Click "📄 Export PDF Report" or "📊 Export Excel Report"
2. Enter a password
3. Choose save location
4. Click Save

#### Step 5: Compare Datasets
1. Upload at least 2 files
2. Select 2 files from history (hold Ctrl and click)
3. Click "⚖️ Compare Selected"
4. View comparison results

---

## 📊 Sample Data Format

Your CSV file should contain these columns (case-insensitive):

```csv
Equipment_Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,85.2
Reactor-A1,Reactor,200.0,45.8,120.5
HeatEx-12,Heat Exchanger,180.2,30.1,95.7
Compressor-5,Compressor,175.3,35.2,95.0
Valve-23,Valve,120.0,20.5,75.3
```

### Required Columns:
- `Equipment_Name` or `Name` - Equipment identifier
- `Type` or `Equipment_Type` - Category (Pump, Reactor, Heat Exchanger, etc.)
- `Flowrate` or `Flow_Rate` - Numeric flow value
- `Pressure` - Numeric pressure value (bar)
- `Temperature` or `Temp` - Numeric temperature value (°C)

### Optional Columns:
- `Timestamp` or `Date` - For trend analysis

A sample file `sample_equipment_data.csv` is included in the project root for testing.

---

## 🎯 API Endpoints

### Authentication
```
POST   /api/signup/              # Register new user
POST   /api/login/               # Login (returns JWT tokens)
POST   /api/token/refresh/       # Refresh access token
POST   /api/logout/              # Logout (blacklist refresh token)
```

### User Profile
```
GET    /api/profile/             # Get user profile
PUT    /api/profile/             # Update user profile
POST   /api/profile/password/    # Change password
```

### Data Management
```
POST   /api/upload/              # Upload CSV file
GET    /api/analysis/{id}/       # Get analysis for specific file
GET    /api/history/             # Get upload history
POST   /api/compare/             # Compare two datasets
DELETE /api/delete/{id}/         # Delete uploaded file
```

### Export
```
POST   /api/export/pdf/{id}/     # Generate encrypted PDF
POST   /api/export/excel/{id}/   # Generate encrypted Excel
```

---

## 🎨 Tech Stack

### Backend
- Django 4.2.7 - Web framework
- Django REST Framework - API development
- djangorestframework-simplejwt - JWT authentication
- Pandas - Data manipulation
- NumPy & SciPy - Statistical analysis
- Matplotlib - Chart generation
- ReportLab - PDF generation
- XlsxWriter - Excel export
- Google Generative AI - AI-powered insights

### Web Frontend
- React 19.2 - UI framework
- Vite - Build tool
- React Router - Navigation
- Axios - HTTP client
- Chart.js - Data visualization
- Framer Motion - Animations
- Tailwind CSS - Styling
- React Dropzone - File upload
- React Hot Toast - Notifications
- Lucide React - Icons

### Desktop Frontend
- PyQt5 - Native GUI framework
- Matplotlib - 2D/3D plotting
- Requests - HTTP client
- Pandas - Data handling
- NumPy - Numerical operations

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'django'`
```bash
cd backend
pip install -r requirements.txt
```

**Problem:** `Port 8000 already in use`
```bash
# Find and kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

**Problem:** `GEMINI_API_KEY not found`
- Check that `backend/.env` file exists
- Ensure it contains your actual API key
- Restart the backend server

### Web Frontend Issues

**Problem:** `npm: command not found`
- Install Node.js from https://nodejs.org/

**Problem:** `Module not found errors`
```bash
cd frontend-web
rm -rf node_modules package-lock.json
npm install
```

**Problem:** `Cannot connect to backend`
- Ensure backend is running on port 8000
- Check `frontend-web/.env` has correct API URL
- Check browser console for CORS errors

### Desktop App Issues

**Problem:** `No module named 'PyQt5'`
```bash
cd frontend-desktop
pip install -r requirements.txt
```

**Problem:** `Connection refused`
- Ensure Django backend is running
- Backend must be on port 8000

**Problem:** `Login failed`
- Create account in web app first
- Or use desktop signup feature

---

## 🔄 Stopping the Applications

### Stop Web Application:
1. Go to Backend Terminal - Press `Ctrl+C`
2. Go to Frontend Terminal - Press `Ctrl+C`

### Stop Desktop Application:
1. Close the desktop window
2. Go to Backend Terminal - Press `Ctrl+C`

---

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django REST API
│   ├── api/                   # API endpoints & logic
│   ├── backend/               # Django settings
│   ├── media/                 # Uploaded files
│   ├── .env                   # Environment variables
│   ├── db.sqlite3            # SQLite database
│   ├── manage.py             # Django management
│   └── requirements.txt      # Python dependencies
├── frontend-web/              # React web application
│   ├── src/                  # Source code
│   ├── public/               # Static assets
│   ├── .env                  # Environment variables
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
├── frontend-desktop/          # PyQt5 desktop application
│   ├── src/                  # Source code
│   ├── requirements.txt      # Python dependencies
│   └── main.py              # Entry point
├── sample_equipment_data.csv  # Sample test data
├── README.md                  # This file
├── DEPLOYMENT_GUIDE.md        # AWS deployment guide
├── QUICK_START_GUIDE.md       # Quick start instructions
└── .gitignore                # Git ignore rules
```

---

## 💡 Tips & Shortcuts

1. **Always start backend first** before frontend/desktop
2. **Keep terminal windows open** while using the apps
3. **Use same credentials** for both web and desktop
4. **Data is shared** between web and desktop apps
5. **Press Ctrl+U** for quick file upload
6. **Sample data** is in project root folder
7. **Check browser console** for debugging web app
8. **Check terminal output** for backend errors

---

## 🔐 Security Notes

- Never commit `.env` files to Git
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use strong passwords for user accounts
- Keep your Gemini API key private
- Enable HTTPS in production

---

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review terminal/console error messages
- Ensure all dependencies are installed
- Verify environment variables are set correctly

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🎉 Acknowledgments

- Google Gemini API for AI insights
- Chart.js for beautiful visualizations
- Django & React communities
- All open-source contributors

---

**Built with ❤️ for Chemical Engineers | POTASH v1.0.0**

---

## ✅ Quick Reference

### Start Web Application:
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python manage.py runserver

# Terminal 2 - Frontend
cd frontend-web
npm run dev

# Browser: http://localhost:5173
```

### Start Desktop Application:
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python manage.py runserver

# Terminal 2 - Desktop
cd frontend-desktop
venv\Scripts\activate
python src/main.py
```

### Test the Application:
1. Create account / Login
2. Upload `sample_equipment_data.csv`
3. View AI analysis and charts
4. Export PDF/Excel reports
5. Compare datasets
6. Manage profile

---

**🚀 Ready to analyze your chemical equipment data!**
