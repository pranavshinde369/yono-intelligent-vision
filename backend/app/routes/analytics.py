from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.routes.twin import twin_store
from app.services.agent_service import generate_money_story, generate_spend_dna

router = APIRouter()


class MoneyStoryRequest(BaseModel):
    user_id: str
    month_name: str
    income: float
    expenses: float
    top_category: str
    top_amount: float
    savings: float
    sip: Optional[float] = 0
    language: Optional[str] = "english"


class SpendDNARequest(BaseModel):
    user_id: str
    spend_categories: dict
    peer_averages: dict
    monthly_income: float


class CashFlowRequest(BaseModel):
    user_id: str
    monthly_salary: float
    fixed_outflows: float
    predicted_variable: float


class TaxRadarRequest(BaseModel):
    user_id: str
    section_80c_used: float
    section_80d_used: float
    nps_used: float
    tax_bracket: int


@router.post("/money-story")
def get_money_story(request: MoneyStoryRequest):
    """Generate a personalised monthly Money Story narrative."""
    if request.user_id not in twin_store:
        raise HTTPException(status_code=404, detail="Financial Twin not found.")

    twin = twin_store[request.user_id]
    story = generate_money_story(
        twin=twin,
        month_name=request.month_name,
        spend_summary={
            "income": request.income,
            "expenses": request.expenses,
            "top_category": request.top_category,
            "top_amount": request.top_amount,
            "savings": request.savings,
            "sip": request.sip,
        },
        language=request.language,
    )
    return {
        "user_id": request.user_id,
        "month": request.month_name,
        "money_story": story,
        "savings_rate": round((request.savings / request.income) * 100, 1) if request.income else 0,
    }


@router.post("/spend-dna")
def get_spend_dna(request: SpendDNARequest):
    """Get Spend DNA analysis vs anonymised peer cohort."""
    if request.user_id not in twin_store:
        raise HTTPException(status_code=404, detail="Financial Twin not found.")

    insight = generate_spend_dna(
        spend_categories=request.spend_categories,
        peer_averages=request.peer_averages,
        monthly_income=request.monthly_income,
    )

    deviations = {}
    for category, amount in request.spend_categories.items():
        peer = request.peer_averages.get(category, 0)
        if peer > 0:
            diff = round(((amount - peer) / peer) * 100, 1)
            deviations[category] = {"your_spend": amount, "peer_avg": peer, "diff_pct": diff}

    return {
        "user_id": request.user_id,
        "deviations": deviations,
        "ai_insight": insight,
    }


@router.post("/cashflow")
def get_cashflow_forecast(request: CashFlowRequest):
    """Get 30-day cash flow forecast with stress period detection."""
    projected_surplus = request.monthly_salary - request.fixed_outflows - request.predicted_variable
    stress_risk = projected_surplus < (request.monthly_salary * 0.1)

    return {
        "user_id": request.user_id,
        "forecast": {
            "predicted_inflow": request.monthly_salary,
            "fixed_outflows": request.fixed_outflows,
            "variable_predicted": request.predicted_variable,
            "projected_surplus": round(projected_surplus, 0),
        },
        "stress_risk": stress_risk,
        "alert": (
            f"Balance stress risk detected. Surplus of only ₹{projected_surplus:,.0f} this month. "
            "Consider moving funds to a buffer account before major bills are due."
            if stress_risk else "Cash flow looks healthy this month."
        ),
    }


@router.post("/tax-radar")
def get_tax_radar(request: TaxRadarRequest):
    """Get real-time tax opportunity analysis."""
    gap_80c = max(0, 150000 - request.section_80c_used)
    gap_80d = max(0, 25000 - request.section_80d_used)
    gap_nps = max(0, 50000 - request.nps_used)
    total_gap = gap_80c + gap_80d + gap_nps
    tax_rate = request.tax_bracket / 100
    potential_saving = round(total_gap * tax_rate, 0)

    return {
        "user_id": request.user_id,
        "gaps": {
            "80C_remaining": gap_80c,
            "80D_remaining": gap_80d,
            "NPS_80CCD_remaining": gap_nps,
        },
        "total_deduction_gap": total_gap,
        "potential_tax_saving": potential_saving,
        "recommendations": [
            f"Invest ₹{gap_80c:,.0f} in ELSS to fully utilise 80C" if gap_80c > 0 else None,
            f"Get health insurance worth ₹{gap_80d:,.0f} to claim 80D" if gap_80d > 0 else None,
            f"Top up NPS by ₹{gap_nps:,.0f} for additional 80CCD(1B) deduction" if gap_nps > 0 else None,
        ],
        "summary": f"You can save ₹{potential_saving:,.0f} more in taxes this FY by utilising remaining deductions.",
    }


@router.post("/discipline-score")
def get_discipline_score(request: dict):
    """Calculate Financial Discipline Score vs peer cohort."""
    investment_consistency = request.get("sip_months_paid", 0) / 12 * 100
    emi_consistency = request.get("emi_on_time", 0) / 12 * 100
    savings_rate = request.get("avg_savings_rate", 0)
    score = round((investment_consistency * 0.4) + (emi_consistency * 0.3) + (savings_rate * 0.3), 1)

    return {
        "discipline_score": min(100, score),
        "investment_consistency": investment_consistency,
        "emi_consistency": emi_consistency,
        "savings_rate": savings_rate,
        "peer_rank": f"Top {max(5, 100 - int(score))}% of YONO users in your age and income group",
    }


@router.get("/demo/money-story")
def demo_money_story():
    """
    Demo endpoint — Rahul's October Money Story.
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

    story = generate_money_story(
        twin=demo_twin,
        month_name="October",
        spend_summary={
            "income": 35000,
            "expenses": 26800,
            "top_category": "Food Delivery (Zomato + Swiggy)",
            "top_amount": 3840,
            "savings": 8200,
            "sip": 2000,
        },
        language="english",
    )
    return {
        "demo": True,
        "user": "Rahul, 27, Pune",
        "month": "October",
        "money_story": story,
        "savings_rate": "23.4%",
    }
