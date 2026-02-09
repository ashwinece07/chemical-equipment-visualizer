# 🚀 Getting Started with Desktop App

## ⚡ Quick Start (2 Minutes)

### Step 1: Start Backend
```bash
# Open terminal in project root
cd backend
python manage.py runserver
```
✅ Keep this terminal open!

### Step 2: Launch Desktop App

**Windows (Easiest):**
- Double-click `START_DESKTOP.bat` in project root
- Wait for setup (first time only)
- App launches automatically!

**Manual (All Platforms):**
```bash
cd frontend-desktop
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python src/main.py
```

### Step 3: Login
- Use existing credentials OR
- Click "Sign Up" tab to create account

### Step 4: Upload & Analyze
- Press `Ctrl+U` or click "📁 Upload CSV"
- Select `sample_equipment_data.csv`
- View instant analysis!

---

## 🎯 What You Get

### ✅ All Web Features
- JWT Authentication
- CSV Upload & Analysis
- AI-Powered Insights
- Interactive Charts
- Dataset Comparison
- Password-Protected Exports
- Dark/Light Theme
- User Profile

### ⭐ Plus Desktop Exclusives
- **3D Interactive Plots** (rotate with mouse!)
- Native Performance
- Offline Capability
- System Integration

---

## 📊 Key Features to Try

### 1. 3D Visualization (Desktop Exclusive!)
```
1. Upload CSV file
2. Go to "Visualizations" tab
3. Click "3D Plot" button
4. Drag mouse to rotate
5. Scroll to zoom
```

### 2. AI Insights
```
1. Upload any CSV
2. Check "Overview" tab
3. Read detailed AI analysis
4. Get actionable recommendations
```

### 3. Password-Protected Exports
```
1. Upload and analyze data
2. Go to "Export" tab
3. Click "Export PDF Report"
4. Enter password (e.g., "secure123")
5. Save and share securely
```

### 4. Dataset Comparison
```
1. Upload 2 different CSV files
2. Select both in history (left sidebar)
3. Click "⚖️ Compare Selected"
4. View side-by-side comparison
```

### 5. Theme Toggle
```
1. Click "🌓 Toggle Theme" button
2. Switch between dark/light mode
3. Preference saved automatically
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+U` | Quick file upload |
| `Enter` | Submit login/signup |
| `Esc` | Close dialogs |

---

## 📁 Sample Data

Use the included sample file for testing:
- **Location**: `sample_equipment_data.csv` (project root)
- **Contents**: 50+ equipment records
- **Columns**: Equipment_Name, Type, Flowrate, Pressure, Temperature

---

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────┐
│  Chemical Equipment Visualizer - Desktop    │
├──────────┬──────────────────────────────────┤
│ SIDEBAR  │  MAIN CONTENT                    │
│          │                                   │
│ 👤 User  │  [Overview] [Data] [Charts]      │
│ 📁 Upload│                                   │
│ 🌓 Theme │  📊 Statistics Cards (6)         │
│          │  🤖 AI Insights                  │
│ 📜 Hist: │  📈 Interactive Charts           │
│  • File1 │  📄 Export Options               │
│  • File2 │                                   │
│          │                                   │
│ ⚖️ Comp  │                                   │
│ 👤 Prof  │                                   │
│ 🚪 Logout│                                   │
└──────────┴──────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### "Connection refused"
✅ **Solution**: Ensure backend is running
```bash
cd backend
python manage.py runserver
```

### "Module not found"
✅ **Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "Charts not showing"
✅ **Solution**: Update matplotlib
```bash
pip install --upgrade matplotlib
```

### "Theme not saving"
✅ **Solution**: Check write permissions
- Windows: Registry access
- macOS/Linux: ~/.config/ directory

---

## 📚 Documentation

| Document | Purpose | Time |
|----------|---------|------|
| `QUICKSTART.md` | Fast start | 5 min |
| `README.md` | Overview | 10 min |
| `SETUP_GUIDE.md` | Detailed setup | 15 min |
| `FEATURES.md` | All features | 20 min |

---

## 💡 Pro Tips

1. **Use Ctrl+U** for fastest upload
2. **3D plots** are interactive - drag to rotate!
3. **Theme toggle** works instantly
4. **History** auto-refreshes after upload
5. **Exports** are password-protected
6. **Backend** must be running first

---

## 🎓 Learning Path

### Beginner (5 minutes)
1. Launch app
2. Login/Signup
3. Upload sample CSV
4. View statistics
5. Read AI insights

### Intermediate (10 minutes)
6. Explore all chart types
7. Try 3D visualization
8. Export PDF report
9. Toggle theme
10. View profile

### Advanced (15 minutes)
11. Upload multiple files
12. Compare datasets
13. Export Excel with password
14. Explore all tabs
15. Master keyboard shortcuts

---

## 🎯 Success Checklist

- [ ] Backend running on port 8000
- [ ] Desktop app launched
- [ ] Logged in successfully
- [ ] CSV uploaded
- [ ] Analysis displayed
- [ ] Charts rendered
- [ ] Export working
- [ ] Theme toggle working

---

## 🆘 Need Help?

### Quick Help
1. Check `QUICKSTART.md` for fast start
2. Review `SETUP_GUIDE.md` for detailed setup
3. See `FEATURES.md` for complete feature list

### Common Issues
- Backend not running → Start with `python manage.py runserver`
- Dependencies missing → Run `pip install -r requirements.txt`
- Port conflict → Change port in `api_client.py`

---

## 🎉 You're Ready!

The desktop app is now ready to use. Here's what to do next:

1. ✅ **Upload your data** - Press Ctrl+U
2. ✅ **Explore features** - Try all tabs
3. ✅ **Generate reports** - Export PDF/Excel
4. ✅ **Compare datasets** - Analyze trends
5. ✅ **Share insights** - Encrypted exports

---

## 📞 Support

For issues and questions:
- Check documentation files
- Review backend logs
- Verify backend is running
- Check Python version (3.9+)

---

## 🏆 Features at a Glance

| Feature | Status | Location |
|---------|--------|----------|
| Login/Signup | ✅ | Login screen |
| CSV Upload | ✅ | Ctrl+U or Upload button |
| Statistics | ✅ | Overview tab |
| AI Insights | ✅ | Overview tab |
| Data Table | ✅ | Data Table tab |
| Bar Chart | ✅ | Visualizations tab |
| Scatter Plot | ✅ | Visualizations tab |
| Pie Chart | ✅ | Visualizations tab |
| 3D Plot ⭐ | ✅ | Visualizations tab |
| History | ✅ | Left sidebar |
| Comparison | ✅ | Compare button |
| PDF Export | ✅ | Export tab |
| Excel Export | ✅ | Export tab |
| Theme Toggle | ✅ | Theme button |
| Profile | ✅ | Profile button |

---

**Ready to analyze? Launch the app and press Ctrl+U!** 🚀

**Desktop Application v1.0.0**
**Built with PyQt5 and ❤️ for Chemical Engineers**
