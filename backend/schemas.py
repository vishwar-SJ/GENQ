"""
GENQ Pydantic Schemas — Request/Response validation models
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ─── Auth Schemas ────────────────────────────────────────────
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str
    username: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Genotype Data Schemas ───────────────────────────────────
class GenotypeEntry(BaseModel):
    rsid: str
    genotype: str


class ExtractionResult(BaseModel):
    snp_count: int
    genotypes: list[GenotypeEntry]


# ─── Disease Risk Schemas ────────────────────────────────────
class DiseaseRiskOut(BaseModel):
    disease_name: str
    risk_label: str
    percentile: Optional[float] = None
    raw_score: Optional[float] = None
    is_estimated: str = "false"

    class Config:
        from_attributes = True


# ─── Drug Response Schemas ───────────────────────────────────
class DrugResponseOut(BaseModel):
    drug_name: str
    gene: str
    metabolizer_status: str
    guidance_text: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Combined Report Response ────────────────────────────────
class ReportResponse(BaseModel):
    report_id: int
    uploaded_at: datetime
    snp_count: int
    disease_risks: list[DiseaseRiskOut]
    drug_responses: list[DrugResponseOut]
    disclaimer: str = (
        "This is genetic risk information, not a medical diagnosis. "
        "Please consult a doctor or genetic counselor."
    )


# ─── Chat Schemas ────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    report_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    sections: Optional[list[dict]] = None


# ─── Offspring Schemas ───────────────────────────────────────
class OffspringDiseaseRiskOut(BaseModel):
    disease_name: str
    risk_label: str
    probability_text: str
    is_polygenic: str = "false"
    percentile: Optional[float] = None

    class Config:
        from_attributes = True


class OffspringReportResponse(BaseModel):
    id: int
    created_at: datetime
    disease_risks: list[OffspringDiseaseRiskOut]
