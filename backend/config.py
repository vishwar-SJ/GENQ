"""
GENQ Backend Configuration
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'genq.db'}")

# JWT Settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "genq-dev-secret-change-in-production-2026")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# File Upload
MAX_UPLOAD_SIZE_MB = 10
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
UPLOAD_TEMP_DIR = BASE_DIR / "temp_uploads"
UPLOAD_TEMP_DIR.mkdir(exist_ok=True)

# Data directories
SCORING_FILES_DIR = BASE_DIR / "data" / "scoring_files"
DRUG_LOOKUP_DIR = BASE_DIR / "data" / "drug_lookup"

# Minimum SNPs threshold for valid extraction
MIN_SNPS_THRESHOLD = 20

# Production mode flag
PRODUCTION = os.getenv("PRODUCTION", "false").lower() == "true"
