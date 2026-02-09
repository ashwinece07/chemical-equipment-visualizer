# Chemical Equipment Visualizer - Desktop Application

A native desktop application built with PyQt5 for chemical equipment data visualization and analysis.

## Features

✅ **JWT Authentication** - Secure login/signup
✅ **CSV Upload** - Drag & drop with Ctrl+U shortcut
✅ **Real-time Analysis** - Progress tracking
✅ **AI-Powered Insights** - Google Gemini integration
✅ **Interactive Visualizations** - 2D and 3D plots with Matplotlib
✅ **Dataset Comparison** - Side-by-side analysis
✅ **Upload History** - Last 10 uploads
✅ **Password-Protected Exports** - PDF & Excel reports
✅ **Dark/Light Theme** - Toggle with persistence
✅ **User Profile** - View statistics

## Installation

### Prerequisites
- Python 3.9+
- Backend server running on http://127.0.0.1:8000

### Setup

```bash
# Navigate to desktop app directory
cd frontend-desktop

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

## Usage

### 1. Login/Signup
- Launch the application
- Login with existing credentials or create a new account

### 2. Upload Data
- Click "📁 Upload CSV (Ctrl+U)" or press Ctrl+U
- Select your CSV file
- Wait for analysis to complete

### 3. View Analysis
- **Overview Tab**: Statistics and AI insights
- **Data Table Tab**: Raw data view
- **Visualizations Tab**: Interactive charts
  - Bar Chart: Equipment distribution
  - Scatter Plot: Parameter correlations
  - Pie Chart: Health score distribution
  - 3D Plot: Interactive 3D visualization
- **Export Tab**: Generate reports

### 4. Compare Datasets
- Select 2 files from history
- Click "⚖️ Compare Selected"
- View comparison results

### 5. Export Reports
- Navigate to Export tab
- Click "📄 Export PDF Report" or "📊 Export Excel Report"
- Enter password for encryption
- Choose save location

### 6. Theme Toggle
- Click "🌓 Toggle Theme" to switch between dark/light mode
- Theme preference is saved automatically

## Keyboard Shortcuts

- **Ctrl+U**: Quick file upload
- **Enter**: Submit login/signup form

## Architecture

```
frontend-desktop/
├── src/
│   ├── main.py              # Application entry point
│   ├── api_client.py        # Backend API communication
│   ├── views/
│   │   ├── login_view.py    # Authentication UI
│   │   └── dashboard_view.py # Main dashboard
│   └── utils/
│       └── theme_manager.py  # Theme management
├── requirements.txt
└── README.md
```

## Technology Stack

- **PyQt5** - GUI framework
- **Matplotlib** - 2D/3D plotting
- **Requests** - HTTP client
- **Pandas** - Data handling
- **NumPy** - Numerical operations

## Configuration

The application connects to the backend at `http://127.0.0.1:8000/api/` by default.

To change the API URL, modify `api_client.py`:

```python
def __init__(self, base_url: str = "http://your-backend-url/api/"):
```

## Troubleshooting

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Connection Refused
- Ensure backend server is running
- Check backend URL in api_client.py

### Theme Not Persisting
- Check write permissions for QSettings storage
- Windows: Registry
- macOS/Linux: ~/.config/ChemicalVisualizer/

## Building Executable

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "ChemicalVisualizer" src/main.py

# Executable will be in dist/ folder
```

## System Requirements

- **OS**: Windows 10/11, macOS 12+, Ubuntu 20.04+
- **RAM**: 4GB minimum, 8GB recommended
- **Display**: 1366x768 minimum resolution

## License

MIT License - see main project LICENSE file

## Support

For issues and questions, refer to the main project repository.

---

**Built with ❤️ for Chemical Engineers**
