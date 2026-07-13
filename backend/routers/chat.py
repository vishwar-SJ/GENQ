"""
GENQ Chat Router — AI Health Advisor chatbot endpoint.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, GeneticReport, DiseaseRiskResult, DrugResponseResult
from schemas import ChatRequest, ChatResponse
from auth.dependencies import get_current_user
from services.chatbot import generate_chat_response

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a health advice response based on the user's report and question."""
    # Get the specified report, or the latest one
    if req.report_id:
        report = (
            db.query(GeneticReport)
            .filter(
                GeneticReport.id == req.report_id,
                GeneticReport.user_id == current_user.id,
            )
            .first()
        )
    else:
        report = (
            db.query(GeneticReport)
            .filter(GeneticReport.user_id == current_user.id)
            .order_by(GeneticReport.uploaded_at.desc())
            .first()
        )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No report found. Please upload a genetic report first.",
        )

    # Build disease risk and drug response dicts
    disease_risks = [
        {
            "disease_name": dr.disease_name,
            "risk_label": dr.risk_label,
            "percentile": dr.percentile,
            "raw_score": dr.raw_score,
        }
        for dr in report.disease_results
    ]

    drug_responses = [
        {
            "drug_name": dg.drug_name,
            "gene": dg.gene,
            "metabolizer_status": dg.metabolizer_status,
            "guidance_text": dg.guidance_text,
        }
        for dg in report.drug_results
    ]

    # Generate response
    result = generate_chat_response(req.message, disease_risks, drug_responses)

    return ChatResponse(
        response=result["response"],
        sections=result.get("sections"),
    )
