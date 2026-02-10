#  POTASH - Chemical Equipment Parameter Visualizer

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![React](https://img.shields.io/badge/React-19.2.0-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10-orange.svg)

---

##  Live Demo

### **[https://ashwin-potash.duckdns.org/](https://ashwin-potash.duckdns.org/)**

### Video Demo & Documentation
- **Video Demo**: [Google Drive Link](#) _(Add your drive link here)_
- **Full Documentation**: [Google Drive Link](#) _(Add your drive link here)_

---

##  What is POTASH?

POTASH is a **hybrid web + desktop application** for chemical engineers to visualize, analyze, and monitor equipment parameters in real-time. Upload CSV files containing equipment data and get instant AI-powered insights, interactive charts, and detailed reports.

---

##  What It Does

-  **Analyzes chemical equipment data** from CSV files
-  **Generates AI-powered insights** using Google Gemini
-  **Creates interactive visualizations** (7 chart types)
-  **Exports encrypted PDF/Excel reports**
-  **Compares multiple datasets** side-by-side
-  **Secure authentication** with JWT tokens
-  **Dark/Light theme** support

---

##  Features

### Web Application
- JWT Authentication (Login/Signup)
- CSV Upload with drag & drop
- Real-time data analysis
- AI-powered insights (Google Gemini)
- Interactive charts (Bar, Scatter, Pie, Heatmap, Box Plot, Histogram)
- Dataset comparison
- Password-protected exports (PDF/Excel)
- Upload history (last 10 files)
- User profile management
- Dark/Light theme toggle

### Desktop Application
- All web features +
- **3D Interactive Visualizations**
- Native desktop performance
- Offline data viewing
- Local file management
- Cross-platform (Windows, macOS, Linux)

---
<img width="1887" height="970" alt="image" src="https://github.com/user-attachments/assets/02b32e62-59b6-47e9-be04-511ad9e0aba3" />
<img width="1399" height="933" alt="image" src="https://github.com/user-attachments/assets/0815ef53-34c6-489b-b1b9-a1c8bcfa1028" />
<img width="1390" height="918" alt="image" src="https://github.com/user-attachments/assets/8c473dbf-a244-4b8d-8e29-96b9856a1452" />

##  Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/ashwinece07/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Web App Setup
```bash
cd frontend-web
npm install
npm run dev
# Open http://localhost:5173
```

### 4. Desktop App Setup
```bash
cd frontend-desktop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

---

##  Project Structure

```
chemical-equipment-visualizer/
├── backend/              # Django REST API
│   ├── api/             # API endpoints
│   ├── backend/         # Django settings
│   └── media/           # Uploaded files
├── frontend-web/         # React web app
│   ├── src/             # React components
│   └── public/          # Static assets
├── frontend-desktop/     # PyQt5 desktop app
│   └── src/             # Desktop UI
└── sample_equipment_data.csv
```

---

##  Tech Stack

**Backend:** Django, Django REST Framework, Pandas, NumPy, Matplotlib, Google Gemini AI

**Web Frontend:** React, Vite, Chart.js, Tailwind CSS, Axios

**Desktop Frontend:** PyQt5, Matplotlib, Requests

---

##  Sample Data Format

```csv
Equipment_Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,85.2
Reactor-A1,Reactor,200.0,45.8,120.5
```

---

cal Engineers | POTASH v1.0.0**
