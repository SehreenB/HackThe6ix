"""
optimizer.py – Canadian Dissemination Area (DA) facility placement optimizer.
Uses real Canadian DA population, travel times, and discrete optimization.

UPDATED: now supports two access types:
  - "emergency": nearest 24-hr ED of any kind (original behaviour)
  - "surgical":  nearest 24-hr ED with 24/7 operating room capability

For "surgical", we don't have a precomputed DA-to-every-ED travel time matrix
(the source dataset only computed nearest-ED, not nearest-surgical-ED). So we
approximate surgical travel time using haversine distance to the nearest
surgical-flagged ED, converted to minutes via an assumed rural driving speed.
This is a clearly-labeled approximation — swap in real routing (OSRM/Valhalla)
against the surgical-only facility list if time allows.

Known upstream data gaps (labeled, not silently propagated):
  - TERRITORY TRAVEL TIMES: The figshare DA_Centroid_to_24hrED.csv source file
    (DOI 10.6084/m9.figshare.24082158) contains no rows for NT, NU, or YT.
    All 205 inhabited territory DAs carry Total_Minutes = 9999.0, a sentinel
    written by the join script's fillna(9999). This is defensible — "no road
    route exists" reasonably means "beyond any threshold" — but it must be
    disclosed, not presented as a measured travel time.
  - OR-CAPABILITY FLAGS: ED_locations.csv has no is_surgical column. Surgical
    mode uses a seeded-random 30% placeholder, flagged via data_quality_warning.
"""

import math
from pathlib import Path
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

router = APIRouter()

_DATA_DIR = Path(__file__).parent / "data"
_WORKING_DATA = _DATA_DIR / "da_working_dataset.csv"
_ED_DATA = _DATA_DIR / "ED_locations.csv"

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
RADIUS_MINUTES = 120  # 2-hour threshold
CANDIDATE_THRESHOLD_MINUTES = 120  # DAs beyond this are candidates for new facilities
CANDIDATE_FLOOR_POP = 500  # Minimum population in a candidate DA cluster
DISTANCE_RADIUS_KM = 150  # Radius within which a new facility covers unserved DAs

# Sentinel value written by the join script (build_working_dataset.py fillna)
# for DAs whose province is absent from the figshare travel time source.
# Currently: all NT/NU/YT DAs (205 inhabited rows, ~118k people).
# This is an upstream gap in figshare DOI 10.6084/m9.figshare.24082158 —
# those territories simply have no rows in the source file.
TRAVEL_TIME_SENTINEL = 9999.0
TERRITORY_PRUIDS_NO_ROUTING = {"NT", "NU", "YT"}  # PRUIDs absent from figshare travel time file

# Assumed average rural driving speed (km/h) used ONLY to approximate
# DA -> nearest-surgical-ED travel time, since no real routing exists for
# the surgical-only facility subset. Replace with real routing if time allows.
ASSUMED_RURAL_SPEED_KMH = 70

PROVINCES_SHORTNAME = {
    "ON": "Ontario",
    "BC": "British Columbia",
    "AB": "Alberta",
    "MB": "Manitoba",
    "SK": "Saskatchewan",
    "QC": "Quebec",
}


# ─────────────────────────────────────────────────────────────────────────────
# Request schema
# ─────────────────────────────────────────────────────────────────────────────
class OptimizeRequest(BaseModel):
    n: int = Field(..., ge=1, le=50)
    access_type: str = Field(
        default="emergency",
        description='Either "emergency" (any 24-hr ED) or "surgical" (24-hr ED with 24/7 OR)',
    )
    province: Optional[str] = Field(
        default=None,
        description="Optional PRUID to filter candidate placements to a specific province",
    )
    weight_by_shortage: bool = Field(
        default=False,
        description="Multiply candidate population gain by a shortage factor derived from province physician supply",
    )

    class Config:
        json_schema_extra = {
            "example": {"n": 5, "access_type": "surgical", "province": "ON", "weight_by_shortage": True}
        }


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute great-circle distance in km."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


def _get_province_name(pruid: str) -> str:
    """Map PRUID to province name."""
    return PROVINCES_SHORTNAME.get(pruid, f"Province {pruid}")


def _load_eds() -> pd.DataFrame:
    """
    Load ED locations with an is_surgical flag.

    If the CSV already has an `is_surgical` column (real data, sourced from
    provincial health authority OR listings), use it directly.

    If not present (e.g. still on placeholder data), fall back to a seeded,
    clearly-labeled placeholder classification so the code path is testable
    end-to-end. THIS MUST BE REPLACED before relying on results for a demo
    that claims real OR-capability data.
    """
    eds = pd.read_csv(_ED_DATA)

    if "is_surgical" not in eds.columns:
        rng = np.random.default_rng(seed=42)  # seeded for reproducibility
        eds["is_surgical"] = rng.random(len(eds)) < 0.30  # PLACEHOLDER: ~30% flagged as surgical-capable
        eds["_is_surgical_placeholder"] = True
    else:
        eds["_is_surgical_placeholder"] = False

    return eds


def _recompute_surgical_travel_time(df: pd.DataFrame, surgical_eds: pd.DataFrame) -> pd.DataFrame:
    """
    Approximate each DA's travel time to the nearest surgical-capable ED.

    Uses haversine distance to the nearest surgical ED, converted to minutes
    via ASSUMED_RURAL_SPEED_KMH. This is an approximation flagged for
    replacement with real routing (OSRM/Valhalla against the surgical-only
    facility subset) if time allows.
    """
    if surgical_eds.empty:
        # No surgical-capable EDs at all -> everyone is "beyond" for this access type
        df = df.copy()
        df["Total_Minutes"] = np.inf
        return df

    ed_lats = surgical_eds["y"].to_numpy()
    ed_lngs = surgical_eds["x"].to_numpy()

    def nearest_minutes(row):
        dists = np.array([
            _haversine_km(row["y"], row["x"], lat, lng)
            for lat, lng in zip(ed_lats, ed_lngs)
        ])
        nearest_km = dists.min()
        return (nearest_km / ASSUMED_RURAL_SPEED_KMH) * 60.0

    df = df.copy()
    df["Total_Minutes"] = df.apply(nearest_minutes, axis=1)
    return df


def _check_sentinel_travel_times(df: pd.DataFrame) -> Optional[str]:
    """
    Detect DAs that carry the 9999 sentinel value and return a disclosure
    string, or None if all travel times are real measured values.

    Sentinel DAs fall into two groups:
      - Territory DAs (NT/NU/YT): entirely absent from the figshare travel
        time source (DOI 10.6084/m9.figshare.24082158).
      - Non-territory isolated DAs (NL, QC, BC, MB, SK): present in the
        centroid file but unmatched in the travel time file, likely coastal
        islands or communities with no road connection to any 24-hr ED.
    Both groups receive the same sentinel from the join script's fillna(9999).
    """
    sentinel_rows = df[df["Total_Minutes"] >= TRAVEL_TIME_SENTINEL]
    if sentinel_rows.empty:
        return None

    by_prov = sentinel_rows.groupby("PRUID")["Population"].agg(["count", "sum"])
    affected_pop = int(sentinel_rows["Population"].sum())
    affected_das = len(sentinel_rows)
    prov_summary = ", ".join(
        f"{pruid} ({row['count']} DAs, {int(row['sum']):,} people)"
        for pruid, row in by_prov.iterrows()
    )

    return (
        f"NO-ROAD-NETWORK DATA GAP: {affected_das} DAs across {len(by_prov)} "
        f"provinces/territories ({affected_pop:,} people total) carry a sentinel "
        f"value of {int(TRAVEL_TIME_SENTINEL)} minutes \u2014 not a real measured "
        f"travel time. These DAs were absent from the figshare travel time source "
        f"(DOI 10.6084/m9.figshare.24082158), indicating no road-network route to "
        f"any 24-hr ED. Breakdown: {prov_summary}. "
        f"These DAs are excluded from facility-placement optimization (see "
        f"excluded_no_road_network in this response) and require a different "
        f"intervention strategy."
    )


def _split_road_network_scope(
    df: pd.DataFrame,
) -> tuple:
    """
    Split DAs into those covered by the road-network travel-time analysis
    vs. those with no routing at all (sentinel value = TRAVEL_TIME_SENTINEL).

    Returns (in_scope_df, no_road_network_df).

    The sentinel applies to ALL DAs absent from the figshare travel time file,
    not only territory DAs. There are 243 such DAs total (~136k people):
      - 205 in NT/NU/YT (territories entirely absent from the source)
      -  38 in NL/QC/BC/MB/SK (isolated communities, likely coastal islands
         or communities with no road route to any 24-hr ED)

    The optimizer's coverage model assumes a connected road network (coverage
    radius is road-distance based). Including sentinel DAs would either produce
    phantom placements (haversine distance with no actual road access) or let
    sentinel values dominate the unserved ranking by magnitude alone.
    """
    no_road_network = df[df["Total_Minutes"] >= TRAVEL_TIME_SENTINEL]
    in_scope = df.drop(no_road_network.index)
    return in_scope, no_road_network


def _generate_candidates(df: pd.DataFrame) -> List[Dict]:
    """
    Generate candidate sites from unserved DAs (travel_time > 120 min).
    Called only on the in-scope (road-connected) subset after
    _split_road_network_scope has removed territory sentinel rows.
    """
    unserved = df[df["Total_Minutes"] > CANDIDATE_THRESHOLD_MINUTES].copy()
    unserved = unserved[unserved["Population"] > 0]
    candidates = unserved.nlargest(500, "Population").to_dict("records")
    return candidates


# ─────────────────────────────────────────────────────────────────────────────
# Route: POST /api/optimize
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/api/optimize")
def optimize(body: OptimizeRequest):
    """
    Greedy DA-level facility placement optimizer.

    access_type="emergency" (default): uses the precomputed nearest-any-ED
    travel time exactly as before.

    access_type="surgical": filters EDs to the surgical-capable subset and
    approximates travel time to the nearest one (see _recompute_surgical_travel_time).
    """
    if body.access_type not in ("emergency", "surgical"):
        raise HTTPException(status_code=400, detail='access_type must be "emergency" or "surgical"')

    if not _WORKING_DATA.exists():
        raise HTTPException(status_code=503, detail="Working dataset not found")

    df = pd.read_csv(_WORKING_DATA)
    if df.empty:
        raise HTTPException(status_code=400, detail="No data loaded")

    # Check for sentinel travel times (territory upstream data gap) up front
    # so the warning is present regardless of access_type
    territory_sentinel_warning = _check_sentinel_travel_times(df)

    # Exclude territory DAs from the placement model entirely.
    # Their sentinel travel times (9999) are not road-network results, and
    # including them would either produce phantom facility placements (haversine
    # distance with no road access) or let them dominate the unserved ranking
    # by sentinel magnitude rather than real routing comparison.
    # The excluded population is surfaced in the response as its own category.
    df, no_road_network_df = _split_road_network_scope(df)

    if body.province:
        df = df[df["PRUID"] == body.province]
        no_road_network_df = no_road_network_df[no_road_network_df["PRUID"] == body.province]

    no_road_network_pop = int(no_road_network_df["Population"].sum())
    no_road_network_das = len(no_road_network_df)

    shortage_weights = {}
    unavailable_weighting_pruids = set()
    if body.weight_by_shortage:
        from endpoints.workforce import get_workforce_alignment
        wf_data = get_workforce_alignment()
        for prov_data in wf_data.get("provincial_data", []):
            shortage_weights[prov_data["pruid"]] = 241.0 / prov_data["physicians_per_100k"]

    used_placeholder_or_data = False

    if body.access_type == "surgical":
        eds = _load_eds()
        used_placeholder_or_data = bool(eds["_is_surgical_placeholder"].iloc[0]) if len(eds) else False
        surgical_eds = eds[eds["is_surgical"]]
        df = _recompute_surgical_travel_time(df, surgical_eds)
    # else: "emergency" uses df["Total_Minutes"] as-is (nearest any ED, precomputed)

    # ─────────────────────────────────────────────────────────────────
    # Initialize
    # ─────────────────────────────────────────────────────────────────
    total_pop = df["Population"].sum()

    current_within = df[df["Total_Minutes"] <= RADIUS_MINUTES].copy()
    current_within_pop = current_within["Population"].sum()

    candidates = _generate_candidates(df)

    placed = []
    coverage_curve = []

    # ─────────────────────────────────────────────────────────────────
    # Greedy placement loop
    # ─────────────────────────────────────────────────────────────────
    for iteration in range(body.n):
        if not candidates:
            break

        unserved = df[~df["DAUID"].isin(current_within["DAUID"])].copy()
        unserved_pop = unserved["Population"].sum()

        if unserved_pop <= 0:
            break

        best_gain = -1
        best_raw_pop = -1
        best_candidate = None
        best_newly_covered = None

        for candidate in candidates:
            cand_lat, cand_lng = candidate["y"], candidate["x"]
            cand_pruid = candidate.get("PRUID", "XX")

            distances = unserved.apply(
                lambda row: _haversine_km(cand_lat, cand_lng, row["y"], row["x"]),
                axis=1
            )

            newly_covered_mask = distances <= DISTANCE_RADIUS_KM
            newly_covered_pop = unserved[newly_covered_mask]["Population"].sum()

            weight = 1.0
            if body.weight_by_shortage:
                if cand_pruid in shortage_weights:
                    weight = shortage_weights[cand_pruid]
                else:
                    unavailable_weighting_pruids.add(cand_pruid)
                    
            weighted_gain = newly_covered_pop * weight

            if weighted_gain > best_gain:
                best_gain = weighted_gain
                best_raw_pop = newly_covered_pop
                best_candidate = candidate
                best_newly_covered = unserved[newly_covered_mask]

        if best_candidate is None or best_gain <= 0:
            break

        placed.append({
            "lat": round(float(best_candidate["y"]), 6),
            "lng": round(float(best_candidate["x"]), 6),
            "pop_gained": int(best_raw_pop),
            "weighted_score": round(best_gain, 2) if body.weight_by_shortage else None,
            "dauid": int(best_candidate["DAUID"]),
            "province": _get_province_name(best_candidate.get("PRUID", "XX")),
            "access_type": body.access_type,
        })

        current_within = pd.concat([current_within, best_newly_covered], ignore_index=True)
        current_within = current_within.drop_duplicates(subset=["DAUID"])
        current_within_pop = current_within["Population"].sum()

        candidates = [c for c in candidates if c["DAUID"] != best_candidate["DAUID"]]

        coverage_pct = round(float(current_within_pop / total_pop * 100), 1) if total_pop else 0.0
        coverage_curve.append({
            "n_facilities": len(placed),
            "pct_covered": coverage_pct,
            "pop_gained": int(best_raw_pop),
        })

    # ─────────────────────────────────────────────────────────────────
    # Build final stats and DA-level coverage map
    # ─────────────────────────────────────────────────────────────────
    within_pop = int(current_within_pop)
    beyond_pop = int(total_pop - within_pop)
    pct_covered = round(float(within_pop / total_pop * 100), 1) if total_pop else 0.0

    da_coverage = []
    for _, da_row in df.iterrows():
        is_served = da_row["DAUID"] in current_within["DAUID"].values
        is_sentinel = da_row["Total_Minutes"] >= TRAVEL_TIME_SENTINEL
        da_coverage.append({
            "dauid": int(da_row["DAUID"]),
            "pruid": da_row.get("PRUID", "XX"),
            "within_2hr": bool(is_served),
            # None when isinf (surgical mode), sentinel integer omitted in favour of
            # travel_time_is_sentinel flag so frontends don't render "9999 minutes"
            "travel_time_minutes": None if (math.isinf(da_row["Total_Minutes"]) or is_sentinel)
                                   else int(da_row["Total_Minutes"]),
            # True for territory DAs (NT/NU/YT) whose travel time is a fill-sentinel,
            # not a real routing result. See TERRITORY_PRUIDS_NO_ROUTING in this file.
            "travel_time_is_sentinel": bool(is_sentinel),
            "population": int(da_row["Population"]),
        })

    # Build data quality warnings — one list covering all active gaps
    warnings = []
    if body.access_type == "surgical" and used_placeholder_or_data:
        warnings.append(
            "OR-CAPABILITY PLACEHOLDER: Surgical mode is using seeded-random ~30% "
            "OR-capability flags, not real provincial health authority data. "
            "Travel times are haversine-approximated, not real routing. "
            "Replace before citing surgical access results."
        )
    if territory_sentinel_warning:
        warnings.append(territory_sentinel_warning)

    response_content = {
        "access_type": body.access_type,
        "locations": placed,
        "updated_stats": {
            # Covers road-connected DAs only (territories excluded below)
            "total_pop": int(total_pop),
            "within_2hr": within_pop,
            "beyond_2hr": beyond_pop,
            "pct_covered": pct_covered,
            "pct_beyond": round(100.0 - pct_covered, 1),
        },
        "coverage_curve": coverage_curve,
        "da_coverage_map": da_coverage,
        # Communities with no road-network routing in the source data.
        # Excluded from placement math; require a different intervention.
        # Includes territories (NT/NU/YT) and isolated communities in NL/QC/BC/MB/SK
        # that were also absent from the figshare travel time file.
        "excluded_no_road_network": {
            "population": no_road_network_pop,
            "n_das": no_road_network_das,
            "provinces": sorted(no_road_network_df["Province"].unique().tolist()) if not no_road_network_df.empty and "Province" in no_road_network_df.columns else [],
            "note": (
                "These communities have no road-network routing in the source dataset "
                "(McGaughey & Peters, 2024, DOI 10.6084/m9.figshare.24082158) and are "
                "not included in facility-placement optimization, since the model's "
                "coverage radius assumes road access. Includes all three territories "
                "(NT/NU/YT) plus 38 isolated DAs in NL, QC, BC, MB, and SK. "
                "These communities require a different strategy: air ambulance, "
                "telemedicine, or seasonal winter-road infrastructure investment, "
                "not a new facility sited by road distance."
            ),
        },
        # None when no gaps active; a list of strings when one or more gaps apply.
        # Each entry names the gap, its scope, and what the limitation means.
        "data_quality_warnings": warnings if warnings else None,
        # Legacy single-warning field kept for backwards compatibility
        "data_quality_warning": warnings[0] if warnings else None,
    }

    if body.weight_by_shortage and unavailable_weighting_pruids:
        response_content["shortage_data_unavailable"] = sorted(list(unavailable_weighting_pruids))

    return JSONResponse(content=response_content)
