# YONO Intelligent Vision — API Documentation

Base URL: `http://localhost:8000/api/v1`
Interactive docs: `http://localhost:8000/docs`

---

## Financial Twin

### POST /twin/build
Build a Financial Twin from user financial data.

**Request:**
```json
{
  "user_id": "rahul_001",
  "monthly_salary": 35000,
  "total_emi": 8000,
  "life_cover": 0,
  "health_cover": 0,
  "emergency_fund": 15000,
  "monthly_expenses": 22000,
  "mutual_funds": 5000,
  "fixed_deposits": 10000,
  "tax_bracket": 20,
  "section_80c_used": 24000
}
```

**Response:** Full FinancialTwin object with 6 nodes and health scores.

---

### GET /twin/{user_id}
Get current Financial Twin state.

**Response:**
```json
{
  "twin": { ... },
  "summary": { "overall_score": 58, "priority": "protection" },
  "priority_recommendation": "protection"
}
```

---

## Signal Intelligence

### POST /signals/detect
Detect life-stage events from transaction data.

**Request:**
```json
{
  "user_id": "rahul_001",
  "current_month_salary": 35000,
  "previous_month_salary": 20000,
  "current_month_credits": 35000,
  "current_month_debits": 18000,
  "month": 11
}
```

**Response:**
```json
{
  "events_detected": [
    {
      "signal_type": "salary_jump",
      "confidence": 0.87,
      "description": "Salary increased by 75% this month",
      "recommended_action": "Suggest investment or insurance upgrade"
    }
  ],
  "should_trigger_agent": true,
  "highest_confidence": 0.87
}
```

### POST /signals/demo
Demo endpoint — Rahul's promotion scenario. No auth required.

---

## Agent

### POST /agent/recommend
Get a personalised AI recommendation.

**Request:**
```json
{
  "user_id": "rahul_001",
  "event_description": "Salary increased by 75% this month",
  "language": "hindi"
}
```

**Response:**
```json
{
  "recommendation": "Rahul bhai, promotion ki bahut bahut badhai! ...",
  "priority_area": "protection",
  "trust_tier": "advisor"
}
```

### POST /agent/simulate
Simulate the financial impact of a decision.

**Request:**
```json
{
  "user_id": "rahul_001",
  "decision": "Buy a ₹7L car on EMI",
  "decision_amount": 700000
}
```

### POST /agent/demo/recommend
Demo endpoint — Hindi recommendation for Rahul. No auth required.

---

## Analytics

### POST /analytics/money-story
Generate monthly Money Story narrative.

### POST /analytics/spend-dna
Get Spend DNA vs peer cohort.

### POST /analytics/cashflow
Get 30-day cash flow forecast.

### POST /analytics/tax-radar
Get real-time tax opportunity analysis.

### POST /analytics/discipline-score
Calculate Financial Discipline Score.

### GET /analytics/demo/money-story
Demo endpoint — Rahul's October Money Story. No auth required.

---

## Demo Endpoints (No Auth Required)

| Endpoint | Description |
|----------|-------------|
| GET / | API info |
| GET /health | Health check |
| POST /signals/demo | Rahul's promotion signal |
| POST /agent/demo/recommend | Hindi recommendation |
| GET /analytics/demo/money-story | October Money Story |
