# Nirikshan - Smart Data Observation Platform

Nirikshan is an intelligent CSV analysis web application that helps you observe, audit, and analyze datasets instantly.
It performs automatic schema detection, data quality checks, anomaly detection, statistical summaries, and chart recommendations inside a clean, interactive dashboard.

## Home Page UI

![Nirikshan Home](frontend/Homepage%20UI/home.png)

---

## Live Website

[https://nirikshan-ten.vercel.app](https://nirikshan-ten.vercel.app)

---

## Live Backend

[https://nirikshan-pfxs.onrender.com](https://nirikshan-pfxs.onrender.com)

Health Check:
[https://nirikshan-pfxs.onrender.com/health](https://nirikshan-pfxs.onrender.com/health)

---

## Features

### Smart CSV Analysis
- Upload CSV and get instant analysis
- Auto-detect column types (numeric, categorical, date-like, text)
- Structured dashboard-ready response

### Data Quality Audit
- Missing values per column
- Duplicate row detection
- Dataset health score

### Statistical Summary
- Mean, min, max, total for numeric columns
- Range-oriented metrics for quick understanding

### Anomaly Detection
- Outlier detection using threshold logic
- Column-wise anomaly counts and highlights

### Smart Chart Suggestions
- Histogram for numeric data
- Bar chart for categorical data
- Category + numeric combo chart suggestions

### Insight Generation
- Missing data alerts
- Variability insights
- Dominant category patterns
- Anomaly summary notes

### Modern, Responsive UI
- Light / Dark mode toggle
- Responsive dashboard layout
- Collapsible chart sections and summary cards

---

## System Architecture

### Frontend (React + Vite + Chart.js)
- Handles CSV upload flow
- Renders summary cards, charts, anomalies, and insights
- Calls backend APIs via Axios

### Backend (FastAPI + Python)
- Accepts CSV uploads
- Performs schema detection, audit, stats, anomaly analysis
- Exposes REST endpoints

### Storage Layer
- In-memory Pandas DataFrame processing
- No database dependency

---

## Files Used

### Backend
- `backend/app/main.py`
- `backend/requirements.txt`

### Frontend
- `frontend/src/services/api.js`
- `frontend/src/components/*`
- `frontend/src/pages/*`
- `frontend/src/App.jsx`
- `frontend/src/main.jsx`

---

## How It Works (Short Overview)

1. User uploads CSV file
2. Frontend sends file to backend `/dashboard`
3. Backend parses and analyzes dataset
4. Backend returns summary, charts, insights, and anomalies
5. Frontend renders complete analysis dashboard

---

## Installation and Setup

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

## Deployment

### Backend (Render)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
- Framework Preset: `Vite`
- Root Directory: `frontend`
- Build Command: `vite build`
- Output Directory: `dist`

---

## Authors

- **Sujal Patil** - [GitHub](https://github.com/SujalPatil21)
- **Shreya Awari** - [GitHub](https://github.com/shreyaawari28)
- **Tejas Halvankar** - [GitHub](https://github.com/Tejas-H01)
- **Nihal Mishra** - [GitHub](https://github.com/NihalMishra3009)

---

## License

Built for academic and hackathon use.
