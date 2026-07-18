"""
data.py – Load Canadian DA population and travel time data.
Replaces the Liberia hospitals.geojson + raster setup.
"""

import json
import os
import pandas as pd
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
_WORKING_CSV = _DATA_DIR / "da_working_dataset.csv"
_ED_CSV = _DATA_DIR / "ED_locations.csv"


def load_das():
    """Load all Dissemination Areas with population and travel times."""
    try:
        df = pd.read_csv(_WORKING_CSV)
        
        das = []
        for _, row in df.iterrows():
            das.append({
                "dauid": int(row["DAUID"]),
                "pruid": row.get("PRUID", "XX"),
                "lat": float(row["y"]),
                "lng": float(row["x"]),
                "population": int(row["Population"]),
                "travel_time_minutes": int(row["Total_Minutes"]),
                "within_2hr": row["Total_Minutes"] <= 120,
            })
        
        return das
    except Exception as e:
        print(f"Warning: Could not load DAs: {e}")
        return []


def load_eds():
    """Load 24-hour Emergency Department locations."""
    try:
        df = pd.read_csv(_ED_CSV)
        
        eds = []
        for _, row in df.iterrows():
            eds.append({
                "ed_id": int(row["ED_ID"]),
                "name": str(row.get("ED_Name", "Hospital")),
                "pruid": row.get("PRUID", "XX"),
                "lat": float(row.get("y", row.get("lat"))),
                "lng": float(row.get("x", row.get("lng"))),
            })
        
        return eds
    except Exception as e:
        print(f"Warning: Could not load EDs: {e}")
        return []


def load_coverage_stats():
    """Compute initial coverage statistics from the dataset."""
    try:
        df = pd.read_csv(_WORKING_CSV)
        
        total_pop = int(df["Population"].sum())
        within_2hr_pop = int(df[df["Total_Minutes"] <= 120]["Population"].sum())
        beyond_2hr_pop = total_pop - within_2hr_pop
        
        return {
            "total_pop": total_pop,
            "within_2hr": within_2hr_pop,
            "beyond_2hr": beyond_2hr_pop,
            "pct_covered": round(float(within_2hr_pop / total_pop * 100), 1) if total_pop else 0.0,
            "pct_beyond": round(float(beyond_2hr_pop / total_pop * 100), 1) if total_pop else 0.0,
        }
    except Exception as e:
        print(f"Warning: Could not compute stats: {e}")
        return {
            "total_pop": 0,
            "within_2hr": 0,
            "beyond_2hr": 0,
            "pct_covered": 0.0,
            "pct_beyond": 0.0,
        }


# Cache on module load
DAS = load_das()
EDS = load_eds()
STATS = load_coverage_stats()


def get_data():
    """Return initial dataset for /api/data endpoint."""
    return {
        "stats": STATS,
        "das": DAS,
        "eds": EDS,
        "metadata": {
            "data_source": "Statistics Canada 2021 Census, McGaughey 2024 travel times",
            "n_dissemination_areas": len(DAS),
            "n_emergency_departments": len(EDS),
            "coverage_threshold_minutes": 120,
            "note": "Canadian surgical access data using real DA-level population and travel time.",
        },
    }
