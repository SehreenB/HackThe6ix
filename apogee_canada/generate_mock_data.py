"""
Generate mock Canadian DA-level dataset for Phase 0 testing.
This lets optimizer.py be written and tested before real McGaughey data arrives.
"""

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path("backend/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GENERATING MOCK CANADIAN DATA")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────
# Province bounds and ED locations (realistic approximations)
# ─────────────────────────────────────────────────────────────────
PROVINCES = {
    "ON": {"name": "Ontario", "bounds": (-95.2, 41.7, -74.3, 56.8), "n_da": 1200, "n_ed": 45},
    "BC": {"name": "British Columbia", "bounds": (-139.1, 48.4, -114.1, 60.1), "n_da": 800, "n_ed": 30},
    "AB": {"name": "Alberta", "bounds": (-120.0, 49.0, -110.0, 60.0), "n_da": 600, "n_ed": 25},
    "MB": {"name": "Manitoba", "bounds": (-102.1, 49.7, -89.1, 60.4), "n_da": 400, "n_ed": 15},
    "SK": {"name": "Saskatchewan", "bounds": (-110.5, 49.0, -102.2, 60.4), "n_da": 350, "n_ed": 12},
    "QC": {"name": "Quebec", "bounds": (-79.8, 45.0, -57.5, 55.8), "n_da": 1400, "n_ed": 50},
}

# ─────────────────────────────────────────────────────────────────
# 1. Generate Dissemination Areas
# ─────────────────────────────────────────────────────────────────
print("\n1. Generating Dissemination Areas (DAs)...")

da_records = []
da_id = 10000000

for pr_code, pr_info in PROVINCES.items():
    min_lng, min_lat, max_lng, max_lat = pr_info["bounds"]
    n_da = pr_info["n_da"]
    
    for _ in range(n_da):
        lng = np.random.uniform(min_lng, max_lng)
        lat = np.random.uniform(min_lat, max_lat)
        
        # Population follows log-normal distribution (realistic skew)
        pop = int(np.random.lognormal(mean=6.5, sigma=1.2))
        pop = max(100, min(5000, pop))  # Clamp to realistic DA range
        
        da_records.append({
            "DAUID": da_id,
            "PRUID": pr_code,
            "Province": pr_info["name"],
            "x": lng,
            "y": lat,
            "Population": pop,
        })
        da_id += 1

da_pop = pd.DataFrame(da_records)
print(f"   ✓ Generated {len(da_pop)} DAs")
print(f"   Total population: {da_pop['Population'].sum():,.0f}")

# ─────────────────────────────────────────────────────────────────
# 2. Generate Emergency Department Locations
# ─────────────────────────────────────────────────────────────────
print("\n2. Generating Emergency Departments (EDs)...")

ed_records = []
ed_id = 1

for pr_code, pr_info in PROVINCES.items():
    min_lng, min_lat, max_lng, max_lat = pr_info["bounds"]
    n_ed = pr_info["n_ed"]
    
    for _ in range(n_ed):
        lng = np.random.uniform(min_lng, max_lng)
        lat = np.random.uniform(min_lat, max_lat)
        
        ed_records.append({
            "ED_ID": ed_id,
            "Province": pr_info["name"],
            "PRUID": pr_code,
            "ED_Name": f"{pr_info['name']} Hospital #{ed_id}",
            "x": lng,
            "y": lat,
            "lat": lat,
            "lng": lng,
        })
        ed_id += 1

eds = pd.DataFrame(ed_records)
print(f"   ✓ Generated {len(eds)} EDs")

# ─────────────────────────────────────────────────────────────────
# 3. Compute DA-to-nearest-ED travel times (mock Haversine + road factor)
# ─────────────────────────────────────────────────────────────────
print("\n3. Computing DA-to-ED travel times...")

def haversine_km(lat1, lon1, lat2, lon2):
    """Compute great-circle distance in km."""
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

travel_records = []
for _, da_row in da_pop.iterrows():
    da_lng, da_lat = da_row["x"], da_row["y"]
    
    # Find nearest ED in same province
    same_prov_eds = eds[eds["PRUID"] == da_row["PRUID"]]
    if len(same_prov_eds) == 0:
        continue
    
    min_time = float('inf')
    for _, ed_row in same_prov_eds.iterrows():
        straight_km = haversine_km(da_lat, da_lng, ed_row["y"], ed_row["x"])
        # Road factor: ~1.5x for urban, ~2.0x for rural (use 1.7 average)
        road_km = straight_km * 1.7
        # Average speed: 80 km/h
        minutes = (road_km / 80) * 60
        min_time = min(min_time, minutes)
    
    if min_time < float('inf'):
        travel_records.append({
            "DAUID": da_row["DAUID"],
            "PRUID": da_row["PRUID"],
            "Total_Minutes": int(min_time),
            "Total_Kilometres": round(min_time * 80 / 60, 1),
        })

da_travel = pd.DataFrame(travel_records)
print(f"   ✓ Computed travel times for {len(da_travel)} DA-ED pairs")
print(f"   Travel time range: {da_travel['Total_Minutes'].min()}-{da_travel['Total_Minutes'].max()} min")
print(f"   Beyond 2-hr threshold (120 min): {(da_travel['Total_Minutes'] > 120).sum()}")

# ─────────────────────────────────────────────────────────────────
# 4. Generate CSD-DA linking (mock: assign DAs to random CSDs)
# ─────────────────────────────────────────────────────────────────
print("\n4. Generating CSD-DA linking table...")

csd_da_records = []
csd_id = 1000000

for _, da_row in da_pop.iterrows():
    # Simple mock: assign each DA to a fake CSD in its province
    csd_uid = csd_id + (hash(da_row["DAUID"]) % 100)  # ~100 CSDs per province
    
    csd_da_records.append({
        "CSDUID": csd_uid,
        "DAUID": da_row["DAUID"],
    })

csd_da = pd.DataFrame(csd_da_records)
print(f"   ✓ Generated {len(csd_da)} CSD-DA assignments")
print(f"   Unique CSDs: {csd_da['CSDUID'].nunique()}")

# ─────────────────────────────────────────────────────────────────
# 5. Generate CSD-level average travel times
# ─────────────────────────────────────────────────────────────────
print("\n5. Computing CSD-level average travel times...")

csd_travel_records = []
for csd_uid in csd_da["CSDUID"].unique():
    das_in_csd = csd_da[csd_da["CSDUID"] == csd_uid]["DAUID"].values
    
    # Average travel time for all DAs in this CSD
    avg_time = da_travel[da_travel["DAUID"].isin(das_in_csd)]["Total_Minutes"].mean()
    
    if not np.isnan(avg_time):
        csd_travel_records.append({
            "CSDUID": csd_uid,
            "Average_Travel_Minutes": int(avg_time),
        })

csd_travel = pd.DataFrame(csd_travel_records)
print(f"   ✓ Generated average travel times for {len(csd_travel)} CSDs")

# ─────────────────────────────────────────────────────────────────
# 6. Save all files
# ─────────────────────────────────────────────────────────────────
print("\n6. Saving CSV files...")

files_saved = {
    "DA_population_centroids.csv": da_pop,
    "DA_to_ED_travel_times.csv": da_travel,
    "ED_locations.csv": eds,
    "CSD_DA_linking.csv": csd_da,
    "CSD_avg_travel_time.csv": csd_travel,
}

for fname, df in files_saved.items():
    fpath = DATA_DIR / fname
    df.to_csv(fpath, index=False)
    print(f"   ✓ {fname} ({len(df)} rows)")

# ─────────────────────────────────────────────────────────────────
# 7. Join into working dataset
# ─────────────────────────────────────────────────────────────────
print("\n7. Creating working dataset...")

working = da_pop.merge(da_travel, on="DAUID", how="inner")
print(f"   ✓ Merged DA + travel time: {len(working)} rows")

# Save
working_file = DATA_DIR / "da_working_dataset.csv"
working.to_csv(working_file, index=False)
print(f"   ✓ Saved: {working_file}")

print("\n" + "=" * 70)
print("MOCK DATA READY")
print("=" * 70)
print(f"""
Files created in {DATA_DIR}:
  - DA_population_centroids.csv ({len(da_pop)} DAs)
  - DA_to_ED_travel_times.csv ({len(da_travel)} rows)
  - ED_locations.csv ({len(eds)} EDs)
  - CSD_DA_linking.csv ({len(csd_da)} assignments)
  - CSD_avg_travel_time.csv ({len(csd_travel)} CSDs)
  - da_working_dataset.csv (joined working table)

Total population: {da_pop['Population'].sum():,.0f}
Beyond 2-hr threshold: {(da_travel['Total_Minutes'] > 120).sum()} DAs

Next: Update backend/optimizer.py to load these CSVs.
""")
