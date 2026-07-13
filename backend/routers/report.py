"""
GENQ Report Router — PDF upload, analysis, and results retrieval endpoints.
"""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, GeneticReport, DiseaseRiskResult, DrugResponseResult, OffspringReport, OffspringDiseaseRisk
from schemas import ReportResponse, DiseaseRiskOut, DrugResponseOut, OffspringReportResponse, OffspringDiseaseRiskOut
from auth.dependencies import get_current_user
from services.pdf_parser import extract_genotypes_from_pdf
from services.disease_risk import analyze_disease_risk
from services.offspring_risk import analyze_offspring_risk
from services.drug_response import analyze_drug_response
from config import MAX_UPLOAD_SIZE_BYTES, UPLOAD_TEMP_DIR, PRODUCTION

router = APIRouter(prefix="/api", tags=["Reports"])


@router.post("/upload-report", response_model=ReportResponse)
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a genetic report PDF, extract genotypes, run disease risk
    and drug response analyses, store results, and return combined response.
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted.",
        )

    # Read file content and check size
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the maximum limit of {MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB.",
        )

    # Save temporarily for processing
    temp_filename = f"{uuid.uuid4().hex}.pdf"
    temp_path = UPLOAD_TEMP_DIR / temp_filename

    try:
        with open(temp_path, "wb") as f:
            f.write(content)

        # Step 1: Extract genotypes from PDF
        try:
            genotype_list = extract_genotypes_from_pdf(str(temp_path))
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )

        # Create report record
        report = GeneticReport(
            user_id=current_user.id,
            extraction_status="success",
            snp_count=len(genotype_list),
        )
        db.add(report)
        db.flush()  # Get report.id before adding results

        # Step 2: Run disease risk analysis
        disease_results = analyze_disease_risk(genotype_list)
        for dr in disease_results:
            db_result = DiseaseRiskResult(
                report_id=report.id,
                disease_name=dr["disease_name"],
                risk_label=dr["risk_label"],
                percentile=dr.get("percentile"),
                raw_score=dr.get("raw_score"),
                is_estimated=dr.get("is_estimated", "false"),
            )
            db.add(db_result)

        # Step 3: Run drug response analysis
        drug_results = analyze_drug_response(genotype_list)
        for dg in drug_results:
            db_result = DrugResponseResult(
                report_id=report.id,
                drug_name=dg["drug_name"],
                gene=dg["gene"],
                metabolizer_status=dg["metabolizer_status"],
                guidance_text=dg.get("guidance_text"),
            )
            db.add(db_result)

        db.commit()
        db.refresh(report)

        # Build response
        return ReportResponse(
            report_id=report.id,
            uploaded_at=report.uploaded_at,
            snp_count=report.snp_count,
            disease_risks=[DiseaseRiskOut(**dr) for dr in disease_results],
            drug_responses=[DrugResponseOut(**dg) for dg in drug_results],
        )

    finally:
        # ALWAYS delete the raw PDF — privacy requirement
        if temp_path.exists():
            os.remove(temp_path)
            if not PRODUCTION:
                print(f"Deleted temporary PDF: {temp_filename}")


@router.post("/analyze/disease-risk")
async def analyze_disease_risk_endpoint(
    genotypes: list[dict],
    current_user: User = Depends(get_current_user),
):
    """Run disease risk analysis on provided genotype data (without PDF upload)."""
    results = analyze_disease_risk(genotypes)
    return {
        "disease_risks": results,
        "disclaimer": (
            "This is genetic risk information, not a medical diagnosis. "
            "Please consult a doctor or genetic counselor."
        ),
    }


@router.post("/analyze/drug-response")
async def analyze_drug_response_endpoint(
    genotypes: list[dict],
    current_user: User = Depends(get_current_user),
):
    """Run drug response analysis on provided genotype data (without PDF upload)."""
    results = analyze_drug_response(genotypes)
    return {
        "drug_responses": results,
        "disclaimer": (
            "This is genetic risk information, not a medical diagnosis. "
            "Please consult a doctor or genetic counselor."
        ),
    }


@router.get("/results/latest", response_model=ReportResponse)
async def get_latest_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the most recent analysis results for the current user."""
    report = (
        db.query(GeneticReport)
        .filter(GeneticReport.user_id == current_user.id)
        .order_by(GeneticReport.uploaded_at.desc())
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No analysis results found. Please upload a genetic report first.",
        )

    return ReportResponse(
        report_id=report.id,
        uploaded_at=report.uploaded_at,
        snp_count=report.snp_count,
        disease_risks=[
            DiseaseRiskOut.model_validate(dr) for dr in report.disease_results
        ],
        drug_responses=[
            DrugResponseOut.model_validate(dg) for dg in report.drug_results
        ],
    )


@router.get("/results/{report_id}", response_model=ReportResponse)
async def get_results_by_id(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get analysis results by report ID (must belong to current user)."""
    report = (
        db.query(GeneticReport)
        .filter(
            GeneticReport.id == report_id,
            GeneticReport.user_id == current_user.id,
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    return ReportResponse(
        report_id=report.id,
        uploaded_at=report.uploaded_at,
        snp_count=report.snp_count,
        disease_risks=[
            DiseaseRiskOut.model_validate(dr) for dr in report.disease_results
        ],
        drug_responses=[
            DrugResponseOut.model_validate(dg) for dg in report.drug_results
        ],
    )


@router.post("/upload-offspring", response_model=OffspringReportResponse)
async def upload_offspring_report(
    mother_file: UploadFile = File(...),
    father_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload two genetic report PDFs (mother and father), extract genotypes, 
    run offspring disease risk analyses, store results, and return combined response.
    """
    # Validate file type
    for file in [mother_file, father_file]:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are accepted for both parents.",
            )

    # Temporary saving and extraction for both files
    mom_temp_filename = f"{uuid.uuid4().hex}_mom.pdf"
    dad_temp_filename = f"{uuid.uuid4().hex}_dad.pdf"
    mom_temp_path = UPLOAD_TEMP_DIR / mom_temp_filename
    dad_temp_path = UPLOAD_TEMP_DIR / dad_temp_filename

    try:
        # Save Mother PDF
        with open(mom_temp_path, "wb") as f:
            f.write(await mother_file.read())
        
        # Save Father PDF
        with open(dad_temp_path, "wb") as f:
            f.write(await father_file.read())

        # Extract Genotypes
        try:
            mom_genotypes = extract_genotypes_from_pdf(str(mom_temp_path))
            dad_genotypes = extract_genotypes_from_pdf(str(dad_temp_path))
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
            
        # Convert list of dicts to dicts mapping rsid->genotype
        mom_dict = {g["rsid"].lower(): g["genotype"] for g in mom_genotypes}
        dad_dict = {g["rsid"].lower(): g["genotype"] for g in dad_genotypes}

        # Create offspring report record
        offspring_report = OffspringReport(
            user_id=current_user.id
        )
        db.add(offspring_report)
        db.flush()

        # Run offspring risk analysis
        offspring_results = analyze_offspring_risk(mom_dict, dad_dict)
        
        for dr in offspring_results:
            db_result = OffspringDiseaseRisk(
                offspring_report_id=offspring_report.id,
                disease_name=dr["disease_name"],
                risk_label=dr["risk_label"],
                probability_text=dr["probability_text"],
                is_polygenic=dr.get("is_polygenic", "false"),
                percentile=dr.get("percentile")
            )
            db.add(db_result)

        db.commit()
        db.refresh(offspring_report)

        return OffspringReportResponse(
            id=offspring_report.id,
            created_at=offspring_report.created_at,
            disease_risks=[OffspringDiseaseRiskOut(**dr) for dr in offspring_results]
        )

    finally:
        # ALWAYS delete the raw PDFs
        for path in [mom_temp_path, dad_temp_path]:
            if path.exists():
                os.remove(path)
                if not PRODUCTION:
                    print(f"Deleted temporary PDF: {path.name}")
