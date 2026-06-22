from fastapi import APIRouter, HTTPException
from app.models.twin import TwinBuildRequest, FinancialTwin
from app.services.twin_service import build_financial_twin, get_twin_summary

router = APIRouter()

# In-memory store for demo purposes (replace with Neo4j in production)
twin_store: dict[str, FinancialTwin] = {}


@router.post("/build", response_model=FinancialTwin)
def build_twin(request: TwinBuildRequest):
    """Build a Financial Twin for a user from their financial data."""
    twin = build_financial_twin(request)
    twin_store[request.user_id] = twin
    return twin


@router.get("/{user_id}")
def get_twin(user_id: str):
    """Get the current Financial Twin state for a user."""
    if user_id not in twin_store:
        raise HTTPException(status_code=404, detail="Financial Twin not found. Build one first.")
    twin = twin_store[user_id]
    return {
        "twin": twin,
        "summary": get_twin_summary(twin),
        "priority_recommendation": twin.get_priority_recommendation(),
    }


@router.get("/{user_id}/health")
def get_twin_health(user_id: str):
    """Get node-level health scores for the Financial Twin."""
    if user_id not in twin_store:
        raise HTTPException(status_code=404, detail="Financial Twin not found.")
    twin = twin_store[user_id]
    return {
        "user_id": user_id,
        "overall_score": twin.overall_score,
        "nodes": {
            "income": twin.income.health,
            "liabilities": twin.liabilities.health,
            "protection": twin.protection.health,
            "growth": twin.growth.health,
            "tax": twin.tax.health,
            "goals": twin.goals.health,
        },
        "priority": twin.get_priority_recommendation(),
    }
