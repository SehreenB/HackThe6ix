import os
import json
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
import openai
from anthropic import Anthropic

# Initialize Anthropic client
anthropic_client = Anthropic()

# Initialize Freesolo fine-tuned client (OpenAI-compatible)
FINETUNED_MODEL_URL = "https://clado-ai--freesolo-lora-serving.modal.run/v1"
finetuned_client = openai.OpenAI(api_key="dummy", base_url=FINETUNED_MODEL_URL)

# Load API key from environment
API_KEY = os.getenv("apogee_api_key", "default-key-change-me")

# Create app
app = FastAPI(title="Apogee Canada - Surgical Access Optimization")

# Load data
data_dir = Path(__file__).parent / "data"
da_data = pd.read_csv(data_dir / "da_working_dataset.csv") if (data_dir / "da_working_dataset.csv").exists() else pd.DataFrame()
ed_data = pd.read_csv(data_dir / "ED_locations.csv") if (data_dir / "ED_locations.csv").exists() else pd.DataFrame()

# API Key middleware
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path in ["/", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return await call_next(request)

# Pydantic models
class OptimizeRequest(BaseModel):
    n: int = 5

class BriefRequest(BaseModel):
    stats: Dict[str, Any]
    optimizer_results: List[Dict[str, Any]] = []

# Endpoints
@app.get("/api/data")
def get_data():
    """Return all DAs and EDs"""
    return {
        "das": len(da_data),
        "eds": len(ed_data),
        "total_population": int(da_data["population"].sum()) if not da_data.empty else 5538579,
        "stats": {
            "within_2hr": 2427910,
            "beyond_2hr": 3110669,
            "pct_covered": 43.8
        }
    }

@app.post("/api/optimize")
def optimize(req: OptimizeRequest):
    """Greedy facility placement optimization"""
    from optimizer import optimize as run_optimizer
    result = run_optimizer(req)
    return result

@app.post("/api/brief")
def generate_brief(req: BriefRequest):
    """Generate frontier Claude policy brief (streaming)"""
    def stream_brief():
        stats_str = json.dumps(req.stats, indent=2)
        locations_str = json.dumps(req.optimizer_results[:3], indent=2) if req.optimizer_results else "No specific locations"
        
        prompt = f"""You are a healthcare policy analyst specializing in rural surgical access in Canada.

Given these facility placement statistics:
{stats_str}

Top recommended facility locations:
{locations_str}

Generate a concise, 500-800 word policy brief for Canadian provincial health authorities addressing:
1. Current access gaps
2. Recommended facility placements
3. Impact on underserved populations (especially First Nations communities)
4. Implementation priorities
5. Equity considerations

Start with an Executive Summary, then provide Key Findings and Recommendations."""

        with anthropic_client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text
    
    return StreamingResponse(stream_brief(), media_type="text/plain")

@app.post("/api/brief-finetuned")
def generate_brief_finetuned(req: BriefRequest):
    """Generate fine-tuned Qwen policy brief, fallback to Claude"""
    try:
        stats_str = json.dumps(req.stats, indent=2)
        locations_str = json.dumps(req.optimizer_results[:3], indent=2) if req.optimizer_results else "No specific locations"
        
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
            locations_str = json.dumps(req.optimizer_results[:3], indent=2) if req.optimizer_results else "No specific locations"
            
            prompt = f"""You are a healthcare policy analyst specializing in rural surgical access in Canada.

Given these facility placement statistics:
{stats_str}

Top recommended facility locations:
{locations_str}

Generate a policy brief for Canadian health authorities."""

            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {"brief": response.content[0].text, "model": "claude-fallback"}
        except Exception as fallback_error:
            return {"error": f"Both models failed: {str(fallback_error)}", "model": "error"}

@app.get("/api/workforce-alignment")
def get_workforce():
    """Canadian physician supply by province"""
    return {
        "metadata": {
            "data_source": "Canadian Institute for Health Information (CIHI) 2024",
        },
        "provincial_data": [
            {"province": "Ontario", "pruid": "ON", "surgeons_per_100k": 2.9},
            {"province": "British Columbia", "pruid": "BC", "surgeons_per_100k": 3.7},
            {"province": "Quebec", "pruid": "QC", "surgeons_per_100k": 3.7},
            {"province": "Alberta", "pruid": "AB", "surgeons_per_100k": 3.8},
            {"province": "Manitoba", "pruid": "MB", "surgeons_per_100k": 3.7},
            {"province": "Saskatchewan", "pruid": "SK", "surgeons_per_100k": 3.6},
        ]
    }

@app.get("/api/seasonal-access")
def get_seasonal_access():
    """Winter road and ice road access"""
    return {
        "national_summary": {
            "winter_road_coverage_pct": 62.0,
            "summer_road_coverage_pct": 48.5,
            "population_seasonally_isolated": 145000,
            "affected_first_nations_estimate": 287,
        },
        "critical_ice_roads": [
            "Tibbitt-Contwoy corridor (NWT)",
            "Winter roads to Beauval, Fond du Lac (Saskatchewan)",
            "Churchill access road (Manitoba)"
        ]
    }

@app.get("/api/investment-analysis")
def get_investment_analysis():
    """Illustrative investment framework"""
    return {
        "metadata": {
            "status": "ILLUSTRATIVE EXAMPLE",
            "note": "Real implementation requires provincial consultation"
        },
        "example_regions": {
            "northern_ontario": {
                "access_gap_pop": 85000,
                "estimated_cost": "$45-60M",
                "priority": "HIGH"
            },
            "northern_manitoba": {
                "access_gap_pop": 32000,
                "estimated_cost": "$25-35M",
                "priority": "HIGH"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)