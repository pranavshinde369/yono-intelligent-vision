from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.routes.twin import twin_store
from app.services.agent_service import get_contextual_recommendation, run_decision_simulator

router = APIRouter()


class RecommendationRequest(BaseModel):
    user_id: str
    event_description: str
    language: Optional[str] = "english"


class SimulationRequest(BaseModel):
    user_id: str
    decision: str
    decision_amount: float


@router.post("/recommend")
def get_recommendation(request: RecommendationRequest):
    """Get a personalised AI recommendation based on Financial Twin and life event."""
    if request.user_id not in twin_store:
        raise HTTPException(status_code=404, detail="Financial Twin not found. Build one first.")

    twin = twin_store[request.user_id]
    recommendation = get_contextual_recommendation(
        twin=twin,
        event_description=request.event_description,
        language=request.language,
    )
    return {
        "user_id": request.user_id,
        "event": request.event_description,
        "language": request.language,
        "recommendation": recommendation,
        "priority_area": twin.get_priority_recommendation(),
        "trust_tier": "advisor",
    }


@router.post("/simulate")
def simulate_decision(request: SimulationRequest):
    """Simulate the financial impact of a major decision against the Financial Twin."""
    if request.user_id not in twin_store:
        raise HTTPException(status_code=404, detail="Financial Twin not found. Build one first.")

    twin = twin_store[request.user_id]
    result = run_decision_simulator(
        twin=twin,
        decision=request.decision,
        decision_amount=request.decision_amount,
    )
    return {
        "user_id": request.user_id,
        "decision": request.decision,
        "amount": request.decision_amount,
        "simulation_result": result,
    }


@router.post("/demo/recommend")
def demo_recommendation():
    """
    Demo endpoint — Rahul's promotion recommendation in Hindi.
    No auth required. Use this for hackathon demo.
    """
    from app.services.twin_service import build_financial_twin
    from app.models.twin import TwinBuildRequest

    demo_twin = build_financial_twin(TwinBuildRequest(
        user_id="rahul_demo",
        monthly_salary=35000,
        total_emi=8000,
        life_cover=0,
        health_cover=0,
        emergency_fund=15000,
        monthly_expenses=22000,
        mutual_funds=5000,
        fixed_deposits=10000,
        tax_bracket=20,
        section_80c_used=24000,
    ))

    recommendation = get_contextual_recommendation(
        twin=demo_twin,
        event_description="Salary increased from ₹20,000 to ₹35,000 this month — a 75% jump indicating a promotion",
        language="hindi",
    )
    return {
        "demo": True,
        "scenario": "Rahul gets promoted",
        "twin_priority": demo_twin.get_priority_recommendation(),
        "recommendation_hindi": recommendation,
    }
