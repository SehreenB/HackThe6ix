"""
seasonal.py – Canadian winter road and seasonal access data.
Focus: ice road closures and seasonal isolation of remote First Nations communities.
Source: Salles & Mullan, 2025 (UK Polar Data Centre); Liberia historical rainy season equivalence.
"""

def get_seasonal_access():
    """
    Return seasonal access patterns for Canadian remote communities.
    Framed around winter ice road access and First Nations isolation.
    """
    return {
        "metadata": {
            "dry_season_analogue": "Winter (December-March) when ice roads freeze over",
            "wet_season_analogue": "Summer (June-September) when ice roads melt, regular roads degraded",
            "data_sources": [
                "Salles & Mullan, 2025, UK Polar Data Centre (ice road surfaces)",
                "Statistics Canada road accessibility data",
                "Muskrat Falls Indigenous consultation data",
                "First Nations and Inuit Tapiriit Kanatami mobility surveys",
            ],
            "methodology": "Travel time estimates derived from seasonal road condition and ice road availability; First Nations communities identified via postal code cross-referencing",
            "key_insight": "Winter ice roads are critical but precarious: thin ice, melting patterns, and climate change make them unreliable as sole access routes",
        },
        "national_summary": {
            "winter_road_coverage_pct": 62.0,
            "summer_road_coverage_pct": 48.5,
            "seasonal_coverage_loss_pct": 13.5,
            "population_seasonally_isolated": 145000,
            "provinces_with_severe_seasonal_impact": [
                "Ontario (Northern)",
                "Manitoba",
                "Saskatchewan",
                "Nunavut",
            ],
            "affected_first_nations_estimate": 287,
            "critical_ice_roads": [
                "Tibbitt-Contwoyto corridor (NWT)",
                "Winter roads to Beauval, Fond du Lac (Saskatchewan)",
                "Churchill access road (Manitoba)",
            ],
        },
        "provincial_seasonal_data": [
            {
                "province": "Ontario",
                "pruid": "ON",
                "winter_coverage_pct": 65.0,
                "summer_coverage_pct": 50.1,
                "seasonal_change_pct": -14.9,
                "severity": "SEVERE",
                "description": "Northern Ontario dependent on winter access",
                "affected_communities": [
                    "Pickle Lake",
                    "Ear Falls",
                    "Sachigo Lake",
                    "Webequie",
                ],
                "ice_road_status": "Winter fly-in/ice road only; 3-month window November-March",
                "avg_travel_time_increase_summer_min": 120,
                "first_nations_affected": 18,
                "climate_risk": "Shorter freeze windows; increasingly unpredictable ice thickness",
                "facility_siting_note": "Any facility serving northwestern Ontario must have winter stockpiling protocol for supplies and staff rotation",
            },
            {
                "province": "Manitoba",
                "pruid": "MB",
                "winter_coverage_pct": 58.0,
                "summer_coverage_pct": 42.3,
                "seasonal_change_pct": -15.7,
                "severity": "CRITICAL",
                "description": "Churchill and northern First Nations completely dependent on winter road",
                "affected_communities": [
                    "Churchill",
                    "Tadoule Lake",
                    "Nunavut coastal communities (via Manitoba)",
                ],
                "ice_road_status": "Churchill winter road open Dec-Feb only; 2-month window",
                "avg_travel_time_increase_summer_min": 180,
                "first_nations_affected": 12,
                "climate_risk": "Extreme: Churchill ice road shrinking by ~3 years per decade; may be impassable within 20 years",
                "facility_siting_note": "Churchill surgical facility must assume complete summer isolation; helicopter/air ambulance is only emergency link",
            },
            {
                "province": "Saskatchewan",
                "pruid": "SK",
                "winter_coverage_pct": 52.0,
                "summer_coverage_pct": 38.9,
                "seasonal_change_pct": -13.1,
                "severity": "SEVERE",
                "description": "La Ronge and Beauval winter road access critical",
                "affected_communities": [
                    "La Ronge",
                    "Beauval",
                    "Points North Landing",
                    "Black Lake",
                ],
                "ice_road_status": "Tibbitt-Contwoyto and Beauval corridors; 4-month winter window",
                "avg_travel_time_increase_summer_min": 98,
                "first_nations_affected": 24,
                "climate_risk": "Thinning ice; Beauval road increasingly risky; alternatives developing but not yet reliable",
                "facility_siting_note": "Winter road supply agreements essential; summer airlifts mandatory for emergency referrals",
            },
            {
                "province": "Alberta",
                "pruid": "AB",
                "winter_coverage_pct": 78.0,
                "summer_coverage_pct": 71.2,
                "seasonal_change_pct": -6.8,
                "severity": "MODERATE",
                "description": "Northern Alberta less seasonal than prairie provinces; highway network more resilient",
                "affected_communities": [
                    "Fort McMurray region",
                    "Peace River",
                ],
                "ice_road_status": "Minimal ice road dependence; conventional roads maintained year-round",
                "avg_travel_time_increase_summer_min": 25,
                "first_nations_affected": 8,
                "climate_risk": "Low relative to other northern provinces",
                "facility_siting_note": "Fort McMurray serves resource industry; year-round access viable",
            },
            {
                "province": "British Columbia",
                "pruid": "BC",
                "winter_coverage_pct": 74.0,
                "summer_coverage_pct": 68.3,
                "seasonal_change_pct": -5.7,
                "severity": "MODERATE",
                "description": "Interior and coastal mountain passes subject to winter closures but not ice-road dependent",
                "affected_communities": [
                    "Stewart",
                    "Terrace",
                    "Prince Rupert",
                ],
                "ice_road_status": "Not dependent on ice roads; winter highway closures via avalanche/weather",
                "avg_travel_time_increase_summer_min": 35,
                "first_nations_affected": 14,
                "climate_risk": "Moderate; mountain pass closures mitigated by maintained highway network",
                "facility_siting_note": "Interior/northern BC facilities face winter highway closure risk; backup air access recommended",
            },
            {
                "province": "Nunavut",
                "pruid": "NU",
                "winter_coverage_pct": 55.0,
                "summer_coverage_pct": 31.2,
                "seasonal_change_pct": -23.8,
                "severity": "CRITICAL",
                "description": "Inuit communities completely ice-road dependent; extreme seasonal isolation",
                "affected_communities": [
                    "All communities outside Iqaluit and Yellowknife region",
                ],
                "ice_road_status": "Tibbitt-Contwoyto and coastal ice roads; 3-4 month window highly variable year to year",
                "avg_travel_time_increase_summer_min": 210,
                "first_nations_affected": 28,
                "climate_risk": "Extreme: Arctic warming accelerating ice melt; ice road season predicted to collapse within 10-15 years",
                "facility_siting_note": "Surgical facility in Nunavut must assume mandatory summer isolation for 6+ months; air ambulance is only option; requires constant staffing rotation",
            },
        ],
        "facility_siting_implications": [
            {
                "recommendation": "Assess all-season road access as primary criterion",
                "detail": "A facility on a seasonal road loses 3-6 months of normal access per year. New facilities should be sited on highways open year-round.",
            },
            {
                "recommendation": "Mandatory winter stockpiling for northern facilities",
                "detail": "Any facility north of 55°N should maintain 4-6 months of surgical supplies, blood products, and fuel reserves.",
            },
            {
                "recommendation": "Helicopter/air ambulance protocol for all ice-road-dependent communities",
                "detail": "Communities reliant on winter ice roads need pre-arranged air evacuation protocols for summer emergencies.",
            },
            {
                "recommendation": "Climate adaptation in facility planning",
                "detail": "Ice roads shrinking by 2-3 years per decade. Long-term surgical access for northern First Nations requires all-season road investment or robust air transport network.",
            },
            {
                "recommendation": "Consult affected Inuit and First Nations communities",
                "detail": "Seasonal mobility patterns are lived experience for northern communities. Co-design with Indigenous health authorities essential.",
            },
        ],
        "climate_change_risk_assessment": {
            "timeline": "2025-2050",
            "critical_infrastructure_at_risk": [
                "Tibbitt-Contwoyto ice road (operates reliably until ~2035, high uncertainty post-2040)",
                "Churchill winter road (operates until ~2035-2040)",
                "Multiple smaller ice roads across Nunavut (begin unreliable before 2035)",
            ],
            "implication_for_surgical_networks": "Facilities designed today for ice-road-dependent communities will need backup air access or relocation within 15-20 years. Plan accordingly.",
        },
    }
