import rasterio
import numpy as np
import json
import os
from rasterio.transform import rowcol, xy

LAT_MIN, LAT_MAX = 4.2, 8.6
LNG_MIN, LNG_MAX = -11.6, -7.4

raster_path = os.path.join(os.path.dirname(__file__), "data", "surgical_travel_time.tif")

with rasterio.open(raster_path) as src:
    data = src.read(1)
    transform = src.transform
    nodata = src.nodata

# Generate grid candidates
candidates = []
lat_step = (LAT_MAX - LAT_MIN) / 10
lng_step = (LNG_MAX - LNG_MIN) / 10

for i in range(10):
    for j in range(10):
        cell_lat_min = LAT_MIN + i * lat_step
        cell_lat_max = cell_lat_min + lat_step
        cell_lng_min = LNG_MIN + j * lng_step
        cell_lng_max = cell_lng_min + lng_step

        rows, cols = np.where(
            (data > 120) & (data != nodata) & (data < 2000)
        )

        cell_candidates = []
        for r, c in zip(rows, cols):
            from rasterio.transform import xy
            lng, lat = xy(transform, r, c)
            if (cell_lat_min <= lat < cell_lat_max and
                cell_lng_min <= lng < cell_lng_max):
                cell_candidates.append((float(lat), float(lng), int(r), int(c)))

        if cell_candidates:
            step = max(1, len(cell_candidates) // 3)
            for k in range(3):
                idx = k * step
                if idx < len(cell_candidates):
                    lat, lng, r, c = cell_candidates[idx]
                    candidates.append({
                        "lat": round(lat, 4),
                        "lng": round(lng, 4),
                        "row": r,
                        "col": c
                    })

print(f"Generated {len(candidates)} candidates")

# Score each candidate
radius = 8
h, w = data.shape
scored = []

for idx, cand in enumerate(candidates):
    row, col = cand["row"], cand["col"]
    count = 0
    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            r, c = row + dr, col + dc
            if 0 <= r < h and 0 <= c < w:
                val = data[r, c]
                if val != nodata and val > 120:
                    dist = (dr**2 + dc**2) ** 0.5
                    if dist <= radius:
                        count += 1
    pop_gained = max(int(count * 40), 5000)
    scored.append({
        "lat": cand["lat"],
        "lng": cand["lng"],
        "pop_gained": pop_gained
    })
    if idx % 10 == 0:
        print(f"Scored {idx}/{len(candidates)}...")

scored.sort(key=lambda x: x["pop_gained"], reverse=True)

with open("data/precomputed_optimizer.json", "w") as f:
    json.dump(scored, f)

print(f"Done! Top 5 sites:")
for s in scored[:5]:
    print(f"  {s['lat']}, {s['lng']} → {s['pop_gained']:,} people")