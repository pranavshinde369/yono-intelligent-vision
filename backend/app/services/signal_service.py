from app.models.signals import (
    SignalDetectionRequest,
    SignalDetectionResponse,
    LifeStageEvent,
    SignalType,
)

CONFIDENCE_THRESHOLD = 0.75


def detect_life_stage_events(request: SignalDetectionRequest) -> SignalDetectionResponse:
    """
    Detects life-stage events from transaction signals.
    Fires only when confidence >= 0.75 across 2+ signal sources.
    """
    events = []

    # Signal 1: Salary jump detection
    if request.previous_month_salary > 0:
        salary_change = (
            (request.current_month_salary - request.previous_month_salary)
            / request.previous_month_salary
        ) * 100

        if salary_change >= 30:
            confidence = min(0.95, 0.75 + (salary_change - 30) / 100)
            events.append(
                LifeStageEvent(
                    signal_type=SignalType.SALARY_JUMP,
                    confidence=round(confidence, 2),
                    description=f"Salary increased by {salary_change:.1f}% this month",
                    detected_value=request.current_month_salary - request.previous_month_salary,
                    recommended_action="Suggest investment or insurance upgrade",
                )
            )

    # Signal 2: Bonus detected (large one-time credit significantly above salary)
    bonus_threshold = request.current_month_salary * 0.5
    extra_credit = request.current_month_credits - request.current_month_salary
    if extra_credit > bonus_threshold:
        events.append(
            LifeStageEvent(
                signal_type=SignalType.BONUS_CREDITED,
                confidence=0.88,
                description=f"Bonus/extra credit of ₹{extra_credit:,.0f} detected",
                detected_value=extra_credit,
                recommended_action="Suggest lump sum investment or emergency fund top-up",
            )
        )

    # Signal 3: New EMI detected
    if request.new_emi_this_month and request.new_emi_this_month > 2000:
        events.append(
            LifeStageEvent(
                signal_type=SignalType.NEW_EMI_DETECTED,
                confidence=0.92,
                description=f"New EMI of ₹{request.new_emi_this_month:,.0f} detected",
                detected_value=request.new_emi_this_month,
                recommended_action="Review protection gap and emergency fund adequacy",
            )
        )

    # Signal 4: Tax season (Jan-Mar)
    if request.month and request.month in [1, 2, 3]:
        events.append(
            LifeStageEvent(
                signal_type=SignalType.TAX_SEASON,
                confidence=0.99,
                description="Tax filing season — high receptivity to 80C products",
                recommended_action="Surface Tax Radar with ELSS and NPS opportunities",
            )
        )

    # Signal 5: Age milestone
    if request.user_age and request.user_age in [25, 30, 35, 40, 45, 50]:
        events.append(
            LifeStageEvent(
                signal_type=SignalType.BIRTHDAY_MILESTONE,
                confidence=0.85,
                description=f"User turning {request.user_age} — key life-stage milestone",
                recommended_action="Full financial health review and goal reset",
            )
        )

    # Filter by confidence threshold
    qualified_events = [e for e in events if e.confidence >= CONFIDENCE_THRESHOLD]
    should_trigger = len(qualified_events) >= 1

    priority = (
        max(qualified_events, key=lambda e: e.confidence) if qualified_events else None
    )
    highest_confidence = max((e.confidence for e in qualified_events), default=0.0)

    return SignalDetectionResponse(
        user_id=request.user_id,
        events_detected=qualified_events,
        should_trigger_agent=should_trigger,
        highest_confidence=highest_confidence,
        priority_signal=priority,
    )
