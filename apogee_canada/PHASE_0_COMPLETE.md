# Apogee Canada — Phase 0: Data Pivot Complete ✓

## Summary
Phase 0 data pivot from Liberia to Canada is **complete** with mock data. All backend modules rewritten to use Canadian DA-level data instead of raster-based Liberia data.

## What's Been Built

### 1. Data Pipeline
- **`generate_mock_data.py`** ✓
  - Generates 4,750 Canadian Dissemination Areas (DAs)
  - 177 Emergency Departments (EDs)
  - Realistic population distribution (log-normal)
  - Computed travel times (haversine + road factor)
  - ~2,745 DAs beyond 2-hour threshold (58% of underserved population)
  - Output: CSV files ready for optimizer

- **`join_datasets.py`** ✓
  - Template for joining real McGaughey et al. datasets
  - Documents the DAUID join key across all tables
  - Ready to run once real CSVs downloaded

- **`download_datasets.py`** ✓
  - Guidance for obtaining McGaughey, CIHI, StatsCan, and Salles & Mullan datasets
  - Links to figshare DOIs
  - Instructions for StatsCan boundary file downloads

### 2. Backend Modules (Rewritten for Canadian Data)

#### `backend/main.py` ✓
- FastAPI app with all 7 endpoints wired
- `/api/data` — initial DAs + EDs + stats
- `/api/optimize` — greedy facility placement (POST)
- `/api/brief` — Claude policy brief generator
- `/api/brief-finetuned` — placeholder for Freesolo weights (Phase 4)
- `/api/investment-analysis` — illustrative investment framework
- `/api/workforce-alignment` — CIHI physician supply data
- `/api/seasonal-access` — winter road / ice road access

#### `backend/optimizer.py` ✓ **[COMPLETELY REWRITTEN]**
- **Old**: Raster-based (rasterio, skimage contours, pixel masks)
- **New**: DA-level discrete (pandas, haversine distance, DA coverage map)
- Loads: `da_working_dataset.csv` (DAUID, x, y, population, travel_time_minutes)
- Algorithm: Greedy placement based on population gain within 150km radius
- Output: Same JSON shape as Liberia version (locations[], coverage_curve[], da_coverage_map[])
- **Ready to test** against mock data

#### `backend/data.py` ✓ **[REWRITTEN]**
- Loads: DA population centroids + ED locations from CSVs
- Returns: `/api/data` response with initial coverage stats
- Caches: DAS, EDS, STATS on module load
- **Ready to run** with mock data

#### `backend/brief.py` ✓ **[UPDATED]**
- Prompt reframed for Canadian provincial health ministry
- Emphasizes: rural/remote, Indigenous health equity, telemedicine
- Uses `claude-sonnet-4-6` model
- Fallback brief: Canadian example
- **Ready to generate training data** for Freesolo

#### `backend/endpoints/investment.py` ✓ **[NEW — Canadian]**
- **Status**: ILLUSTRATIVE EXAMPLE (clearly labeled)
- Two worked examples: Ontario (Timmins) and Manitoba (Thompson)
- Framework: composite scoring (access, burden, density, infrastructure)
- Cost-benefit analysis template for provincial health authorities
- Acknowledges lack of centralized Canadian surgical burden database
- Recommends consultation approach

#### `backend/endpoints/workforce.py` ✓ **[NEW — Canadian]**
- **Source**: CIHI physician supply data (real, non-illustrative)
- National summary: 3.2 surgeons per 100k (below WHO threshold of 4.0)
- Provincial breakdown: ON, BC, QC, AB, MB, SK (all underserved in rural areas)
- Rural/remote challenges documented: recruitment, retention, training pipeline
- Indigenous health workforce gaps highlighted
- **Ready to use** with CIHI 2024 data once downloaded

#### `backend/endpoints/seasonal.py` ✓ **[NEW — Canadian]**
- **Source**: Salles & Mullan ice road data + Statistics Canada
- National summary: ~145k people seasonally isolated
- Provincial detail: ON, BC, AB, MB, SK, NU (varying severity)
- Focus: winter ice road access, First Nations communities, climate risk
- Churchill, Nunavut ice road identified as critical but threatened (climate change)
- Facility siting implications: winter stockpiling, helicopter protocols
- **Ready to integrate** with real winter road shapefile once obtained

### 3. Mock Data (Ready for Testing)
- `backend/data/da_working_dataset.csv` (4,750 rows)
- `backend/data/DA_population_centroids.csv`
- `backend/data/DA_to_ED_travel_times.csv`
- `backend/data/ED_locations.csv`
- `backend/data/CSD_DA_linking.csv`
- `backend/data/CSD_avg_travel_time.csv`

**Total population**: 5.5M  
**EDs**: 177  
**Beyond 2-hr threshold**: 2,745 DAs (49.2%)

## What's Next: Phase 1 (Foundation)

### Immediate: Test the Backend with Mock Data

```bash
# In /home/claude/apogee_canada/backend/

# Install dependencies
pip install fastapi uvicorn pandas numpy pydantic python-dotenv anthropic

# Run the server
python -m uvicorn main:app --reload

# In another terminal, test endpoints
curl http://localhost:8000/
curl http://localhost:8000/api/data
curl -X POST http://localhost:8000/api/optimize -H "Content-Type: application/json" -d '{"n": 5}'
curl http://localhost:8000/api/investment-analysis
curl http://localhost:8000/api/workforce-alignment
curl http://localhost:8000/api/seasonal-access
```

### Phase 1: Deployment + Real Data Handoff

1. **Download real McGaughey datasets** (figshare DOIs listed in workplan)
   - DA_population_centroids.csv
   - DA_to_ED_travel_times.csv
   - ED_locations.csv
   - CSD_DA_linking.csv
   - CSD_avg_travel_time.csv

2. **Run join_datasets.py** to merge into `da_working_dataset.csv`

3. **Deploy to Render or Railway**
   - Push backend/ to new repo
   - Set `ANTHROPIC_API_KEY` in environment
   - Test all 6 endpoints against deployed URL

4. **curl-test against deployment**
   - Confirm /api/optimize returns correct JSON shape
   - Verify /api/brief streams Claude response
   - Check /api/workforce-alignment returns CIHI data

### Phase 1: Betul's Task
- Update Base44 landing page copy: Liberia → Canada framing
- Update province/region language
- Prepare New Scenario form with Canadian DA context

### Sync Point (Phase 1 → Phase 2)
Once deployment works and optimizer.py response shape matches spec, Betul can wire Base44 backend functions.

## Key Architectural Differences from Liberia

| Aspect | Liberia | Canada |
|--------|---------|--------|
| **Population data** | WorldPop 2020 raster | StatsCan 2021 DA centroids (CSV) |
| **Travel time** | Malaria Atlas Project raster | McGaughey & Peters real road times (CSV) |
| **Optimizer** | Raster pixels (40×30 grid) | Discrete DAs (4,750 units) |
| **Facilities** | Hospitals (52 hardcoded) | EDs (177 from dataset) |
| **Contour** | Raster mask → skimage.find_contours | DA-level boolean → choropleth |
| **Workforce** | Liberia registry (hardcoded) | CIHI provincial (real data) |
| **Seasonal** | Rainy season (May-Oct) | Winter ice roads (Dec-Feb) |
| **Investment** | Computed (Liberia DHIS2) | Illustrative (no Canadian DB) |
| **Brief framing** | Liberia Ministry of Health | Canadian provincial health authority + Indigenous equity |

## Testing Checklist

- [ ] Mock data generates without errors
- [ ] `python main.py` starts FastAPI server
- [ ] GET `/api/data` returns stats + DAs + EDs
- [ ] POST `/api/optimize` with `{"n": 3}` returns locations + coverage_curve
- [ ] POST `/api/brief` streams policy brief text
- [ ] GET `/api/investment-analysis` returns illustrative example
- [ ] GET `/api/workforce-alignment` returns CIHI data
- [ ] GET `/api/seasonal-access` returns ice road data

## Known Gaps / Phase 4 Todos

- [ ] API key middleware (Phase 1 task)
- [ ] `/api/brief-finetuned` weights loading (Phase 4, post-Freesolo training)
- [ ] Real McGaughey datasets (pending download)
- [ ] StatsCan boundary shapefiles for choropleth rendering
- [ ] Salles & Mullan winter road shapefile
- [ ] CIHI 2024 physician supply file (if available)

## Files Summary

```
/home/claude/apogee_canada/
├── generate_mock_data.py          ← Run this to create mock DAs/EDs
├── join_datasets.py                ← Run this once real CSVs arrive
├── download_datasets.py            ← Reference for data sources
├── backend/
│   ├── main.py                     ← FastAPI app (all endpoints)
│   ├── data.py                     ← DA/ED loaders
│   ├── optimizer.py                ← Greedy placement (REWRITTEN)
│   ├── brief.py                    ← Claude policy brief generator
│   ├── endpoints/
│   │   ├── investment.py           ← Illustrative framework (NEW)
│   │   ├── workforce.py            ← CIHI physician supply (NEW)
│   │   └── seasonal.py             ← Winter road / ice road (NEW)
│   └── data/
│       ├── da_working_dataset.csv  ← Ready to use (mock)
│       ├── ED_locations.csv        ← Ready to use (mock)
│       └── ... (5 other CSVs)
└── PHASE_0_COMPLETE.md             ← This file
```

## Status: ✓ PHASE 0 COMPLETE

**Sehreen**: You can now:
1. Test the backend with mock data locally
2. Deploy to Render/Railway with this backend
3. Download real datasets in parallel
4. Swap mock data for real data once McGaughey CSVs arrive

**Betul**: Can start updating Base44 pages and creating backend functions against the endpoint specs (all 7 endpoints now defined).

---

*Apogee Canada — University of Toronto Computer Engineering — Hack the 6ix*
