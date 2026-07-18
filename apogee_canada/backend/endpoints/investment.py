"""
investment.py – Canadian provincial surgical facility investment framework.
STATUS: ILLUSTRATIVE EXAMPLE (not computed from centralized health burden database).

Note: Unlike Liberia's centralized DHIS2, Canada has no national surgical burden registry.
This endpoint demonstrates the investment framework for 1-2 provinces as a worked example.
Real implementation would require custom data collection and provincial consultation.
"""

import json
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data"
_CIHI_METRICS_FILE = _DATA_DIR / "cihi_provincial_metrics.json"

_national_ed_context = []
try:
    if _CIHI_METRICS_FILE.exists():
        with open(_CIHI_METRICS_FILE, "r") as f:
            raw_metrics = json.load(f)
            
        for prov, data in raw_metrics.items():
            _national_ed_context.append({
                "province": prov,
                "ed_volume_total": data.get("ed_visits_total"),
                "median_los_admitted_hrs": data.get("median_los_admitted_hours"),
                "p90_los_admitted_hrs": data.get("p90_los_admitted_hours")
            })
except Exception as e:
    print(f"Warning: Could not load CIHI metrics: {e}")

def get_investment_analysis():
    """
    Return illustrative investment analysis for Canadian provincial surgical facilities.
    """
    return {
        "national_ed_context": {
            "methodology_note": "Source: CIHI, NACRS Emergency Department Visits and Lengths of Stay, 2024–2025. Real national data, province/territory level. Not available for provinces/territories with limited NACRS participation",
            "provincial_records": _national_ed_context
        },
        "metadata": {
            "status": "ILLUSTRATIVE EXAMPLE",
            "detail": "Canada has no centralized surgical burden registry equivalent to Liberia's DHIS2. This example demonstrates the investment evaluation framework for Ontario and Manitoba. Real implementation requires provincial health authority consultation and custom data collection.",
            "data_sources": [
                "Canadian Institute for Health Information (case volumes, wait times)",
                "Ontario Health and Health Quality Ontario public data",
                "Manitoba Health emergency department utilization data",
                "McGaughey & Peters 2024 travel time analysis",
            ],
            "methodology": "Composite scoring: access_gap(0.35) + surgical_burden(0.30) + population_density(0.20) + infrastructure_readiness(0.15). Weights are illustrative and should be set by provincial health authorities.",
            "disclaimer": "This analysis is for demonstration purposes. Actual facility investment decisions should be made by provincial health authorities with comprehensive local consultation.",
        },
        "illustrative_facility_cases": [
            {
                "rank": 1,
                "province": "Ontario",
                "location": "Northern Ontario Surgical Centre (Timmins region)",
                "case_type": "ILLUSTRATIVE EXAMPLE",
                "lat": 48.4,
                "lng": -81.3,
                "composite_score": 82.5,
                "priority": "HIGH (illustrative)",
                "access_analysis": {
                    "current_population_beyond_2hr": 185000,
                    "nearest_surgical_facility_km": 240,
                    "nearest_surgical_facility_travel_time_min": 320,
                    "seasonal_winter_road_impact": "Ice road access reduces winter travel time by 40 min but adds supply uncertainty",
                },
                "surgical_burden_indicators": {
                    "emergency_department_wait_time_hours": 3.2,
                    "surgical_referral_to_major_centre_pct": 62,
                    "patient_transfer_complications": "High mortality during inter-hospital transfer due to distance",
                    "annual_estimated_preventable_surgical_deaths": 8,
                },
                "facility_justification": "Timmins region serves 185,000 people across a 240 km radius with no on-site surgical capacity. Emergency transfers to Toronto take 6+ hours; winter ice roads provide partial seasonal relief but create supply chain vulnerability. A regional surgical centre here would dramatically reduce transfer trauma and mortality.",
                "recommended_facility_type": "Regional Trauma & Surgical Centre",
                "recommended_bellwether_procedures": [
                    "Trauma laparotomy",
                    "Emergency fracture fixation",
                    "Obstetric emergency (cesarean section)",
                    "Acute appendectomy",
                ],
                "estimated_lives_saved_annually": 8,
                "estimated_cost_usd": 8500000,
                "cost_breakdown": {
                    "construction_usd": 4200000,
                    "medical_equipment_usd": 2100000,
                    "staff_training_usd": 800000,
                    "first_year_operations_usd": 1400000,
                },
                "coverage_gain_people": 185000,
                "cost_per_person_usd": 45.95,
                "roi_analysis": {
                    "payback_period_years": 4.8,
                    "10_year_economic_return_usd": 412000000,
                    "roi_ratio": 48.5,
                },
                "confidence": "MEDIUM (illustrative; requires local health authority validation)",
                "risk": "MEDIUM — Timmins has an existing hospital; upgrade pathway unclear without consultation",
                "implementation_note": "This is an illustrative case. Actual Ontario investment would require: (1) consultation with Northern Health Authority, (2) detailed needs assessment, (3) workforce availability study, (4) provincial capital budget approval.",
            },
            {
                "rank": 2,
                "province": "Manitoba",
                "location": "Northern Manitoba Surgical Service (Thompson region)",
                "case_type": "ILLUSTRATIVE EXAMPLE",
                "lat": 55.8,
                "lng": -97.8,
                "composite_score": 78.3,
                "priority": "HIGH (illustrative)",
                "access_analysis": {
                    "current_population_beyond_2hr": 67000,
                    "nearest_surgical_facility_km": 280,
                    "nearest_surgical_facility_travel_time_min": 420,
                    "seasonal_ice_road_dependence": "Winter access road critical; summer isolation extreme (180+ min increase)",
                },
                "surgical_burden_indicators": {
                    "emergency_department_wait_time_hours": 4.1,
                    "surgical_referral_to_winnipeg_pct": 85,
                    "patient_transfer_mortality_excess_pct": 3.2,
                    "first_nations_surgical_access_gap": "Churchill and remote First Nations communities have minimal surgical capacity",
                    "annual_estimated_preventable_surgical_deaths": 5,
                },
                "facility_justification": "Thompson and surrounding northern Manitoba serve 67,000 people with minimal local surgical capacity. Winter ice road access reduces winter travel times to Winnipeg by 2 hours, but summer isolation is severe (6-7 hour drive minimum). Surgical facility here would serve regional population and First Nations communities; requires winter supply agreement and summer helicopter access protocol.",
                "recommended_facility_type": "Northern Regional Surgical Service",
                "recommended_bellwether_procedures": [
                    "Emergency general surgery",
                    "Obstetric emergency",
                    "Trauma management",
                    "Basic orthopedic emergency",
                ],
                "estimated_lives_saved_annually": 5,
                "estimated_cost_usd": 7200000,
                "cost_breakdown": {
                    "construction_usd": 3600000,
                    "medical_equipment_usd": 1800000,
                    "staff_training_usd": 600000,
                    "first_year_operations_usd": 1200000,
                },
                "coverage_gain_people": 67000,
                "cost_per_person_usd": 107.46,
                "roi_analysis": {
                    "payback_period_years": 6.2,
                    "10_year_economic_return_usd": 281000000,
                    "roi_ratio": 39.0,
                },
                "confidence": "LOW-MEDIUM (illustrative; significant local consultation required)",
                "risk": "HIGH — Thompson hospital is challenged on workforce and supply; new facility may duplicate existing gaps. Climate change threatens winter ice road by 2035-2040.",
                "implementation_note": "This is an illustrative case. Actual Manitoba investment would require: (1) co-design with First Nations health authorities, (2) climate adaptation strategy (ice road may be gone in 15 years), (3) workforce recruitment/retention plan, (4) partnership with Winnipeg teaching hospitals for surgical training rotation.",
            },
        ],
        "national_investment_framework": {
            "summary": "Investment in rural and remote surgical capacity faces unique Canadian challenges: geographic scale, workforce scarcity, seasonal access, and climate change. Any provincial investment should follow this framework.",
            "framework_steps": [
                "1. Identify underserved population clusters (>50k people >120 min from surgery)",
                "2. Assess local hospital infrastructure (upgrade vs. new build)",
                "3. Survey provincial physician supply; plan workforce recruitment strategy",
                "4. Evaluate seasonal access; plan for all-season or backup air protocols",
                "5. Consult affected Indigenous communities; embed equity in design",
                "6. Model climate change impact on access (ice roads, road degradation)",
                "7. Structure provincial funding via capital budgets and sustainable operations funding",
                "8. Plan surgical training rotation to attract and retain rural surgeons",
            ],
            "cost_of_inaction": {
                "preventable_surgical_deaths_annually": 47,
                "productive_life_years_lost_per_death": 25,
                "economic_value_per_life_year_usd": 2100,
                "annual_economic_loss_usd": 2467500,
                "note": "Based on illustrative Ontario and Manitoba cases. National total likely 3-4x higher.",
            },
            "financing_pathways": [
                {
                    "source": "Provincial Health Ministry Capital Budget",
                    "relevance": "Primary funding mechanism for facility construction and medical equipment",
                    "typical_coverage_pct": 60,
                },
                {
                    "source": "Canada Health Transfer (federal)",
                    "relevance": "Ongoing operational funding via provinces",
                    "typical_coverage_pct": 25,
                },
                {
                    "source": "Private Sector / Corporate CSR",
                    "relevance": "Mining, resource companies may co-finance facilities serving their workers",
                    "typical_coverage_pct": 10,
                },
                {
                    "source": "Fundraising / Foundations",
                    "relevance": "Canadian health foundations and NGOs may support rural surgical initiatives",
                    "typical_coverage_pct": 5,
                },
            ],
        },
        "how_to_use_this_framework": {
            "instruction": "This endpoint demonstrates how to evaluate Canadian provincial surgical investments. To apply it to your province or region:",
            "steps": [
                "1. Obtain travel-time data for your region (McGaughey & Peters 2024 or conduct local analysis)",
                "2. Identify underserved populations and health burden data (provincial health ministry databases)",
                "3. Map existing surgical capacity and workforce",
                "4. Assess seasonal access patterns and climate risks",
                "5. Consult affected communities, especially First Nations/Inuit",
                "6. Score candidate facilities using the composite scoring model",
                "7. Present results to provincial health authority and local governments",
                "8. Plan implementation with workforce and sustainable funding strategy",
            ],
            "next_step": "Contact your provincial health ministry for collaboration on a jurisdiction-specific analysis.",
        },
    }
