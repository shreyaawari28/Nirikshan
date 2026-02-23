# 🚀 Nirikshan – Smart Data Observation Platform

> Observe. Analyze. Decide.

Nirikshan is an automated data intelligence platform that transforms raw CSV files into structured dashboards with built-in data auditing, anomaly detection, statistical analysis, and prioritized insights — without requiring manual configuration or technical expertise.

---

## 📌 Problem Statement

Traditional data tools:

- Require manual chart configuration  
- Demand technical expertise  
- Do not automatically audit data quality  
- Do not prioritize critical insights  
- Delay decision-making due to setup complexity  

There remains a significant gap between raw data and actionable intelligence.

---

## 💡 Our Solution

Nirikshan introduces an **Automated Insight & Data Audit Engine** that:

- Automatically detects schema  
- Performs built-in data quality auditing  
- Computes statistical summaries  
- Detects anomalies using standard deviation logic  
- Identifies trends and growth patterns  
- Recommends optimal chart types  
- Generates ranked, prioritized insights  

Upload → Analyze → Decide.

---

## 🏗️ System Architecture

```
CSV Upload
    ↓
FastAPI Analysis Engine
    ↓
Insight & Chart Recommendation Engine
    ↓
React Dashboard
```

---

## 🛠️ Technology Stack

### Frontend
- React + Vite  
- Recharts  
- Axios  
- jsPDF + html2canvas  

### Backend
- FastAPI  
- Pandas  
- NumPy  
- Modular service-based architecture  

### API
- Endpoint: `POST /analyze`  
- Request type: `multipart/form-data`  
- Response: Structured JSON analytics  

---

## 🔎 Core Features

### 📂 CSV Upload
Upload any structured CSV file without predefined schema.

### 🔍 Automatic Schema Detection
Detects:
- Numeric columns  
- Categorical columns  
- Datetime columns  
- Total rows and columns  

### 🧪 Data Quality Audit
Checks:
- Missing values  
- Duplicate rows  
- Data completeness percentage  

### 📊 Statistical Analysis
Computes:
- Mean  
- Median  
- Standard deviation  
- Min / Max  
- Totals  

### 🚨 Anomaly Detection
Flags outliers using statistical thresholds.

### 📈 Pattern Detection
Identifies:
- Upward/downward trends  
- Growth percentages  
- Top contributors  
- Correlations  

### 📊 Smart Chart Recommendation
Automatically selects:
- Line chart (time + numeric)  
- Bar chart (category + numeric)  
- Histogram (numeric only)  

### 🧠 Insight Generation
Prioritizes insights by impact.

### 📄 PDF Export
Download a full analysis report in one click.

---

## 📂 Project Structure

```
Nirikshan/
│
├── backend/
│   ├── main.py
│   ├── services/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── components/
│   └── package.json
│
└── README.md
```

---

## 🚀 How to Run

### Backend

```bash
cd backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend URL:
```
http://localhost:8000
```

API Docs:
```
http://localhost:8000/docs
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:
```
http://localhost:5173
```

---

## 🏆 Hackathon Alignment

| Criteria | Implementation |
|----------|---------------|
| Problem Understanding | Eliminates manual bottlenecks |
| Technical Implementation | FastAPI + React modular design |
| Innovation | Observes data before visualizing |
| Scalability | Stateless processing architecture |
| UI/UX | Clean dashboard with smart flow |
| Impact | Government, education, SMB use |
| Code Quality | Service-layer separation |

---

## 🏁 Conclusion

Nirikshan transforms raw datasets into decision-ready intelligence instantly.

It does not just visualize data.

It observes, audits, analyzes, and explains it.

---

## 👥 Team

Frontend Development  
Backend Development  
System Architecture  

---

## 📜 License

Developed for academic and hackathon purposes.