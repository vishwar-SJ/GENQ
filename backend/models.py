"""
GENQ SQLAlchemy ORM Models
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reports = relationship("GeneticReport", back_populates="user", cascade="all, delete-orphan")


class GeneticReport(Base):
    __tablename__ = "genetic_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    extraction_status = Column(String(50), default="pending")  # pending, success, failed
    snp_count = Column(Integer, default=0)

    user = relationship("User", back_populates="reports")
    disease_results = relationship("DiseaseRiskResult", back_populates="report", cascade="all, delete-orphan")
    drug_results = relationship("DrugResponseResult", back_populates="report", cascade="all, delete-orphan")


class DiseaseRiskResult(Base):
    __tablename__ = "disease_risk_results"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("genetic_reports.id"), nullable=False)
    disease_name = Column(String(100), nullable=False)
    risk_label = Column(String(50), nullable=False)  # Low, Average, Elevated, Carrier detected, etc.
    percentile = Column(Float, nullable=True)  # null for non-PRS diseases like Thalassemia
    raw_score = Column(Float, nullable=True)
    is_estimated = Column(String(10), default="false")  # "true" if population stats are estimated

    report = relationship("GeneticReport", back_populates="disease_results")


class DrugResponseResult(Base):
    __tablename__ = "drug_response_results"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("genetic_reports.id"), nullable=False)
    drug_name = Column(String(100), nullable=False)
    gene = Column(String(50), nullable=False)
    metabolizer_status = Column(String(100), nullable=False)  # Poor, Intermediate, Normal, Rapid, Insufficient data
    guidance_text = Column(Text, nullable=True)

    report = relationship("GeneticReport", back_populates="drug_results")


class OffspringReport(Base):
    __tablename__ = "offspring_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    disease_results = relationship("OffspringDiseaseRisk", back_populates="offspring_report", cascade="all, delete-orphan")


class OffspringDiseaseRisk(Base):
    __tablename__ = "offspring_disease_risks"

    id = Column(Integer, primary_key=True, index=True)
    offspring_report_id = Column(Integer, ForeignKey("offspring_reports.id"), nullable=False)
    disease_name = Column(String(100), nullable=False)
    risk_label = Column(String(50), nullable=False)
    probability_text = Column(String(100), nullable=False)
    is_polygenic = Column(String(10), default="false")
    percentile = Column(Float, nullable=True)

    offspring_report = relationship("OffspringReport", back_populates="disease_results")
