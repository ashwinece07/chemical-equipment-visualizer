# Desktop Application Setup Guide

## Quick Start

### Option 1: Using Batch File (Windows - Easiest)

1. **Ensure Backend is Running**
   ```bash
   # In a separate terminal
   cd backend
   python manage.py runserver
   ```

2. **Launch Desktop App**
   - Double-click `START_DESKTOP.bat` in the project root
   - The script will automatically:
     - Create virtual environment
     - Install dependencies
     - Launch the application

### Option 2: Manual Setup

1. **Navigate to Desktop Directory**
   ```bash
   cd frontend-desktop
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Application**
   ```bash
   python src/main.py
   ```

## First Time Usage

1. **Start Backend Server** (if not already running)
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Launch Desktop App**
   - Use START_DESKTOP.bat or manual method above

3. **Create Account or Login**
   - Click "Sign Up" tab to create new account
   - Or use existing credentials in "Login" tab

4. **Upload CSV File**
   - Click "📁 Upload CSV (Ctrl+U)" button
   - Or press Ctrl+U keyboard shortcut
   - Select your CSV file
   - Wait for analysis to complete

5. **Explore Features**
   - View statistics in Overview tab
   - Browse data in Data Table tab
   - Visualize with charts in Visualizations tab
   - Export reports in Export tab

## Features Overview

### 🔐 Authentication
- Secure JWT-based login/signup
- Session persistence
- Profile management

### 📊 Data Analysis
- CSV file upload (up to 10MB)
- Real-time statistical analysis
- AI-powered insights via Google Gemini
- Health score calculation
- Outlier detection

### 📈 Visualizations
- **Bar Chart**: Equipment type distribution
- **Scatter Plot**: Parameter correlations
- **Pie Chart**: Health score breakdown
- **3D Plot**: Interactive 3D parameter visualization
  - Mouse rotation
  - Zoom controls
  - Multi-parameter view

### 📁 History Management
- Last 10 uploads displayed
- Quick re-analysis
- Dataset comparison
- Delete functionality

### 📄 Export Options
- **PDF Reports**: Password-protected professional reports
- **Excel Reports**: Multi-sheet encrypted workbooks
- Custom password protection

### 🎨 Theme System
- Light mode (default)
- Dark mode
- Toggle button
- Persistent preference

### ⌨️ Keyboard Shortcuts
- **Ctrl+U**: Quick file upload
- **Enter**: Submit forms

## Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### "Connection refused" error
- Ensure backend is running on http://127.0.0.1:8000
- Check if port 8000 is available
- Verify firewall settings

### Charts not displaying
```bash
pip install --upgrade matplotlib
```

### Theme not saving
- Check write permissions
- Windows: Registry access required
- macOS/Linux: ~/.config/ directory access

### PyQt5 installation issues

**Windows:**
```bash
pip install PyQt5 --no-cache-dir
```

**macOS:**
```bash
brew install pyqt5
pip install PyQt5
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyqt5
pip install PyQt5
```

## Building Standalone Executable

### Windows Executable

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build Executable**
   ```bash
   cd frontend-desktop
   pyinstaller --onefile --windowed --name "ChemicalVisualizer" --icon=src/assets/icon.ico src/main.py
   ```

3. **Find Executable**
   - Located in `frontend-desktop/dist/ChemicalVisualizer.exe`
   - Distribute this file to users

### macOS Application

```bash
pyinstaller --onefile --windowed --name "ChemicalVisualizer" src/main.py
# Creates .app bundle in dist/
```

### Linux Binary

```bash
pyinstaller --onefile --name "ChemicalVisualizer" src/main.py
# Creates binary in dist/
```

## System Requirements

### Minimum
- **OS**: Windows 10, macOS 12, Ubuntu 20.04
- **RAM**: 4GB
- **Display**: 1366x768
- **Python**: 3.9+

### Recommended
- **OS**: Windows 11, macOS 13+, Ubuntu 22.04
- **RAM**: 8GB
- **Display**: 1920x1080
- **Python**: 3.11+

## Configuration

### Change Backend URL

Edit `src/api_client.py`:

```python
class APIClient:
    def __init__(self, base_url: str = "http://your-server:8000/api/"):
        # ...
```

### Customize Theme Colors

Edit `src/utils/theme_manager.py`:

```python
# Modify LIGHT_THEME or DARK_THEME constants
```

## Development

### Project Structure
```
frontend-desktop/
├── src/
│   ├── main.py              # Entry point
│   ├── api_client.py        # API communication
│   ├── views/
│   │   ├── login_view.py    # Login/Signup UI
│   │   └── dashboard_view.py # Main dashboard
│   └── utils/
│       └── theme_manager.py  # Theme management
├── requirements.txt
└── README.md
```

### Adding New Features

1. **New View**: Create in `src/views/`
2. **New Utility**: Create in `src/utils/`
3. **Update Main**: Import and integrate in `src/main.py`

### Testing

```bash
# Run application in debug mode
python src/main.py
```

## Performance Tips

1. **Large Files**: Files >5MB may take longer to process
2. **3D Plots**: May be slower on older hardware
3. **Memory**: Close unused tabs to free memory
4. **Network**: Ensure stable connection to backend

## Security Notes

1. **Passwords**: Never hardcode passwords
2. **Tokens**: JWT tokens stored in memory only
3. **Exports**: Always use strong passwords for reports
4. **Updates**: Keep dependencies updated

## Support

For issues:
1. Check this guide
2. Review main project README
3. Check backend logs
4. Open GitHub issue

## License

MIT License - See main project LICENSE

---

**Desktop App Version 1.0.0**
**Built with PyQt5 and ❤️**
