# 🚀 Desktop App Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9 or higher installed
- ✅ Backend server running (http://127.0.0.1:8000)
- ✅ Internet connection (for AI features)

## 🎯 Fastest Way to Start (Windows)

### Step 1: Start Backend
```bash
# Open Command Prompt/PowerShell in project root
cd backend
python manage.py runserver
```
Keep this terminal open!

### Step 2: Launch Desktop App
- Double-click `START_DESKTOP.bat` in project root
- Wait for dependencies to install (first time only)
- Application will launch automatically

### Step 3: Login
- Use existing credentials OR
- Click "Sign Up" tab to create new account

### Step 4: Upload & Analyze
- Press `Ctrl+U` or click "📁 Upload CSV"
- Select your CSV file
- View instant analysis!

## 📋 Manual Setup (All Platforms)

### Windows
```bash
cd frontend-desktop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src\main.py
```

### macOS/Linux
```bash
cd frontend-desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## 🎨 First Time Usage

### 1. Create Account
- Launch app
- Click "Sign Up" tab
- Enter username, email, password
- Click "Sign Up" button

### 2. Upload Data
- Click "📁 Upload CSV (Ctrl+U)"
- Select `sample_equipment_data.csv` from project root
- Wait for progress bar to complete

### 3. Explore Features

**Overview Tab:**
- View 6 key statistics
- Read AI-powered insights

**Data Table Tab:**
- Browse raw data
- Scroll through records

**Visualizations Tab:**
- Click "Bar Chart" - Equipment distribution
- Click "Scatter Plot" - Parameter correlation
- Click "Pie Chart" - Health breakdown
- Click "3D Plot" - Interactive 3D view (rotate with mouse!)

**Export Tab:**
- Click "📄 Export PDF Report"
- Enter password (e.g., "test123")
- Save file
- Open PDF with password

### 4. Try Comparison
- Upload another CSV file
- Select 2 files from history (left sidebar)
- Click "⚖️ Compare Selected"
- View comparison results

### 5. Toggle Theme
- Click "🌓 Toggle Theme"
- Switch between light/dark mode
- Preference is saved automatically

## 🔧 Troubleshooting

### "No module named 'PyQt5'"
```bash
pip install PyQt5
```

### "Connection refused"
- Ensure backend is running: `python manage.py runserver`
- Check backend URL in `src/api_client.py`

### "File too large"
- Maximum file size: 10MB
- Compress or split your CSV file

### Charts not showing
```bash
pip install --upgrade matplotlib
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+U | Upload file |
| Enter | Submit login/signup |
| Esc | Close dialogs |

## 📊 Sample Data

Use the included `sample_equipment_data.csv` for testing:
- Located in project root
- Contains 50+ equipment records
- Includes all required columns

## 🎯 Key Features to Try

1. **3D Visualization** (Desktop Exclusive!)
   - Go to Visualizations tab
   - Click "3D Plot"
   - Drag mouse to rotate
   - Scroll to zoom

2. **AI Insights**
   - Upload any CSV
   - Check Overview tab
   - Read detailed AI analysis

3. **Password-Protected Exports**
   - Export PDF or Excel
   - Set strong password
   - Share securely

4. **Dataset Comparison**
   - Upload 2 different files
   - Select both in history
   - Compare metrics

## 📱 Interface Overview

```
┌─────────────────────────────────────────────────┐
│  Chemical Equipment Visualizer - Desktop        │
├──────────┬──────────────────────────────────────┤
│          │  Overview Tab                        │
│ Sidebar  │  ┌────────────────────────────────┐ │
│          │  │ Statistics Cards (6)           │ │
│ • User   │  └────────────────────────────────┘ │
│ • Upload │  ┌────────────────────────────────┐ │
│ • Theme  │  │ AI Insights                    │ │
│ • History│  └────────────────────────────────┘ │
│ • Compare│                                      │
│ • Profile│  [Data Table] [Charts] [Export]     │
│ • Logout │                                      │
│          │                                      │
└──────────┴──────────────────────────────────────┘
```

## 🎓 Learning Path

### Beginner (5 minutes)
1. Login/Signup
2. Upload sample CSV
3. View statistics
4. Read AI insights

### Intermediate (10 minutes)
5. Explore all chart types
6. Try 3D visualization
7. Export PDF report
8. Toggle theme

### Advanced (15 minutes)
9. Upload multiple files
10. Compare datasets
11. Export Excel with password
12. Explore all tabs

## 💡 Pro Tips

1. **Use Ctrl+U** for quick uploads
2. **3D plots** are interactive - drag to rotate!
3. **Theme toggle** works instantly
4. **History** shows last 10 uploads
5. **Passwords** protect your exports
6. **AI insights** provide actionable recommendations

## 🔒 Security Notes

- Passwords are never stored
- JWT tokens in memory only
- Logout clears all data
- Exports are encrypted

## 📞 Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Review `FEATURES.md` for complete feature list
3. Check backend logs for API errors
4. Ensure backend is running on port 8000

## 🎉 Success Checklist

- ✅ Backend running
- ✅ Desktop app launched
- ✅ Logged in successfully
- ✅ CSV uploaded
- ✅ Analysis displayed
- ✅ Charts rendered
- ✅ Export working
- ✅ Theme toggle working

## 🚀 Next Steps

After mastering the basics:
1. Try with your own CSV data
2. Experiment with different datasets
3. Compare multiple analyses
4. Generate professional reports
5. Share encrypted exports

---

**Ready to analyze? Launch the app and press Ctrl+U!** 🎯

**Questions?** Check the documentation files:
- `README.md` - Overview
- `SETUP_GUIDE.md` - Detailed setup
- `FEATURES.md` - Complete features

**Happy Analyzing! 📊**
