"""
Phase 0: Join Canadian surgical access datasets.
Creates a single working table: DA-level population + travel time + province.
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
import sys

DATA_DIR = Path("data")
OUTPUT_DIR = Path("backend/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("JOINING CANADIAN DATASETS")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────
# 1. Load DA population centroids
# ─────────────────────────────────────────────────────────────────
print("\n1. Loading DA population centroids...")
try:
    da_pop = pd.read_csv(DATA_DIR / "DA_population_centroids.csv")
    print(f"   ✓ Loaded {len(da_pop)} dissemination areas")
    print(f"   Columns: {list(da_pop.columns)}")
except FileNotFoundError:
    print("   ✗ DA_population_centroids.csv not found")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────
# 2. Load DA-to-ED travel times
# ─────────────────────────────────────────────────────────────────
print("\n2. Loading DA-to-ED travel times...")
try:
    da_travel = pd.read_csv(DATA_DIR / "DA_to_ED_travel_times.csv")
    print(f"   ✓ Loaded travel times for {len(da_travel)} DAs")
    print(f"   Columns: {list(da_travel.columns)}")
except FileNotFoundError:
    print("   ✗ DA_to_ED_travel_times.csv not found")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────
# 3. Load ED locations (24-hr emergency departments)
# ─────────────────────────────────────────────────────────────────
print("\n3. Loading ED locations...")
try:
    eds = pd.read_csv(DATA_DIR / "ED_locations.csv")
    print(f"   ✓ Loaded {len(eds)} emergency departments")
    print(f"   Columns: {list(eds.columns)}")
except FileNotFoundError:
    print("   ✗ ED_locations.csv not found")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────
# 4. Load CSD-DA linking table
# ─────────────────────────────────────────────────────────────────
print("\n4. Loading CSD-DA linking table...")
try:
    csd_da = pd.read_csv(DATA_DIR / "CSD_DA_linking.csv")
    print(f"   ✓ Loaded {len(csd_da)} CSD-DA pairs")
except FileNotFoundError:
    print("   ✗ CSD_DA_linking.csv not found")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────
# 5. Load CSD-level average travel times
# ─────────────────────────────────────────────────────────────────
print("\n5. Loading CSD-level average travel times...")
try:
    csd_travel = pd.read_csv(DATA_DIR / "CSD_avg_travel_time.csv")
    print(f"   ✓ Loaded average travel times for {len(csd_travel)} CSDs")
except FileNotFoundError:
    print("   ✗ CSD_avg_travel_time.csv not found")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────
# 6. Join everything on DAUID
# ─────────────────────────────────────────────────────────────────
print("\n6. Joining datasets...")

# Join DA population + travel times
merged = da_pop.merge(da_travel, on="DAUID", how="inner")
print(f"   After join DA + travel: {len(merged)} rows")

# Add CSD via linking table
merged = merged.merge(csd_da, on="DAUID", how="left")
print(f"   After adding CSD: {len(merged)} rows")

# Rename travel time column for clarity (assume it's "Total_Minutes" or similar)
travel_col = next((c for c in merged.columns if 'inute' in c.lower()), None)
if travel_col:
    merged.rename(columns={travel_col: "travel_time_minutes"}, inplace=True)
    print(f"   ✓ Identified travel time column: {travel_col}")

# ─────────────────────────────────────────────────────────────────
# 7. Save the working dataset
# ─────────────────────────────────────────────────────────────────
output_file = OUTPUT_DIR / "da_working_dataset.csv"
merged.to_csv(output_file, index=False)
print(f"\n✓ Saved working dataset: {output_file}")
print(f"  Shape: {merged.shape}")
print(f"  Columns: {list(merged.columns)}")

# ─────────────────────────────────────────────────────────────────
# 8. Summary stats
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY STATS")
print("=" * 70)

if "PRUID" in merged.columns:
    print(f"\nDAs by province:")
    print(merged["PRUID"].value_counts().head(10))

if "travel_time_minutes" in merged.columns:
    print(f"\nTravel time statistics (minutes):")
    print(f"  Mean: {merged['travel_time_minutes'].mean():.1f}")
    print(f"  Median: {merged['travel_time_minutes'].median():.1f}")
    print(f"  Max: {merged['travel_time_minutes'].max():.1f}")
    print(f"  >120 min (beyond 2-hr threshold): {(merged['travel_time_minutes'] > 120).sum()}")

if "Population" in merged.columns or "x" in merged.columns:
    pop_col = next((c for c in merged.columns if "pop" in c.lower()), None)
    if pop_col:
        print(f"\nPopulation statistics:")
        print(f"  Total: {merged[pop_col].sum():,.0f}")
        print(f"  Mean per DA: {merged[pop_col].mean():.0f}")

print("\n" + "=" * 70)
print("NEXT STEP: Update backend/data.py to load this CSV")
print("=" * 70)
