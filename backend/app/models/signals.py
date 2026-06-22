from pydantic import BaseModel
from typing import Optional
from enum import Enum


class SignalType(str, Enum):
    SALARY_JUMP = "salary_jump"
    BONUS_CREDITED = "bonus_credited"
    NEW_EMI_DETECTED = "new_emi_detected"
    TAX_SEASON = "tax_season"
    FD_MATURITY = "fd_maturity"
    LARGE_EXPENSE = "large_expense"
    INVESTMENT_INTENT = "investment_intent"
    BIRTHDAY_MILESTONE = "birthday_milestone"


class LifeStageEvent(BaseModel):
    signal_type: SignalType
    confidence: float  # 0.0 to 1.0
    description: str
    detected_value: Optional[float] = None
    recommended_action: Optional[str] = None


class SignalDetectionRequest(BaseModel):
    user_id: str
    current_month_salary: float
    previous_month_salary: float
    current_month_credits: float
    current_month_debits: float
    new_emi_this_month: Optional[float] = 0
    user_age: Optional[int] = None
    month: Optional[int] = None  # 1-12


class SignalDetectionResponse(BaseModel):
    user_id: str
    events_detected: list[LifeStageEvent]
    should_trigger_agent: bool
    highest_confidence: float
    priority_signal: Optional[LifeStageEvent] = None
