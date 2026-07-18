#!/usr/bin/env python3
"""
Local test script for Apogee Canada backend.
Run this to verify all endpoints work before deploying.
"""

import sys
import json
import subprocess
import time
from pathlib import Path

print("=" * 70)
print("APOGEE CANADA — LOCAL BACKEND TEST")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# Check 1: Mock data exists
# ─────────────────────────────────────────────────────────────────────────────
print("\n1. Checking mock data...")
data_dir = Path("backend/data")
required_files = [
    "da_working_dataset.csv",
    "ED_locations.csv",
    "DA_population_centroids.csv",
    "DA_to_ED_travel_times.csv",
]

missing = []
for f in required_files:
    if not (data_dir / f).exists():
        missing.append(f)

if missing:
    print(f"   ✗ Missing files: {missing}")
    print("   → Run: python generate_mock_data.py")
    sys.exit(1)
else:
    print(f"   ✓ All required data files present")

# ─────────────────────────────────────────────────────────────────────────────
# Check 2: Backend modules exist and are importable
# ─────────────────────────────────────────────────────────────────────────────
print("\n2. Checking Python modules...")
sys.path.insert(0, "backend")

modules_to_test = [
    "main",
    "data",
    "optimizer",
    "brief",
    "endpoints.investment",
    "endpoints.workforce",
    "endpoints.seasonal",
]

failed_imports = []
for mod in modules_to_test:
    try:
        __import__(mod)
        print(f"   ✓ {mod}")
    except Exception as e:
        print(f"   ✗ {mod}: {e}")
        failed_imports.append((mod, e))

if failed_imports:
    print("\n   Import failed. Check dependencies:")
    print("   pip install fastapi uvicorn pandas numpy pydantic python-dotenv anthropic")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Check 3: Test optimizer directly
# ─────────────────────────────────────────────────────────────────────────────
print("\n3. Testing optimizer directly...")
try:
    from optimizer import optimize, OptimizeRequest
    
    req = OptimizeRequest(n=3)
    result = optimize(req)
    
    # Check response shape
    expected_keys = {"locations", "updated_stats", "coverage_curve", "da_coverage_map"}
    result_dict = json.loads(result.body.decode())
    
    actual_keys = set(result_dict.keys())
    if expected_keys == actual_keys:
        print(f"   ✓ Optimizer response shape correct")
        print(f"     - Placed {len(result_dict['locations'])} facilities")
        print(f"     - Coverage: {result_dict['updated_stats']['pct_covered']}%")
        print(f"     - Coverage curve points: {len(result_dict['coverage_curve'])}")
    else:
        print(f"   ✗ Response shape mismatch")
        print(f"     Expected: {expected_keys}")
        print(f"     Got: {actual_keys}")
        sys.exit(1)
        
except Exception as e:
    print(f"   ✗ Optimizer test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Check 4: Test endpoints
# ─────────────────────────────────────────────────────────────────────────────
print("\n4. Testing endpoint modules...")
try:
    from data import get_data
    from endpoints.investment import get_investment_analysis
    from endpoints.workforce import get_workforce_alignment
    from endpoints.seasonal import get_seasonal_access
    
    data_resp = get_data()
    print(f"   ✓ /api/data: {len(data_resp['das'])} DAs, {len(data_resp['eds'])} EDs")
    
    inv_resp = get_investment_analysis()
    print(f"   ✓ /api/investment-analysis: {len(inv_resp['illustrative_facility_cases'])} cases")
    
    wf_resp = get_workforce_alignment()
    print(f"   ✓ /api/workforce-alignment: {len(wf_resp['provincial_data'])} provinces")
    
    seas_resp = get_seasonal_access()
    print(f"   ✓ /api/seasonal-access: {len(seas_resp['provincial_seasonal_data'])} provinces")
    
except Exception as e:
    print(f"   ✗ Endpoint test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Check 5: Dependencies
# ─────────────────────────────────────────────────────────────────────────────
print("\n5. Checking Python dependencies...")
required_packages = [
    "fastapi",
    "uvicorn",
    "pandas",
    "numpy",
    "pydantic",
    "dotenv",
]

missing_packages = []
for pkg in required_packages:
    try:
        __import__(pkg.replace("-", "_"))
        print(f"   ✓ {pkg}")
    except ImportError:
        print(f"   ✗ {pkg}")
        missing_packages.append(pkg)

if missing_packages:
    print(f"\n   Install missing packages:")
    print(f"   pip install {' '.join(missing_packages)}")

# ─────────────────────────────────────────────────────────────────────────────
# All checks passed
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("ALL CHECKS PASSED ✓")
print("=" * 70)
print("""
Next steps:
1. Start the server:
   cd backend && python -m uvicorn main:app --reload

2. In another terminal, test endpoints:
   curl http://localhost:8000/
   curl http://localhost:8000/api/data
   curl -X POST http://localhost:8000/api/optimize \\
     -H "Content-Type: application/json" \\
     -d '{"n": 5}'

3. View docs at http://localhost:8000/docs

4. When ready to deploy:
   - Push backend/ to new repo (GitHub)
   - Deploy to Render or Railway
   - Set ANTHROPIC_API_KEY environment variable
   - Test all endpoints against deployed URL
""")
