"""
generate_tiles.py
Run this from your apogee/ root folder:
    python generate_tiles.py

Generates PNG map tiles from surgical_travel_time.tif
Output goes to: frontend/public/tiles/
"""

import os
import math
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.crs import CRS
import struct
import zlib

# ── CONFIG ────────────────────────────────────────────────────────────────
INPUT_TIF  = "backend/data/surgical_travel_time.tif"
OUTPUT_DIR = "frontend/public/tiles"
MIN_ZOOM   = 5
MAX_ZOOM   = 11
TILE_SIZE  = 256

# ── COLOR MAP ─────────────────────────────────────────────────────────────
# Travel time (minutes) → RGBA color
# Green=fast access, Yellow=moderate, Orange=slow, Red=beyond 2hr
def travel_time_to_color(minutes):
    if np.isnan(minutes) or minutes < 0:
        return (0, 0, 0, 0)  # transparent
    elif minutes <= 30:
        # Green
        t = minutes / 30
        r = int(50 + t * 50)
        g = int(180 - t * 30)
        b = int(50)
        return (r, g, b, 200)
    elif minutes <= 60:
        # Yellow-green
        t = (minutes - 30) / 30
        r = int(100 + t * 155)
        g = int(200 - t * 50)
        b = int(50)
        return (r, g, b, 200)
    elif minutes <= 120:
        # Orange
        t = (minutes - 60) / 60
        r = int(255)
        g = int(150 - t * 100)
        b = int(50 - t * 40)
        return (r, g, b, 200)
    else:
        # Red - beyond 2hr threshold
        t = min((minutes - 120) / 200, 1.0)
        r = int(200)
        g = int(30 - t * 20)
        b = int(30 - t * 20)
        return (r, g, b, 210)


def colorize_array(data):
    """Convert float travel time array to RGBA uint8 array."""
    h, w = data.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    
    # Vectorized coloring by band
    valid = ~np.isnan(data) & (data >= 0)
    
    # Transparent for nodata
    rgba[:, :, 3] = 0
    
    # Green: 0-30
    mask = valid & (data <= 30)
    t = np.clip(data[mask] / 30, 0, 1)
    rgba[mask, 0] = (50 + t * 50).astype(np.uint8)
    rgba[mask, 1] = (180 - t * 30).astype(np.uint8)
    rgba[mask, 2] = 50
    rgba[mask, 3] = 200

    # Yellow: 30-60
    mask = valid & (data > 30) & (data <= 60)
    t = np.clip((data[mask] - 30) / 30, 0, 1)
    rgba[mask, 0] = (100 + t * 155).astype(np.uint8)
    rgba[mask, 1] = (200 - t * 50).astype(np.uint8)
    rgba[mask, 2] = 50
    rgba[mask, 3] = 200

    # Orange: 60-120
    mask = valid & (data > 60) & (data <= 120)
    t = np.clip((data[mask] - 60) / 60, 0, 1)
    rgba[mask, 0] = 255
    rgba[mask, 1] = (150 - t * 100).astype(np.uint8)
    rgba[mask, 2] = (50 - t * 40).astype(np.uint8)
    rgba[mask, 3] = 200

    # Red: >120
    mask = valid & (data > 120)
    t = np.clip((data[mask] - 120) / 200, 0, 1)
    rgba[mask, 0] = 200
    rgba[mask, 1] = (30 - t * 20).astype(np.uint8)
    rgba[mask, 2] = (30 - t * 20).astype(np.uint8)
    rgba[mask, 3] = 210

    return rgba


def write_png(rgba_tile, path):
    """Write RGBA numpy array as PNG without PIL dependency."""
    h, w = rgba_tile.shape[:2]
    
    def make_chunk(chunk_type, data):
        length = struct.pack('>I', len(data))
        chunk = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
        return length + chunk + crc
    
    # PNG signature
    sig = b'\x89PNG\r\n\x1a\n'
    
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # IDAT - compress scanlines
    raw = b''
    for row in rgba_tile:
        raw += b'\x00' + row.astype(np.uint8).tobytes()
    compressed = zlib.compress(raw, 6)
    idat = make_chunk(b'IDAT', compressed)
    
    # IEND
    iend = make_chunk(b'IEND', b'')
    
    with open(path, 'wb') as f:
        f.write(sig + ihdr + idat + iend)


def lon_lat_to_tile(lon, lat, zoom):
    """Convert lon/lat to tile x/y at given zoom."""
    n = 2 ** zoom
    x = int((lon + 180) / 360 * n)
    lat_rad = math.radians(lat)
    y = int((1 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2 * n)
    return x, y


def tile_bounds(x, y, zoom):
    """Return (west, south, east, north) bounds of a tile."""
    n = 2 ** zoom
    west  = x / n * 360 - 180
    east  = (x + 1) / n * 360 - 180
    north = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    south = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n))))
    return west, south, east, north


def generate_tiles():
    print(f"Loading {INPUT_TIF}...")
    
    with rasterio.open(INPUT_TIF) as src:
        data = src.read(1).astype(float)
        nodata = src.nodata
        bounds = src.bounds
        src_transform = src.transform
        src_crs = src.crs
    
    if nodata is not None:
        data[data == nodata] = np.nan
    data[data < 0] = np.nan
    
    print(f"Raster shape: {data.shape}")
    print(f"Bounds: {bounds}")
    print(f"Valid pixels: {np.sum(~np.isnan(data)):,}")
    
    # Web Mercator CRS for tiles
    web_mercator = CRS.from_epsg(3857)
    
    total_tiles = 0
    
    for zoom in range(MIN_ZOOM, MAX_ZOOM + 1):
        # Find tile range that covers our data
        x_min, y_max = lon_lat_to_tile(bounds.left, bounds.bottom, zoom)
        x_max, y_min = lon_lat_to_tile(bounds.right, bounds.top, zoom)
        
        # Add small buffer
        x_min = max(0, x_min - 1)
        y_min = max(0, y_min - 1)
        x_max = x_max + 1
        y_max = y_max + 1
        
        n_tiles = (x_max - x_min + 1) * (y_max - y_min + 1)
        print(f"Zoom {zoom}: {n_tiles} tiles ({x_max-x_min+1} x {y_max-y_min+1})")
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                west, south, east, north = tile_bounds(x, y, zoom)
                
                # Create output transform for this tile
                from rasterio.transform import from_bounds
                tile_transform = from_bounds(west, south, east, north, TILE_SIZE, TILE_SIZE)
                
                # Reproject data to tile
                tile_data = np.full((TILE_SIZE, TILE_SIZE), np.nan, dtype=np.float32)
                
                try:
                    reproject(
                        source=data.astype(np.float32),
                        destination=tile_data,
                        src_transform=src_transform,
                        src_crs=src_crs,
                        dst_transform=tile_transform,
                        dst_crs=CRS.from_epsg(4326),
                        resampling=Resampling.bilinear,
                        src_nodata=np.nan,
                        dst_nodata=np.nan
                    )
                except Exception:
                    continue
                
                # Skip tiles that are entirely nodata
                if np.all(np.isnan(tile_data)):
                    continue
                
                # Colorize
                rgba = colorize_array(tile_data.astype(float))
                
                # Save
                tile_dir = os.path.join(OUTPUT_DIR, str(zoom), str(x))
                os.makedirs(tile_dir, exist_ok=True)
                tile_path = os.path.join(tile_dir, f"{y}.png")
                write_png(rgba, tile_path)
                total_tiles += 1
        
        print(f"  Zoom {zoom} done. Total tiles so far: {total_tiles}")
    
    print(f"\nDone! Generated {total_tiles} tiles in {OUTPUT_DIR}/")
    print("Tell Betul: tiles are ready. She can point MapLibre at /tiles/{z}/{x}/{y}.png")


if __name__ == "__main__":
    generate_tiles()
