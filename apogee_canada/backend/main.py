"""
main.py – FastAPI backend for Apogee Canada.
Endpoints for surgical access analysis, optimization, and policy briefs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from data import get_data
from optimizer import router as optimizer_router
from brief import generate_brief
from endpoints.investment import get_investment_analysis
from endpoints.workforce import get_workforce_alignment
from endpoints.seasonal import get_seasonal_access

app = FastAPI(
    title="Apogee Canada",
    description="Surgical access analysis for Canadian rural and remote communities",
    version="1.0.0",
)

# ─────────────────────────────────────────────────────────────────────────────
# CORS: Allow Base44 frontend + any local testing
# ─────────────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wide open for hackathon; tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Include optimizer router (POST /api/optimize)
# ─────────────────────────────────────────────────────────────────────────────
app.include_router(optimizer_router)

# ─────────────────────────────────────────────────────────────────────────────
# GET /api/data — Initial dataset: DAs, EDs, coverage stats
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/data")
def api_data():
    """Return initial Canadian DA population and ED locations."""
    return get_data()


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/brief — Stream a policy brief for the given scenario
# ─────────────────────────────────────────────────────────────────────────────
class BriefRequest(BaseModel):
    stats: dict
    optimizer_results: list


@app.post("/api/brief")
def api_brief(req: BriefRequest):
    """
    Stream a policy brief for Canadian provincial health authorities.
    Uses Claude API with fallback to hardcoded brief.
    """
    return StreamingResponse(
        generate_brief(req.stats, req.optimizer_results),
        media_type="text/plain"
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/brief-finetuned — Placeholder for Freesolo fine-tuned brief
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/brief-finetuned")
def api_brief_finetuned(req: BriefRequest):
    """
    Fine-tuned policy brief endpoint (via Freesolo).
    Placeholder: currently returns same as /api/brief.
    To be updated in Phase 4 once Freesolo training completes.
    """
    # TODO: Phase 4 — load fine-tuned weights and use them here
    return StreamingResponse(
        generate_brief(req.stats, req.optimizer_results),
        media_type="text/plain"
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/investment-analysis — Provincial investment framework
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/investment-analysis")
def api_investment():
    """
    Return illustrative Canadian provincial investment analysis.
    Status: Illustrative (not computed from centralized data).
    Demonstrates framework for real provincial consultation.
    """
    return get_investment_analysis()


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/workforce-alignment — Provincial physician supply data
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/workforce-alignment")
def api_workforce():
    """Return Canadian physician supply and rural surgical workforce data (CIHI-based)."""
    return get_workforce_alignment()


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/seasonal-access — Winter road and ice road access patterns
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/seasonal-access")
def api_seasonal():
    """
    Return Canadian seasonal access patterns.
    Focus: winter ice road closures and First Nations community isolation.
    """
    return get_seasonal_access()


# ─────────────────────────────────────────────────────────────────────────────
# GET / — Health check
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    """Health check and API info."""
    return {
        "name": "Apogee Canada",
        "status": "running",
        "endpoints": [
            "GET /api/data",
            "POST /api/optimize",
            "POST /api/brief",
            "POST /api/brief-finetuned",
            "GET /api/investment-analysis",
            "GET /api/workforce-alignment",
            "GET /api/seasonal-access",
        ],
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
