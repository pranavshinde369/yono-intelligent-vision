from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import twin, signals, agent, analytics

app = FastAPI(
    title="YONO Intelligent Vision API",
    description="Agentic AI layer for SBI YONO — Financial Twin, Signal Intelligence, and Narrative Analytics",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(twin.router, prefix="/api/v1/twin", tags=["Financial Twin"])
app.include_router(signals.router, prefix="/api/v1/signals", tags=["Signal Intelligence"])
app.include_router(agent.router, prefix="/api/v1/agent", tags=["Agent"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/")
def root():
    return {
        "project": "YONO Intelligent Vision",
        "version": "1.0.0",
        "hackathon": "SBI Hackathon @ GFF 2026",
        "track": "Digital Adoption",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
