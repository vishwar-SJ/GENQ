# GENQ — Genetic Disease Risk & Drug Response Web App

GENQ is a full-stack web application that analyzes genetic report PDFs to calculate disease risk scores and drug response predictions.

## Features

- **PDF Upload & Parsing** — Upload genetic reports (PDF), extract rsID + genotype data via regex and table extraction
- **Disease Risk Scoring** — Polygenic Risk Score (PRS) calculations for Type 2 Diabetes, Coronary Artery Disease, Breast Cancer, Alzheimer's Disease, and Thalassemia carrier detection
- **Drug Response Prediction** — Pharmacogenomic metabolizer status for Clopidogrel (CYP2C19), Isoniazid (NAT2), and Warfarin (CYP2C9/VKORC1)
- **JWT Authentication** — Secure email + password signup/login
- **Privacy-First** — Raw PDFs are deleted immediately after extraction; only structured results are stored

## Tech Stack

| Layer          | Technology                              |
|----------------|----------------------------------------|
| Frontend       | React (Vite), Tailwind CSS v3, Recharts |
| Backend        | Python, FastAPI                         |
| PDF Parsing    | pdfplumber                              |
| Data Processing| Pandas, SciPy                           |
| Database       | SQLite (dev) / PostgreSQL (prod)        |
| ORM            | SQLAlchemy                              |
| Auth           | JWT (python-jose), bcrypt (passlib)     |

## Project Structure

```
GENQ/
├── frontend/          # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/     # Landing, Login, Signup, Dashboard
│   │   ├── components/# Navbar, Cards, Charts, Upload
│   │   ├── context/   # AuthContext
│   │   └── api/       # Axios instance
│   └── ...
├── backend/
│   ├── main.py        # FastAPI entry point
│   ├── auth/          # JWT auth routes & utils
│   ├── routers/       # API route handlers
│   ├── services/      # PDF parser, Disease Risk, Drug Response engines
│   ├── data/          # Static scoring files & drug lookup tables
│   └── ...
└── scripts/           # Utility scripts (sample PDF generator)
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173` and proxies API calls to `http://localhost:8000`.

## API Endpoints

| Method | Endpoint                    | Auth | Description                    |
|--------|-----------------------------|------|--------------------------------|
| POST   | `/api/auth/signup`          | No   | Create account                 |
| POST   | `/api/auth/login`           | No   | Login, receive JWT             |
| POST   | `/api/upload-report`        | Yes  | Upload PDF, get full analysis  |
| POST   | `/api/analyze/disease-risk` | Yes  | Run disease risk engine only   |
| POST   | `/api/analyze/drug-response`| Yes  | Run drug response engine only  |
| GET    | `/api/results/latest`       | Yes  | Get latest results for user    |

## Disclaimer

> **This application provides genetic risk information for educational purposes only. It is NOT a medical diagnosis. Always consult a doctor or genetic counselor for medical decisions.**

## License

MIT
