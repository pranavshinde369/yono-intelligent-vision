from pydantic import BaseModel
from typing import Optional
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    WATCH = "watch"
    CRITICAL = "critical"
    LOW = "low"
    OPTIMIZABLE = "optimizable"
    ON_TRACK = "on_track"


class IncomeNode(BaseModel):
    monthly_salary: float
    bonus_last_year: Optional[float] = 0
    other_income: Optional[float] = 0
    stability_score: float  # 0-100
    health: HealthStatus = HealthStatus.HEALTHY


class LiabilitiesNode(BaseModel):
    total_emi: float
    credit_card_dues: Optional[float] = 0
    debt_to_income_ratio: float  # percentage
    health: HealthStatus = HealthStatus.WATCH


class ProtectionNode(BaseModel):
    life_cover: Optional[float] = 0
    health_cover: Optional[float] = 0
    emergency_fund_months: float  # months of expenses covered
    health: HealthStatus = HealthStatus.CRITICAL


class GrowthNode(BaseModel):
    mutual_funds: Optional[float] = 0
    fixed_deposits: Optional[float] = 0
    ppf: Optional[float] = 0
    nps: Optional[float] = 0
    stocks: Optional[float] = 0
    returns_vs_inflation_score: float  # 0-100
    health: HealthStatus = HealthStatus.LOW


class TaxNode(BaseModel):
    tax_bracket: int  # percentage
    section_80c_used: float
    section_80c_limit: float = 150000
    section_80d_used: float
    section_80d_limit: float = 25000
    nps_80ccd_used: float
    nps_80ccd_limit: float = 50000
    health: HealthStatus = HealthStatus.OPTIMIZABLE


class Goal(BaseModel):
    name: str
    target_amount: float
    current_savings: float
    target_year: int
    monthly_required: float
    on_track: bool


class GoalsNode(BaseModel):
    goals: list[Goal] = []
    health: HealthStatus = HealthStatus.ON_TRACK


class FinancialTwin(BaseModel):
    user_id: str
    income: IncomeNode
    liabilities: LiabilitiesNode
    protection: ProtectionNode
    growth: GrowthNode
    tax: TaxNode
    goals: GoalsNode
    overall_score: Optional[float] = None
    last_updated: Optional[str] = None

    def compute_overall_score(self) -> float:
        scores = {
            "income": self.income.stability_score,
            "liabilities": 100 - (self.liabilities.debt_to_income_ratio * 2),
            "protection": (self.protection.emergency_fund_months / 6) * 100,
            "growth": self.growth.returns_vs_inflation_score,
            "tax": ((self.tax.section_80c_used / self.tax.section_80c_limit) * 100),
        }
        return round(sum(scores.values()) / len(scores), 1)

    def get_priority_recommendation(self) -> str:
        """Priority logic: never recommend growth when protection is critical."""
        if self.protection.health == HealthStatus.CRITICAL:
            return "protection"
        if self.liabilities.health == HealthStatus.CRITICAL:
            return "liabilities"
        if self.tax.health == HealthStatus.OPTIMIZABLE:
            return "tax"
        return "growth"


class TwinBuildRequest(BaseModel):
    user_id: str
    monthly_salary: float
    total_emi: float
    life_cover: Optional[float] = 0
    health_cover: Optional[float] = 0
    emergency_fund: Optional[float] = 0
    monthly_expenses: Optional[float] = 0
    mutual_funds: Optional[float] = 0
    fixed_deposits: Optional[float] = 0
    tax_bracket: Optional[int] = 20
    section_80c_used: Optional[float] = 0
    goals: Optional[list[Goal]] = []
