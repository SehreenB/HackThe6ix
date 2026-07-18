# Surgical Access Policy Brief
## Liberia National Surgical, Obstetric and Anaesthesia Plan (NSOAP)
### Prepared by Apogee Solutions | April 2026

---

## Executive Summary

Liberia faces a critical surgical access crisis. Of a total population of 5,057,677, an estimated **2,147,806 people — 42.5% of the population — live beyond the 2-hour travel threshold** established by the Lancet Commission on Global Surgery as the international standard for adequate surgical access. This analysis, powered by satellite-derived population data and motorized travel-time modeling, identifies the precise geographic distribution of this gap and recommends targeted infrastructure investments to maximize population coverage.

Strategic placement of **3 new surgical facilities** at the locations identified by Apogee Solutions' coverage optimization analysis would bring an estimated **37,215 additional people** within 2-hour surgical access, representing a measurable and immediate improvement in coverage without requiring system-wide infrastructure transformation.

---

## Key Findings

**1. The access gap is severe and geographically concentrated.**
Current analysis maps 38 hospital-level facilities across Liberia, the majority concentrated in Montserrado County and the greater Monrovia area. Rural counties — particularly Nimba, Lofa, Grand Gedeh, and River Gee — show travel times exceeding 3 to 4 hours to the nearest surgical facility. For populations in these areas, the 2-hour Lancet Commission threshold is not a marginal miss — it is structurally unreachable under current infrastructure.

**2. Coverage distribution reveals a two-tier system.**
- 34.7% of the population (1,757,403 people) live within 30 minutes of a hospital
- 7.0% (354,800 people) live between 30 and 60 minutes
- 12.6% (639,168 people) live between 60 and 120 minutes
- **42.5% (2,147,806 people) live beyond 120 minutes**

This distribution reflects the historical concentration of health infrastructure in urban Monrovia, a legacy of civil war destruction (1989–2003) that eliminated approximately 95% of Liberia's health facilities, and the subsequent Ebola epidemic (2014–2016) which further strained recovery.

**3. The workforce gap compounds the access gap.**
Liberia currently operates with approximately 1 surgeon per 100,000 people. The WHO recommended minimum is 20 surgeons per 100,000. New facility placement must therefore be paired with workforce development — infrastructure without staffing does not translate to surgical access.

**4. Marginal investment yields disproportionate coverage gains.**
Optimization modeling demonstrates that the first new facility placed at the highest-priority location covers more population than facilities 4 through 10 combined. The diminishing returns curve strongly favors immediate investment in the top 3 priority sites before resources are distributed more broadly.

---

## Recommended Investment Locations

Apogee Solutions' greedy coverage maximization algorithm identified the following three facility locations as the highest-priority investments for maximizing population brought within 2-hour surgical access:

**Site 1 — Southeastern Coverage Gap**
- Coordinates: 5.8375°N, 8.6958°W
- Estimated additional population covered: 12,841 people
- Rationale: This location addresses a significant rural gap in the southeastern corridor, a region currently underserved by the existing hospital network. Placement here would serve populations in Grand Kru and Maryland counties with no current 2-hour access.

**Site 2 — Northwestern Corridor**
- Coordinates: 7.3708°N, 10.2042°W
- Estimated additional population covered: 12,518 people
- Rationale: The northwestern region bordering Sierra Leone and Guinea represents one of Liberia's most isolated population clusters. A facility at this location would serve cross-border populations and address the access gap in Lofa County's more remote districts.

**Site 3 — Central Access Gap**
- Coordinates: 6.4458°N, 9.5542°W
- Estimated additional population covered: 11,856 people
- Rationale: This central location fills a geographic gap between existing facilities in Bong and Nimba counties, reducing travel times for populations currently routed through Monrovia for surgical care.

**Combined impact of all 3 sites: 37,215 additional people within 2-hour surgical access.**

---

## Data Sources & Methodology

| Data Layer | Source | Year |
|---|---|---|
| Population raster | WorldPop, University of Southampton (UN-adjusted) | 2020 |
| Travel-time surface | Malaria Atlas Project — Motorized Healthcare Accessibility | 2020 |
| Hospital facilities | OpenStreetMap / Humanitarian Data Exchange | 2025 |
| Administrative boundaries | OCHA Common Operational Dataset | 2026 |

Travel times were computed using a motorized accessibility friction surface accounting for road quality, terrain, river crossings, and land cover. Population coverage statistics were derived by intersecting the WorldPop 100m population raster with the travel-time surface at the 120-minute threshold. Facility placement optimization used a greedy maximum coverage algorithm across 300 candidate locations distributed across Liberia's populated road corridors.

---

## Recommendations for the Ministry of Health

**Immediate (0–6 months)**
1. Validate the three priority facility locations against ground-level feasibility data — land availability, road access, community acceptance
2. Initiate workforce pipeline planning for the identified sites — surgical facility placement without staffing commitments will not translate to access improvement
3. Commission ground-truth validation of travel-time estimates against actual patient journey data in target counties

**Near-term (6–18 months)**
1. Prioritize Site 1 (southeastern corridor) for first construction — highest marginal coverage gain per dollar invested
2. Engage WHO and partner organizations for surgical workforce secondment to Sites 2 and 3 during facility construction phase
3. Integrate Apogee Solutions' coverage mapping into the NSOAP monitoring framework to track access improvement over time

**Strategic (18 months+)**
1. Extend coverage analysis to obstetric and emergency care access — the same geospatial framework applies directly
2. Model build-vs-upgrade decisions for existing basic surgical facilities identified in the current dataset
3. Replicate the methodology for Sierra Leone and Guinea to enable cross-border regional surgical planning

---

## Conclusion

The data is unambiguous: 2.1 million Liberians cannot reach surgical care within the internationally recognized 2-hour threshold. This is not a resource constraint that requires large-scale system transformation to address — targeted placement of three new facilities, informed by satellite-derived optimization, would measurably reduce this gap within a single budget cycle.

Apogee Solutions provides the Ministry of Health with the tool to move from planning blind to planning with precision. The next step is validation with Ministry partners and integration into the NSOAP process currently underway.

---

*This brief was generated by Apogee Solutions using satellite-derived population data (WorldPop 2020), motorized travel-time modeling (Malaria Atlas Project 2020), and facility data from OpenStreetMap and HDX. All statistics reflect modeled estimates and should be validated against ground-truth data before informing capital investment decisions.*

*Apogee Solutions | 7th HSIL Health Systems Innovation Hackathon | Harvard T.H. Chan School of Public Health | April 2026*
