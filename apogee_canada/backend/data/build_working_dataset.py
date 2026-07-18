"""
build_working_dataset.py

Joins the real figshare files into the working CSVs used by the Canada backend.
Run from: apogee_canada/backend/data/

Files produced:
  - da_working_dataset.csv   (DA population + travel time + province — used by optimizer)
  - DA_population_centroids.csv   (real DA centroids)
  - DA_to_ED_travel_times.csv     (real DA travel times)
  - ED_locations.csv              (real 24-hr ED locations, with Province column added)
  - CSD_avg_travel_time.csv       (CSD-level avg travel time, renamed columns)
  - CSD_DA_linking.csv            (CSD-DA lookup)

License: Source data CC BY-NC-ND (figshare). Used as computation input only —
         raw files are NOT exposed as downloadable API responses.
"""

import pandas as pd
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent

# ─── Province mapping ──────────────────────────────────────────────────────────
# PRUID (Statistics Canada numeric) → abbreviation and name
PRUID_TO_ABBR = {
    10: "NL", 11: "PE", 12: "NS", 13: "NB",
    24: "QC", 35: "ON", 46: "MB", 47: "SK",
    48: "AB", 59: "BC", 60: "YT", 61: "NT", 62: "NU",
}
PRUID_TO_NAME = {
    10: "Newfoundland and Labrador", 11: "Prince Edward Island",
    12: "Nova Scotia", 13: "New Brunswick", 24: "Quebec",
    35: "Ontario", 46: "Manitoba", 47: "Saskatchewan",
    48: "Alberta", 59: "British Columbia",
    60: "Yukon", 61: "Northwest Territories", 62: "Nunavut",
}

# ─── 1. Load DA population-weighted centroids ──────────────────────────────────
print("Loading DA centroids...")
cent = pd.read_csv(HERE / "Popwgt_DA_Cent.csv", index_col=0)
# Columns: DAUID, PRUID (numeric), y (lat), x (lon), Population
cent["PRUID_num"] = cent["PRUID"].astype(int)
cent["PRUID"] = cent["PRUID_num"].map(PRUID_TO_ABBR).fillna(cent["PRUID_num"].astype(str))
cent["Province"] = cent["PRUID_num"].map(PRUID_TO_NAME).fillna("Unknown")
cent = cent[["DAUID", "PRUID", "Province", "x", "y", "Population"]]
print(f"  DA centroids: {len(cent):,} rows")

# ─── 2. Load DA-to-nearest-24hr-ED travel times ────────────────────────────────
print("Loading DA travel times...")
tt = pd.read_csv(HERE / "DA_Centroid_to_24hrED.csv", encoding="utf-8-sig")
# Columns: OBJECTID, Total_Kilometers, Total_Minutes, From_DAUID, From_PRUID, ...
tt = tt.rename(columns={
    "From_DAUID":       "DAUID",
    "From_PRUID":       "PRUID_num",
    "Total_Kilometers": "Total_Kilometres",
})
tt["PRUID"] = tt["PRUID_num"].astype(int).map(PRUID_TO_ABBR).fillna(tt["PRUID_num"].astype(str))
tt = tt[["DAUID", "PRUID", "Total_Minutes", "Total_Kilometres"]]
print(f"  Travel times: {len(tt):,} rows")

# ─── 3. Build da_working_dataset.csv ──────────────────────────────────────────
print("Joining DA centroids + travel times...")
working = cent.merge(
    tt[["DAUID", "Total_Minutes", "Total_Kilometres"]],
    on="DAUID",
    how="left"
)
# Fill any unmatched DAs (no path to an ED) with a very large value
working["Total_Minutes"] = working["Total_Minutes"].fillna(9999.0)
working["Total_Kilometres"] = working["Total_Kilometres"].fillna(9999.0)

# Drop rows with zero population (uninhabited DAs don't affect coverage analysis)
working = working[working["Population"] > 0].reset_index(drop=True)
print(f"  Working dataset: {len(working):,} DAs (population > 0)")

# Write
working.to_csv(HERE / "da_working_dataset.csv", index=False)
print("  → Wrote da_working_dataset.csv")

# ─── 4. Write cleaned DA_population_centroids.csv ─────────────────────────────
cent.to_csv(HERE / "DA_population_centroids.csv", index=False)
print("  → Wrote DA_population_centroids.csv")

# ─── 5. Write cleaned DA_to_ED_travel_times.csv ───────────────────────────────
tt.to_csv(HERE / "DA_to_ED_travel_times.csv", index=False)
print("  → Wrote DA_to_ED_travel_times.csv")

# ─── 6. Load and clean 24-hr ED locations ─────────────────────────────────────
print("Loading ED locations...")
eds = pd.read_csv(HERE / "24hrED_Locations.csv", encoding="utf-8-sig")
# Columns: ObjectID, X (lon), Y (lat), 24-hr_ED (name), ADDRESS, CITY, POSTAL_CODE
eds = eds.rename(columns={
    "ObjectID":  "ED_ID",
    "X":         "x",
    "Y":         "y",
    "24-hr_ED":  "ED_Name",
    "ADDRESS":   "Address",
    "CITY":      "City",
    "POSTAL_CODE": "Postal_Code",
})
# Determine Province from postal code prefix (first letter maps to province)
POSTAL_PREFIX_TO_PROVINCE = {
    "A": ("NL", "Newfoundland and Labrador"),
    "B": ("NS", "Nova Scotia"),
    "C": ("PE", "Prince Edward Island"),
    "E": ("NB", "New Brunswick"),
    "G": ("QC", "Quebec"), "H": ("QC", "Quebec"), "J": ("QC", "Quebec"),
    "K": ("ON", "Ontario"), "L": ("ON", "Ontario"),
    "M": ("ON", "Ontario"), "N": ("ON", "Ontario"),
    "P": ("ON", "Ontario"),
    "R": ("MB", "Manitoba"),
    "S": ("SK", "Saskatchewan"),
    "T": ("AB", "Alberta"),
    "V": ("BC", "British Columbia"),
    "X": ("NT", "Northwest Territories"),  # NT and NU share X prefix; approximate
    "Y": ("YT", "Yukon"),
}

def postal_to_province(pcode):
    if not isinstance(pcode, str) or len(pcode) == 0:
        return ("", "")
    return POSTAL_PREFIX_TO_PROVINCE.get(pcode[0].upper(), ("", "Unknown"))

eds[["PRUID", "Province"]] = eds["Postal_Code"].apply(
    lambda p: pd.Series(postal_to_province(p))
)

# Also add lat/lng aliases (some frontend code may expect lat/lng instead of y/x)
eds["lat"] = eds["y"]
eds["lng"] = eds["x"]

eds = eds[["ED_ID", "Province", "PRUID", "ED_Name", "x", "y", "lat", "lng",
           "Address", "City", "Postal_Code"]]
print(f"  ED locations: {len(eds):,} rows")
eds.to_csv(HERE / "ED_locations.csv", index=False)
print("  → Wrote ED_locations.csv")

# ─── 7. CSD avg travel time ───────────────────────────────────────────────────
print("Loading CSD avg travel time...")
csd_tt = pd.read_csv(HERE / "Population_Weighted_Average_Time.csv")
# Columns: CSDUID, Total_Sec, Total_Min
csd_tt = csd_tt.rename(columns={
    "CSDUID":    "CSDUID",
    "Total_Min": "Average_Travel_Minutes",
})
csd_tt = csd_tt[["CSDUID", "Average_Travel_Minutes"]]
csd_tt["Average_Travel_Minutes"] = csd_tt["Average_Travel_Minutes"].round(1)
print(f"  CSD avg travel time: {len(csd_tt):,} CSDs")
csd_tt.to_csv(HERE / "CSD_avg_travel_time.csv", index=False)
print("  → Wrote CSD_avg_travel_time.csv")

# ─── 8. CSD-DA linking table ──────────────────────────────────────────────────
print("Loading CSD-DA linking table...")
linking = pd.read_csv(HERE / "CSD_DA_Union.csv")
# Columns: CSDUID, DAUID
linking = linking[["CSDUID", "DAUID"]]
print(f"  CSD-DA linking: {len(linking):,} rows")
linking.to_csv(HERE / "CSD_DA_linking.csv", index=False)
print("  → Wrote CSD_DA_linking.csv")

# ─── Summary ──────────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===")
print(f"da_working_dataset.csv : {len(working):,} rows | "
      f"Provinces: {sorted(working['PRUID'].unique())}")
print(f"ED_locations.csv       : {len(eds):,} EDs | "
      f"Provinces: {sorted(eds['Province'].unique())[:6]}...")
print(f"CSD_avg_travel_time.csv: {len(csd_tt):,} CSDs")
print(f"CSD_DA_linking.csv     : {len(linking):,} rows")
print(f"\nMedian travel time: {working['Total_Minutes'].median():.1f} min")
print(f"% DAs within 120 min: {(working['Total_Minutes'] <= 120).mean()*100:.1f}%")
print("\nDone.")
