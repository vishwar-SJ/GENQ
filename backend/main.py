"""
GENQ Backend — FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
from auth.router import router as auth_router
from routers.report import router as report_router
from routers.chat import router as chat_router

app = FastAPI(
    title="GENQ API",
    description="Genetic Disease Risk & Drug Response Analysis API",
    version="2.0.0",
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(report_router)
app.include_router(chat_router)


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_tables()


@app.get("/")
def root():
    return {
        "app": "GENQ",
        "version": "1.0.0",
        "description": "Genetic Disease Risk & Drug Response Analysis API",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
