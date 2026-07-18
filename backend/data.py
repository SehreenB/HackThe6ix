import json
import os

def load_facilities():
    filepath = os.path.join(os.path.dirname(__file__), "data", "hospitals.geojson")
    with open(filepath, "r") as f:
        d = json.load(f)
    
    facs = []
    for feat in d.get("features", []):
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})
        
        name = props.get("name", "Unknown Facility")
        if not name or not name.strip():
            name = "Unknown Facility"
            
        cap = props.get("capability_level", "basic")
        county = props.get("county", "Liberia")
        
        gtype = geom.get("type")
        coords = geom.get("coordinates", [])
        if not coords: continue
        
        if gtype == "Point":
            lng, lat = coords
        elif gtype == "Polygon":
            pts = coords[0]
            lng = sum(p[0] for p in pts) / len(pts)
            lat = sum(p[1] for p in pts) / len(pts)
        else:
            continue
            
        facs.append({
            "lat": lat,
            "lng": lng,
            "name": name,
            "county": county,
            "capability_level": cap
        })
    return facs

def load_contour():
    filepath = os.path.join(os.path.dirname(__file__), "data", "contour_2hr.geojson")
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        # Fallback if file not found
        return {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-13.0, 5.5], [-12.5, 5.2], [-11.8, 5.0], [-11.0, 5.3],
                    [-10.5, 5.0], [-10.0, 5.5], [-9.5,  6.0], [-9.0,  6.5],
                    [-9.2,  7.2], [-9.8,  7.5], [-10.5, 7.8], [-11.2, 8.0],
                    [-11.8, 7.5], [-12.3, 6.8], [-12.8, 6.2], [-13.0, 5.5]
                ]
            },
            "properties": {"label": "2-hour travel boundary"}
        }

FACILITIES = load_facilities()
CONTOUR = load_contour()

STATS = {
    "total_pop": 5057677,
    "within_2hr": 2909871,
    "beyond_2hr": 2147806,
    "pct_covered": 57.5,
    "pct_beyond": 42.5
}

def get_data():
    return {
        "stats": STATS,
        "facilities": FACILITIES,
        "contour": CONTOUR,
    }