# YONO Intelligent Vision — Architecture Documentation

## System Overview

YONO Intelligent Vision is a 5-layer agentic AI system embedded inside SBI YONO.

```
┌─────────────────────────────────────────────────────────┐
│                    User (YONO App)                       │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Data Aggregation Layer                      │
│  SBI Core Banking | RBI AA | SEBI MF | DigiLocker | CIBIL│
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│           Signal Intelligence Engine                     │
│   Event Classifier | Confidence Threshold | Kafka        │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
┌─────────▼──────────┐  ┌─────────▼──────────┐
│  Financial Twin    │◄─►│   Agent Brain      │
│  (Neo4j 6 nodes)   │  │  Claude Sonnet 4.6  │
│  Health Scores     │  │  LangGraph + RAG    │
│  Simulation Engine │  │  Bhashini Voice     │
└─────────┬──────────┘  └─────────┬──────────┘
          └───────────┬───────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                   Trust Gate                             │
│        Observer → Advisor → Co-pilot                     │
│        10-min undo | Audit log | Consent                 │
└─────────────────────┬───────────────────────────────────┘
                      │
     ┌────────────────┼────────────────┐
     │                │                │
┌────▼────┐    ┌──────▼─────┐   ┌─────▼──────┐
│Product  │    │ Narrative  │   │    User    │
│Activation│   │ Analytics  │   │ Interface  │
│SBI APIs │    │ Engine     │   │Cards+Dash  │
└─────────┘    └────────────┘   └────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Feedback Loop                               │
│     User actions → Signal Engine → Twin Recalibration   │
└─────────────────────────────────────────────────────────┘
```

## Layer 1 — Data Aggregation

| Source | Data | Integration |
|--------|------|-------------|
| SBI Core Banking | Transactions, balances, products | Internal APIs |
| RBI Account Aggregator | Cross-bank data | AA framework (FIP/FIU) |
| SEBI MF Central | Portfolio, NAV, holdings | Official API |
| DigiLocker | Life documents | Pull API with consent |
| CIBIL | Credit score, liabilities | API integration |

## Layer 2 — Signal Intelligence Engine

- **Classifier**: Python, Scikit-learn, XGBoost
- **Pipeline**: Apache Kafka for real-time event streaming
- **Confidence threshold**: 0.75 across 2+ independent sources
- **Signal types**: Salary jump, bonus, new EMI, tax season, age milestone, investment intent

## Layer 3 — Financial Twin (Neo4j)

Six nodes, each with:
- Live value (updated daily + on every transaction)
- Health score (0–100)
- Health status (Healthy / Watch / Critical / Low / Optimizable)
- Priority logic: Protection > Liabilities > Tax > Growth

## Layer 4 — Agent Brain

- **LLM**: Claude Sonnet 4.6 (Anthropic)
- **Orchestration**: LangGraph state machine
- **Knowledge**: LangChain RAG on SBI product catalog
- **Languages**: Bhashini STT/TTS (12 Indian languages)
- **Inference**: On-device NLP for sensitive data

## Layer 5 — Trust Gate

| Tier | Activation | Agent Capability |
|------|-----------|-----------------|
| Observer | Default (Day 0) | Read-only, zero notifications |
| Advisor | Day 31, user-confirmed | Suggest + 2-tap confirm |
| Co-pilot | Explicit opt-in | Rule-based execution + 10-min undo |

## Analytics Engine — 8 Modules

| Module | Data Source | Output |
|--------|------------|--------|
| Money Story | Twin + transactions | Monthly narrative (Claude API) |
| Spend DNA | Transactions + cohort | Peer benchmarking |
| Goal Runway | Goals node + spend | Impact visualisation |
| Cash Flow Forecaster | 6-month history | 30-day prediction (LSTM) |
| Tax Radar | Tax node + ITR | Live deduction gap |
| Habit Loop Detector | Recurring patterns | Drain identification |
| Decision Simulator | Twin + Monte Carlo | "Can I afford this?" |
| Discipline Score | Investment + EMI history | Peer-ranked score |

## Security Architecture

- AES-256 encryption at rest and in transit
- HSM key management
- Federated learning — no raw data leaves SBI
- Differential privacy for peer cohort benchmarking
- OAuth 2.0 + JWT for authentication
- Immutable audit log (Apache Cassandra)

## Compliance

- RBI Account Aggregator framework
- SEBI MF Central data standards
- IRDAI distribution guidelines 2023
- DPDP Act 2023
- RBI Regulatory Sandbox Track 3 eligible
