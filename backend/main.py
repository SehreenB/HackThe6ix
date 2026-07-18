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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(optimizer_router)

@app.get("/api/data")
def api_data():
    return get_data()

class BriefRequest(BaseModel):
    stats: dict
    optimizer_results: list

@app.post("/api/brief")
def api_brief(req: BriefRequest):
    return StreamingResponse(
        generate_brief(req.stats, req.optimizer_results),
        media_type="text/plain"
    )

@app.get("/api/investment-analysis")
def api_investment():
    return get_investment_analysis()

@app.get("/api/workforce-alignment")
def api_workforce():
    return get_workforce_alignment()

@app.get("/api/seasonal-access")
def api_seasonal():
    return get_seasonal_access()
