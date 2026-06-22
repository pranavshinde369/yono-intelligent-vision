from datetime import datetime
from app.models.twin import (
    FinancialTwin,
    TwinBuildRequest,
    IncomeNode,
    LiabilitiesNode,
    ProtectionNode,
    GrowthNode,
    TaxNode,
    GoalsNode,
    HealthStatus,
)


def build_financial_twin(request: TwinBuildRequest) -> FinancialTwin:
    """Builds a 6-node Financial Twin from user financial data."""

    # Income node
    dti = (request.total_emi / request.monthly_salary) * 100 if request.monthly_salary else 0
    income_score = 85.0 if dti < 40 else 60.0
    income = IncomeNode(
        monthly_salary=request.monthly_salary,
        stability_score=income_score,
        health=HealthStatus.HEALTHY if income_score > 70 else HealthStatus.WATCH,
    )

    # Liabilities node
    liabilities = LiabilitiesNode(
        total_emi=request.total_emi,
        debt_to_income_ratio=round(dti, 1),
        health=HealthStatus.HEALTHY if dti < 30 else (
            HealthStatus.WATCH if dti < 50 else HealthStatus.CRITICAL
        ),
    )

    # Protection node
    monthly_expenses = request.monthly_expenses or (request.monthly_salary * 0.6)
    emergency_months = (
        request.emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
    )
    protection_health = (
        HealthStatus.HEALTHY if emergency_months >= 6 and request.life_cover > 0
        else HealthStatus.CRITICAL if emergency_months < 2 or request.life_cover == 0
        else HealthStatus.WATCH
    )
    protection = ProtectionNode(
        life_cover=request.life_cover or 0,
        health_cover=request.health_cover or 0,
        emergency_fund_months=round(emergency_months, 1),
        health=protection_health,
    )

    # Growth node
    total_investments = (
        (request.mutual_funds or 0) + (request.fixed_deposits or 0)
    )
    growth_score = min(100, (total_investments / (request.monthly_salary * 12)) * 50)
    growth = GrowthNode(
        mutual_funds=request.mutual_funds or 0,
        fixed_deposits=request.fixed_deposits or 0,
        returns_vs_inflation_score=round(growth_score, 1),
        health=HealthStatus.HEALTHY if growth_score > 60 else (
            HealthStatus.WATCH if growth_score > 30 else HealthStatus.LOW
        ),
    )

    # Tax node
    tax = TaxNode(
        tax_bracket=request.tax_bracket or 20,
        section_80c_used=request.section_80c_used or 0,
        section_80d_used=0,
        nps_80ccd_used=0,
        health=HealthStatus.OPTIMIZABLE if (request.section_80c_used or 0) < 150000
        else HealthStatus.HEALTHY,
    )

    # Goals node
    goals = GoalsNode(goals=request.goals or [])

    twin = FinancialTwin(
        user_id=request.user_id,
        income=income,
        liabilities=liabilities,
        protection=protection,
        growth=growth,
        tax=tax,
        goals=goals,
        last_updated=datetime.utcnow().isoformat(),
    )
    twin.overall_score = twin.compute_overall_score()
    return twin


def get_twin_summary(twin: FinancialTwin) -> dict:
    """Returns a concise summary of the Financial Twin for agent consumption."""
    return {
        "user_id": twin.user_id,
        "overall_score": twin.overall_score,
        "priority": twin.get_priority_recommendation(),
        "nodes": {
            "income": {"health": twin.income.health, "salary": twin.income.monthly_salary},
            "liabilities": {"health": twin.liabilities.health, "dti": twin.liabilities.debt_to_income_ratio},
            "protection": {"health": twin.protection.health, "emergency_months": twin.protection.emergency_fund_months},
            "growth": {"health": twin.growth.health, "score": twin.growth.returns_vs_inflation_score},
            "tax": {"health": twin.tax.health, "80c_gap": twin.tax.section_80c_limit - twin.tax.section_80c_used},
            "goals": {"health": twin.goals.health, "count": len(twin.goals.goals)},
        },
    }
