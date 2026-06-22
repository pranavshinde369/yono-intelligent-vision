from fastapi import APIRouter
from app.models.signals import SignalDetectionRequest, SignalDetectionResponse
from app.services.signal_service import detect_life_stage_events

router = APIRouter()


@router.post("/detect", response_model=SignalDetectionResponse)
def detect_signals(request: SignalDetectionRequest):
    """
    Detect life-stage events from transaction data.
    Fires only when confidence >= 0.75 across 2+ signal sources.
    """
    return detect_life_stage_events(request)


@router.post("/demo")
def demo_signal():
    """
    Demo endpoint — simulates a salary jump event for Rahul.
    No auth required. Use this for hackathon demo.
    """
    demo_request = SignalDetectionRequest(
        user_id="rahul_demo",
        current_month_salary=35000,
        previous_month_salary=20000,
        current_month_credits=35000,
        current_month_debits=18000,
        new_emi_this_month=0,
        user_age=27,
        month=11,
    )
    result = detect_life_stage_events(demo_request)
    return {
        "demo": True,
        "scenario": "Rahul gets promoted — salary jumps from ₹20,000 to ₹35,000",
        "result": result,
    }
