import os
import anthropic
from app.models.twin import FinancialTwin
from app.services.twin_service import get_twin_summary

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"


def get_contextual_recommendation(
    twin: FinancialTwin,
    event_description: str,
    language: str = "english",
) -> str:
    """
    Generates a personalised, contextual recommendation based on
    the Financial Twin state and the detected life-stage event.
    """
    twin_summary = get_twin_summary(twin)
    priority = twin_summary["priority"]
    nodes = twin_summary["nodes"]

    lang_instruction = (
        "Respond in Hindi using simple, warm language."
        if language == "hindi"
        else "Respond in English using simple, warm language."
    )

    prompt = f"""You are FinSaathi, the AI financial advisor inside SBI YONO. 
You are speaking directly to a bank customer. Be warm, specific, and helpful.

{lang_instruction}

The user's Financial Twin summary:
- Overall financial health score: {twin_summary['overall_score']}/100
- Monthly salary: ₹{nodes['income']['salary']:,.0f}
- Debt-to-income ratio: {nodes['liabilities']['dti']}%
- Emergency fund: {nodes['protection']['emergency_months']} months
- Investment score: {nodes['growth']['score']}/100
- Tax savings gap (80C): ₹{nodes['tax']['80c_gap']:,.0f} remaining
- Priority area: {priority}

Life event detected: {event_description}

Instructions:
1. Acknowledge the life event in one warm sentence
2. Based on the priority area ({priority}), suggest ONE specific SBI product
3. Give one clear number (amount, percentage, or time period)
4. End with a simple call to action in one sentence
5. Keep total response under 4 sentences
6. Never use financial jargon

Do NOT recommend growth/investment products if protection is critical."""

    message = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_money_story(
    twin: FinancialTwin,
    month_name: str,
    spend_summary: dict,
    language: str = "english",
) -> str:
    """
    Generates a personalised monthly Money Story narrative.
    Analytics that reads like a letter from a trusted advisor.
    """
    twin_summary = get_twin_summary(twin)

    lang_instruction = (
        "Write in Hindi using simple, warm, conversational language."
        if language == "hindi"
        else "Write in English using simple, warm, conversational language."
    )

    prompt = f"""You are FinSaathi, the AI financial advisor inside SBI YONO.
Generate a monthly Money Story for the user — a short, personal financial narrative.

{lang_instruction}

Month: {month_name}
Financial Twin summary: {twin_summary}
Spending summary this month:
- Total income: ₹{spend_summary.get('income', 0):,.0f}
- Total expenses: ₹{spend_summary.get('expenses', 0):,.0f}
- Top spend category: {spend_summary.get('top_category', 'Food')}
- Top category amount: ₹{spend_summary.get('top_amount', 0):,.0f}
- Savings this month: ₹{spend_summary.get('savings', 0):,.0f}
- SIP invested: ₹{spend_summary.get('sip', 0):,.0f}

Write exactly 4 sentences:
1. One positive highlight from this month
2. One area of concern with a specific number
3. What this means for their most important goal
4. One clear, specific action they should take right now

Be personal, specific, and end with energy. No bullet points. No headers. Just 4 sentences."""

    message = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def run_decision_simulator(
    twin: FinancialTwin,
    decision: str,
    decision_amount: float,
) -> str:
    """
    Simulates the financial impact of a major decision against the Financial Twin.
    Answers 'can I afford this?' before the user commits.
    """
    twin_summary = get_twin_summary(twin)
    nodes = twin_summary["nodes"]

    prompt = f"""You are FinSaathi, the AI financial advisor inside SBI YONO.
A user wants to know: "{decision}"
Decision amount: ₹{decision_amount:,.0f}

Their Financial Twin:
- Monthly salary: ₹{nodes['income']['salary']:,.0f}
- Current EMI burden: {nodes['liabilities']['dti']}% of income
- Emergency fund: {nodes['protection']['emergency_months']} months
- Investment score: {nodes['growth']['score']}/100
- Overall financial health: {twin_summary['overall_score']}/100

Simulate the impact of this decision and respond in exactly 3 sentences:
1. What happens to their monthly cash flow if they proceed
2. How it affects their top 2 financial goals (be specific with months/amounts)
3. Your verdict: proceed, wait, or alternative suggestion with a specific timeline

Be direct. Use numbers. Be honest even if the answer is unfavorable."""

    message = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_spend_dna(
    spend_categories: dict,
    peer_averages: dict,
    monthly_income: float,
) -> str:
    """Generates a Spend DNA narrative comparing user spend to peer cohort."""

    deviations = {}
    for category, amount in spend_categories.items():
        peer_avg = peer_averages.get(category, 0)
        if peer_avg > 0:
            pct_diff = ((amount - peer_avg) / peer_avg) * 100
            deviations[category] = {"amount": amount, "peer": peer_avg, "diff": pct_diff}

    worst = max(deviations.items(), key=lambda x: x[1]["diff"]) if deviations else None

    prompt = f"""You are FinSaathi. Analyse this user's spending vs their peer cohort.

User spending this month: {spend_categories}
Peer cohort averages (same city, age, income): {peer_averages}
Monthly income: ₹{monthly_income:,.0f}

Key deviations found: {deviations}
Highest overspend category: {worst[0] if worst else 'None'} at {worst[1]['diff']:.0f}% above peers

Write 2 sentences:
1. Name the biggest spending deviation and its annual cost opportunity
2. One specific, non-restrictive suggestion to rebalance it

Be specific with rupee amounts. Be non-judgmental."""

    message = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
