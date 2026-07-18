"""
Phase 0: Download Canadian surgical access datasets.
Sources: McGaughey 2023 (figshare), CIHI, StatsCan, Salles & Mullan
"""

import os
import sys
import requests
import zipfile
from pathlib import Path

# Create data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("APOGEE CANADA — PHASE 0 DATA DOWNLOAD")
print("=" * 70)

# McGaughey figshare DOIs
FIGSHARE_DOIS = {
    "DA_population_centroids": "10.6084/m9.figshare.24082131",
    "ED_locations": "10.6084/m9.figshare.24082110",
    "DA_to_ED_travel_times": "10.6084/m9.figshare.24082158",
    "CSD_avg_travel_time": "10.6084/m9.figshare.24082128",
    "CSD_DA_linking": "10.6084/m9.figshare.24100428",
}

print("\n1. McGaughey et al. figshare datasets:")
print("-" * 70)
for name, doi in FIGSHARE_DOIS.items():
    url = f"https://doi.org/{doi}"
    print(f"   {name}")
    print(f"   → {url}")
    print(f"   Status: To download, visit the DOI and download the CSV file manually")
    print()

print("\n2. Statistics Canada boundary files (2021 Census):")
print("-" * 70)
statcan_urls = {
    "DA_boundaries": "https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/fd-df/files-fichiers/lda_000b21a_e.zip",
    "CSD_boundaries": "https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/fd-df/files-fichiers/lcsd000b21a_e.zip",
}
print("   These files are large (~200MB each). Download manually or via wget:")
for name, url in statcan_urls.items():
    print(f"   {name}:")
    print(f"   wget '{url}' -O data/{name}.zip")
print()

print("\n3. CIHI Physician Supply Data:")
print("-" * 70)
print("   Visit: https://www.cihi.ca/en/supply-and-distribution")
print("   Download: 'Supply Distribution and Migration of Physicians in Canada, 2024'")
print("   Save as: data/CIHI_physician_supply_2024.xlsx")
print()

print("\n4. Salles & Mullan Winter Road Data:")
print("-" * 70)
print("   Repository: UK Polar Data Centre")
print("   Citation: Salles & Mullan, 2025")
print("   Status: Check UK Polar Data Centre for shapefile download")
print()

print("=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("""
1. Download the figshare CSVs (section 1) manually from their DOI links
   - Place them in: data/

2. Download StatsCan boundary shapefiles (section 2)
   - Run the wget commands or download via web interface

3. Get CIHI physician supply XLSX (section 3)
   - Visit CIHI website, download 2024 report

4. Locate Salles & Mullan winter road shapefiles (section 4)
   - Check UK Polar Data Centre or contact authors

Once all files are in the data/ folder, run: python join_datasets.py
""")

print("\nFiles expected in data/ after download:")
expected_files = [
    "DA_population_centroids.csv",
    "ED_locations.csv",
    "DA_to_ED_travel_times.csv",
    "CSD_avg_travel_time.csv",
    "CSD_DA_linking.csv",
    "CIHI_physician_supply_2024.xlsx",
    "lda_000b21a_e.zip",  # or extracted shapefiles
    "lcsd000b21a_e.zip",  # or extracted shapefiles
    "winter_roads_shapefile/",  # Salles & Mullan
]
for f in expected_files:
    print(f"   - {f}")
