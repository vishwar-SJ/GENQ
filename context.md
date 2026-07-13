# GENQ — Development Context

> This file tracks the current state of AI-assisted development. Updated after each phase.

## Current Status: Phase 8-10 Complete — Full Stack Built

**Last Updated:** 2026-07-13

---

## Tech Stack Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend framework | React (Vite) | Fast dev server, modern tooling, as specified |
| CSS framework | Tailwind CSS v4 | Using @tailwindcss/vite plugin, flat design system |
| Charts | Recharts | Percentile gauge visualizations (PieChart donut) |
| HTTP client | Axios | JWT interceptor support |
| Backend framework | FastAPI | Async support, Pydantic validation, as specified |
| PDF parsing | pdfplumber | Better table extraction than PyMuPDF |
| Database | SQLite (dev) | Zero config for development |
| ORM | SQLAlchemy | As specified |
| Auth | JWT (python-jose) + bcrypt | Stateless auth, as specified |

## Architecture Overview

```
User → React SPA → Axios (JWT) → FastAPI Backend
                                      ├── Auth (signup/login/JWT)
                                      ├── PDF Parser (pdfplumber + regex)
                                      ├── Disease Risk Engine (PRS scoring)
                                      ├── Drug Response Engine (star allele lookup)
                                      └── SQLite DB (users, reports, results)
```

## Data Pipeline

```
PDF Upload → Text Extraction → Regex rsID/genotype parsing
                                    ├── PRS Calculation → z-score → percentile → risk label
                                    └── Star Allele Lookup → metabolizer status → guidance
```

## Scoring Data

- **Disease Risk**: 5 diseases with static CSV scoring files (PGS Catalog format)
  - Type 2 Diabetes (40 SNPs), Coronary Artery Disease (35 SNPs), Breast Cancer (30 SNPs), Alzheimer's (25 SNPs), Thalassemia (5 variants)
  - Uses synthetic weights on real rsIDs (replace with actual PGS files for production)
- **Drug Response**: 3 drug-gene pairs with JSON lookup tables (CPIC format)
  - Clopidogrel/CYP2C19 (3 rsIDs), Isoniazid/NAT2 (3 rsIDs), Warfarin/CYP2C9+VKORC1 (3 rsIDs)

## Build Progress

### ✅ Completed
- Phase 1: Scaffold & Documentation (README.md, context.md)
- Phase 2: Backend Foundation (FastAPI, config, database, models, schemas)
- Phase 3: Authentication (JWT signup/login, password hashing, protected routes)
- Phase 4: PDF Parsing Service (regex + table extraction, validation)
- Phase 5: Disease Risk Engine (PRS calculation, percentile conversion, Thalassemia carrier detection)
- Phase 6: Drug Response Engine (CYP2C19/NAT2/CYP2C9+VKORC1 diplotyping)
- Phase 7: Report Upload Router (combined PDF → analysis → store → response)
- Phase 8: Frontend Scaffold (Vite + React + Tailwind v4 + Recharts)
- Phase 9: Frontend Auth Pages (Landing, Login, Signup, AuthContext, Navbar)
- Phase 10: Dashboard & Results UI (Upload, DiseaseRiskCard, DrugResponseCard, RiskGauge, DisclaimerBanner)

### 🔄 In Progress
- Backend pip install and server verification

### ⏳ Pending
- End-to-end testing with sample PDF
- Generate sample PDF for testing

## File Structure (Complete)

```
GENQ/
├── README.md
├── context.md
├── frontend/
│   ├── index.html (with SEO, Inter font, favicon)
│   ├── vite.config.js (React + Tailwind v4 + API proxy)
│   ├── public/favicon.svg
│   └── src/
│       ├── main.jsx
│       ├── App.jsx (BrowserRouter, routes, ProtectedRoute)
│       ├── index.css (Tailwind v4, design tokens, utilities, animations)
│       ├── api/axios.js (JWT interceptor)
│       ├── context/AuthContext.jsx
│       ├── pages/Landing.jsx, Login.jsx, Signup.jsx, Dashboard.jsx
│       └── components/Navbar.jsx, UploadSection.jsx, DiseaseRiskCard.jsx,
│                       DrugResponseCard.jsx, RiskGauge.jsx, DisclaimerBanner.jsx
├── backend/
│   ├── main.py (FastAPI app with CORS, routers)
│   ├── config.py, database.py, models.py, schemas.py
│   ├── auth/ (router.py, utils.py, dependencies.py)
│   ├── routers/report.py (upload, analyze, results)
│   ├── services/ (pdf_parser.py, disease_risk.py, drug_response.py)
│   └── data/
│       ├── scoring_files/ (5 CSVs)
│       └── drug_lookup/ (3 JSONs)
└── scripts/generate_sample_pdf.py
```

## Security Implementation

- ✅ Raw PDFs deleted after extraction (in report router finally block)
- ✅ Genetic data only logged when PRODUCTION=false
- ✅ All API routes except auth require valid JWT (HTTPBearer dependency)
- ✅ Passwords hashed with bcrypt (passlib)
- ✅ Consent checkbox required before upload (frontend)
- ✅ Disclaimer banners on dashboard (top and bottom)
- ✅ Max file upload size: 10MB

## Known Limitations

- Scoring files use synthetic weights (not actual PGS Catalog data)
- Drug response uses simplified star allele logic (production would need full diplotype resolution)
- No OAuth/social login (stretch feature)
- SQLite for development only (PostgreSQL for production)
- Single-chunk frontend bundle (could be code-split for production)
