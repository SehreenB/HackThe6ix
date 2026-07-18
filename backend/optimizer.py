"""
optimizer.py – Scientist-defensible greedy facility placement optimizer.
Uses road-aware candidates, real population weights, and travel-time propagation.
"""

import math
from pathlib import Path
from typing import List

import numpy as np
import rasterio
from rasterio.transform import rowcol, xy
from rasterio.warp import reproject, Resampling
import geopandas as gpd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from skimage import measure

router = APIRouter()

_DATA_DIR = Path(__file__).parent / "data"
_TIF_PATH = _DATA_DIR / "surgical_travel_time.tif"
_WP_PATH  = _DATA_DIR / "lbr_ppp_2020_UNadj.tif"
_HOSPITALS_PATH = _DATA_DIR / "hospitals.geojson"

# ── Contour helper ─────────────────────────────────────────────────────────────
def compute_contour(cost_array, transform):
    covered = (cost_array <= 120) & (cost_array >= 0)
    try:
        raw_contours = measure.find_contours(covered.astype(float), level=0.5)
    except Exception:
        return None

    coordinates = []
    for contour in raw_contours:
        if len(contour) < 10:
            continue
        ring = []
        for r, c in contour:
            lng, lat = xy(transform, r, c)
            ring.append([round(float(lng), 4), round(float(lat), 4)])
        if ring:
            coordinates.append(ring)

    return {
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": coordinates
        },
        "properties": {"label": "2-hour travel boundary (updated)"}
    }

# ── Config ─────────────────────────────────────────────────────────────────────
LIBERIA_BBOX = (-11.5, 4.3, -7.4, 8.6)
GRID_COLS = 40
GRID_ROWS = 30
RADIUS_MINUTES = 120
HOSPITAL_EXCLUSION_KM = 20

LIBERIA_TOWNS = [
    {"name": "Monrovia",      "lat": 6.30,  "lng": -10.80},
    {"name": "Gbarnga",       "lat": 7.00,  "lng": -9.47},
    {"name": "Kakata",        "lat": 6.53,  "lng": -10.35},
    {"name": "Voinjama",      "lat": 8.42,  "lng": -9.75},
    {"name": "Zwedru",        "lat": 6.07,  "lng": -8.13},
    {"name": "Harper",        "lat": 4.38,  "lng": -7.72},
    {"name": "Buchanan",      "lat": 5.88,  "lng": -10.05},
    {"name": "Tubmanburg",    "lat": 6.87,  "lng": -10.82},
    {"name": "Ganta",         "lat": 7.23,  "lng": -8.98},
    {"name": "Sanniquellie",  "lat": 7.36,  "lng": -8.71},
    {"name": "Tapita",        "lat": 6.49,  "lng": -8.87},
    {"name": "Zorzor",        "lat": 7.78,  "lng": -9.43},
    {"name": "Kolahun",       "lat": 8.29,  "lng": -10.06},
    {"name": "Foya",          "lat": 8.38,  "lng": -10.18},
    {"name": "Greenville",    "lat": 5.01,  "lng": -9.04},
    {"name": "Fish Town",     "lat": 5.19,  "lng": -7.88},
    {"name": "Toe Town",      "lat": 5.88,  "lng": -8.17},
    {"name": "Pleebo",        "lat": 4.60,  "lng": -7.67},
    {"name": "Barclayville",  "lat": 4.67,  "lng": -8.80},
    {"name": "Robertsport",   "lat": 6.75,  "lng": -11.37},
]

class OptimizeRequest(BaseModel):
    n: int = Field(..., ge=1, le=50)

# ── Helpers ────────────────────────────────────────────────────────────────────
def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def _get_nearest_town(lat, lng):
    best_dist, best_name = float('inf'), "Unknown"
    for t in LIBERIA_TOWNS:
        d = _haversine(lat, lng, t["lat"], t["lng"])
        if d < best_dist:
            best_dist, best_name = d, t["name"]
    return best_name

def _generate_candidates(transform, width, height, cost_raw, population, hosp_pts):
    unserved_mask = (cost_raw > 120) & (cost_raw < 9999)
    unserved_pop  = population * unserved_mask

    r_edges = np.linspace(0, height, GRID_ROWS + 1).astype(int)
    c_edges = np.linspace(0, width,  GRID_COLS + 1).astype(int)

    yy, xx = np.mgrid[0:height, 0:width]
    cell_data, cell_sums = [], []

    for i in range(GRID_ROWS):
        for j in range(GRID_COLS):
            r0, r1 = r_edges[i], r_edges[i+1]
            c0, c1 = c_edges[j], c_edges[j+1]
            p_cell = unserved_pop[r0:r1, c0:c1]
            p_sum  = np.sum(p_cell)
            if p_sum > 0:
                r_w = np.sum(p_cell * yy[r0:r1, c0:c1]) / p_sum
                c_w = np.sum(p_cell * xx[r0:r1, c0:c1]) / p_sum
                cell_data.append((r_w, c_w, p_sum))
                cell_sums.append(p_sum)

    if not cell_sums:
        return []

    threshold = np.percentile(cell_sums, 30)
    candidates = []
    for r_f, c_f, p_sum in cell_data:
        if p_sum < threshold:
            continue
        r, c = int(round(r_f)), int(round(c_f))
        if r < 0 or r >= height or c < 0 or c >= width:
            continue
        if cost_raw[r, c] >= 9999 or np.isnan(cost_raw[r, c]):
            continue
        lng, lat = xy(transform, r, c)
        too_close = any(
            _haversine(lat, lng, h_lat, h_lng) < HOSPITAL_EXCLUSION_KM
            for h_lat, h_lng in hosp_pts
        )
        if not too_close:
            candidates.append((r, c, float(lat), float(lng)))

    return candidates

# ── Route ──────────────────────────────────────────────────────────────────────
@router.post("/api/optimize")
def optimize(body: OptimizeRequest):
    if not _TIF_PATH.exists() or not _WP_PATH.exists():
        raise HTTPException(status_code=503, detail="Required data rasters missing.")

    # 1. Load travel time surface
    with rasterio.open(_TIF_PATH) as src:
        transform = src.transform
        cost_raw  = src.read(1).astype(float)
        width, height = src.width, src.height
        nodata    = src.nodata
        res_deg   = abs(transform.a)

    if nodata is not None:
        cost_raw[cost_raw == nodata] = 9999.0
    cost_raw[np.isnan(cost_raw)] = 9999.0

    # 2. Load and reproject population
    with rasterio.open(_WP_PATH) as wp:
        wp_data = wp.read(1).astype(float)
        wp_data[wp_data < 0] = 0
        population = np.empty((height, width), dtype=np.float32)
        reproject(
            source=wp_data, destination=population,
            src_transform=wp.transform, src_crs=wp.crs,
            dst_transform=transform, dst_crs=src.crs,
            resampling=Resampling.sum
        )
    population[np.isnan(population)] = 0

    # 3. Load hospitals for exclusion zone
    hospitals = gpd.read_file(_HOSPITALS_PATH)
    hosp_pts = []
    for geom in hospitals.geometry:
        if geom.geom_type == 'Point':
            hosp_pts.append((float(geom.y), float(geom.x)))
        elif geom.geom_type in ('Polygon', 'MultiPolygon'):
            c = geom.centroid
            hosp_pts.append((float(c.y), float(c.x)))

    # 4. Generate population-weighted candidates
    candidates = _generate_candidates(transform, width, height, cost_raw, population, hosp_pts)

    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    km_per_pixel = res_deg * 111.0

    current_cost = cost_raw.copy()
    placed = []
    coverage_curve = []
    total_pop = np.sum(population)

    # 5. Greedy placement loop
    for i in range(body.n):
        uncovered_pop = population.copy()
        uncovered_pop[current_cost <= RADIUS_MINUTES] = 0

        best_gain, best_site, best_mask = -1, None, None

        for r, c, lat, lon in candidates:
            R_px   = RADIUS_MINUTES / (2.0 * km_per_pixel)
            dist_sq = (rows - r)**2 + (cols - c)**2
            mask   = dist_sq <= R_px**2
            gain   = np.sum(uncovered_pop[mask])
            if gain > best_gain:
                best_gain, best_site, best_mask = gain, (r, c, lat, lon), mask

        if not best_site or best_gain <= 0:
            break

        r, c, lat, lon = best_site
        placed.append({
            "lat":          float(round(lat, 6)),
            "lng":          float(round(lon, 6)),
            "pop_gained":   int(best_gain),
            "nearest_town": str(_get_nearest_town(lat, lon))
        })

        current_cost[best_mask] = 0

        current_covered_pop = np.sum(population[current_cost <= RADIUS_MINUTES])
        coverage_curve.append({
            "n_facilities": len(placed),
            "pct_covered":  round(float(current_covered_pop / total_pop * 100), 1),
            "pop_gained":   int(best_gain)
        })

    # 6. Final stats
    covered_final = current_cost <= RADIUS_MINUTES
    within_pop    = int(np.sum(population[covered_final]))
    beyond_pop    = int(total_pop - within_pop)
    pct           = round(float(within_pop / total_pop * 100), 1) if total_pop else 0.0

    return JSONResponse(content={
        "locations": placed,
        "updated_stats": {
            "total_pop":   int(total_pop),
            "within_2hr":  within_pop,
            "beyond_2hr":  beyond_pop,
            "pct_covered": pct,
            "pct_beyond":  round(100.0 - pct, 1)
        },
        "coverage_curve":    coverage_curve,
        "updated_contour":   compute_contour(current_cost, transform)
    })