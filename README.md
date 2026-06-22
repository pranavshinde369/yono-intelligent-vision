# YONO Intelligent Vision

> **SBI Hackathon @ GFF 2026 — Digital Adoption Track**

YONO Intelligent Vision is an agentic AI layer embedded inside SBI YONO that detects life-stage transitions, builds a live Financial Twin, and delivers narrative analytics. It turns YONO from a transaction utility into a proactive financial advisor for every Indian user.

---

## Overview

- Detects important life-stage signals from financial activity and documents.
- Builds a live six-node Financial Twin to model income, liabilities, protection, growth, tax, and goals.
- Generates actionable narrative analytics and recommendations.
- Supports trust-gated agentic interactions for observer, advisor, and co-pilot modes.

---
## Problem

YONO is used by millions daily, but most users only access payments and UPI features. The platform rarely surfaces the right financial recommendation at the right life stage, so users miss investment, insurance, and savings opportunities.

## Solution

YONO Intelligent Vision detects life-stage triggers from transactions, account aggregator data, document signals, and user behavior. It creates a live Financial Twin and delivers personalized narrative analytics that help users act when the opportunity is most relevant.

## Repository Structure

```text
yono-intelligent-vision/
  backend/           # FastAPI backend
    app/
      agents/        # Agent definitions and orchestration
      models/        # Data models and domain schemas
      routes/        # API endpoints
      services/      # Business logic and workflows
  frontend/          # React / Expo frontend and UI
    src/
      components/    # Reusable UI components
      screens/       # Application views
      utils/         # Helpers and API clients
  demo/              # Standalone HTML demo for quick preview
  docs/              # Architecture and API reference documentation
  docker-compose.yml # Local deployment helpers
  LICENSE            # Project license
```
