import os
import json
from pathlib import Path
from typing import List, Dict, Any, Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
from data import get_data
from optimizer import router as optimizer_router
from brief import generate_brief
from endpoints.investment import get_investment_analysis
from endpoints.workforce import get_workforce_alignment
from endpoints.seasonal import get_seasonal_access
import openai
from anthropic import Anthropic

# Initialize Anthropic client
anthropic_client = Anthropic()

# Initialize Freesolo fine-tuned client (OpenAI-compatible)
FINETUNED_MODEL_URL = "https://clado-ai--freesolo-lora-serving.modal.run/v1"
FREESOLO_API_KEY = os.getenv("FREESOLO_API_KEY", "dummy")
finetuned_client = openai.OpenAI(api_key=FREESOLO_API_KEY, base_url=FINETUNED_MODEL_URL)

# Load API key from environment
API_KEY = os.getenv("APOGEE_API_KEY")

# Create app
app = FastAPI(
    title="Zenith Canada - Surgical Access Optimization",
    description="Surgical access analysis for Canadian rural and remote communities",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key middleware
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    if request.url.path in ["/", "/docs", "/openapi.json", "/health"]:
        return await call_next(request)
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=401, content={"detail": "Invalid API key"})
    return await call_next(request)

# Include optimizer router (POST /api/optimize)
app.include_router(optimizer_router)

# Pydantic models
class BriefRequest(BaseModel):
    stats: dict
    optimizer_results: Union[list, dict]

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "apogee-canada"}

@app.get("/api/data")
def api_data():
    """Return initial Canadian DA population and ED locations."""
    return get_data()

@app.post("/api/brief")
def api_brief(req: BriefRequest):
    """
    Stream a policy brief for Canadian provincial health authorities.
    Uses Claude API with fallback to hardcoded brief.
    """
    results = req.optimizer_results if isinstance(req.optimizer_results, list) else [req.optimizer_results]
    for res in results:
        if "pop_gain" in res and "pop_gained" not in res:
            res["pop_gained"] = res["pop_gain"]

    return StreamingResponse(
        generate_brief(req.stats, results),
        media_type="text/plain"
    )

@app.post("/api/brief-finetuned")
def generate_brief_finetuned(req: BriefRequest):
    """Generate fine-tuned Qwen policy brief, fallback to Claude"""
    results = req.optimizer_results if isinstance(req.optimizer_results, list) else [req.optimizer_results]
    for res in results:
        if "pop_gain" in res and "pop_gained" not in res:
            res["pop_gained"] = res["pop_gain"]

    try:
        stats_str = json.dumps(req.stats, indent=2)
        locations_str = json.dumps(results[:3], indent=2) if results else "No specific locations"
        
        prompt = f"""Given these facility placement statistics:
{stats_str}

Top recommended facility locations:
{locations_str}

Generate a policy brief for Canadian health authorities."""

        response = finetuned_client.chat.completions.create(
            model="lora",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7,
            timeout=30
        )
        
        return {"brief": response.choices[0].message.content, "model": "finetuned-qwen"}
    
    except Exception as e:
        # Fallback to Claude if fine-tuned model fails
        try:
            stats_str = json.dumps(req.stats, indent=2)
            locations_str = json.dumps(results[:3], indent=2) if results else "No specific locations"
            
            prompt = f"""You are a healthcare policy analyst specializing in rural surgical access in Canada.

Given these facility placement statistics:
{stats_str}

Top recommended facility locations:
{locations_str}

Generate a policy brief for Canadian health authorities."""

            response = anthropic_client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {"brief": response.content[0].text, "model": "claude-fallback"}
        except Exception as fallback_error:
            return {"error": f"Both models failed: {str(fallback_error)}", "model": "error"}

@app.get("/api/investment-analysis")
def api_investment():
    """
    Return illustrative Canadian provincial investment analysis.
    Status: Illustrative (not computed from centralized data).
    Demonstrates framework for real provincial consultation.
    """
    return get_investment_analysis()

@app.get("/api/workforce-alignment")
def api_workforce():
    """Return Canadian physician supply and rural surgical workforce data (CIHI-based)."""
    return get_workforce_alignment()

@app.get("/api/seasonal-access")
def api_seasonal():
    """
    Return Canadian seasonal access patterns.
    Focus: winter ice road closures and First Nations community isolation.
    """
    return get_seasonal_access()

@app.get("/")
def root():
    """Health check and API info."""
    return {
        "name": "Zenith Canada",
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
