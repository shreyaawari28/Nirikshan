# ?? Nirikshan - Smart Data Observation Platform

Nirikshan is an intelligent CSV analysis web application that helps you observe, audit, and analyze datasets instantly.  
It performs automatic schema detection, data quality checks, anomaly detection, statistical summaries, and chart recommendations inside a clean, interactive dashboard.

---
 
## ?? Project Video - Click To Open

[![Project Demo](Project.png)](https://www.youtube.com/watch?v=sTBTgqAxueU)

---

---

## ?? Live Website

[https://nirikshan-ten.vercel.app](https://nirikshan-ten.vercel.app)

---

## ?? Live Backend

[https://nirikshan-pfxs.onrender.com](https://nirikshan-pfxs.onrender.com)

Health Check:  
[https://nirikshan-pfxs.onrender.com/health](https://nirikshan-pfxs.onrender.com/health)

---

## ? Features
 
### ?? CSV Upload and Instant Analysis
- Upload structured CSV files directly from UI
- Parse and process data without predefined schema
- Get dashboard-ready output instantly

### ?? Automatic Schema Detection
- Detects numeric, categorical, date-like, and text columns
- Reports dataset shape (rows and columns)
- Generates analysis-ready metadata

### ?? Data Quality Audit
- Missing values per column
- Duplicate row count
- Overall health score based on completeness

### ?? Statistical Analysis
- Numeric column stats (mean, min, max, total)
- Distribution-friendly summaries for charting
- Supports mixed-type CSV datasets

### ?? Anomaly Detection
- Detects outliers using threshold-based logic
- Reports anomaly count, values, and indices
- Highlights anomaly-prone columns in dashboard

### ?? Smart Chart Recommendations
- Histogram for numeric columns
- Bar chart for categorical columns
- Combination chart suggestions for category + numeric pairs

### ?? Insight Generation
- High missing-data alerts
- Variability and spread observations
- Dominant categorical pattern insights
- Anomaly summary insights

### ?? Modern, Responsive UI
- Light / Dark mode toggle
- Responsive dashboard layout
- Collapsible chart sections and summary cards
- Smooth loading and empty-state handling

---

## ??? System Architecture

### **Frontend (React + Vite + Chart.js)**
- Handles CSV upload flow
- Renders summary cards, charts, anomalies, and insights
- Calls backend APIs via Axios
- Provides responsive and themed dashboard UI

### **Backend (FastAPI + Python)**
- Accepts CSV uploads
- Performs schema detection, audit, stats, and anomaly analysis
- Generates dashboard response payload
- Exposes REST endpoints for health and analysis

### **Storage Layer**
- In-memory processing via Pandas DataFrame
- No database dependency
- File uploads handled through multipart form data

---

## ?? Files Used

### **Backend**
- `backend/app/main.py`
- `backend/requirements.txt`

### **Frontend**
- `frontend/src/services/api.js`
- `frontend/src/components/*`
- `frontend/src/pages/*`
- `frontend/src/App.jsx`
- `frontend/src/main.jsx`

---

## ?? How It Works (Short Overview)

1. User uploads CSV file
2. Frontend sends file to backend `/dashboard` endpoint
3. Backend parses and analyzes dataset
4. Backend returns summary, charts, insights, and anomalies
5. Frontend renders complete analysis dashboard

---

## ?? Installation & Setup

```bash
# Clone repository
git clone https://github.com/NihalMishra3009/Nirikshan.git
cd Nirikshan
```

```bash
# Backend setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```bash
# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

---

## ?? Deployment

### **Backend (Render)**
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### **Frontend (Vercel)**
- Framework Preset: `Vite`
- Root Directory: `frontend`
- Build Command: `vite build`
- Output Directory: `dist`

---

## ????? Authors

- **Shreya Awari** - [GitHub](https://github.com/shreyaawari28)
- **Nihal Mishra** - [GitHub](https://github.com/NihalMishra3009)
- **Tejas Halvankar** – [GitHub](https://github.com/Tejas-H01)
- **Sujal Patil** – [GitHub](https://github.com/SujalPatil21)  
---

## ?? License

Built for academic and hackathon use.
