def get_workforce_alignment():
    return {
      "metadata": {
        "data_sources": ["Liberia Health Workforce Registry 2022", "WHO Global Health Observatory 2023", "Liberia Medical and Dental Council 2022", "Lancet Commission on Global Surgery 2015"],
        "who_minimums": {"surgeons_per_100k": 4.0, "anaesthetists_per_100k": 4.0, "obstetricians_per_100k": 4.0, "nurses_per_100k": 100.0},
        "liberia_national_averages": {"surgeons_per_100k": 1.4, "anaesthetists_per_100k": 0.8, "obstetricians_per_100k": 1.1, "nurses_per_100k": 27.3, "total_surgical_workforce": 847}
      },
      "county_workforce": [
        {"county": "Montserrado", "population": 1764000, "surgeons_per_100k": 4.2, "anaesthetists_per_100k": 2.1, "obstetricians_per_100k": 3.8, "nurses_per_100k": 68.4, "meets_who_minimum": False, "workforce_gap_score": 42, "note": "Most concentrated workforce in Liberia due to Monrovia hospitals"},
        {"county": "Bong", "population": 333000, "surgeons_per_100k": 1.8, "anaesthetists_per_100k": 0.6, "obstetricians_per_100k": 0.9, "nurses_per_100k": 22.1, "meets_who_minimum": False, "workforce_gap_score": 71, "note": "Phebe Hospital is primary employer — single point of failure"},
        {"county": "Nimba", "population": 468000, "surgeons_per_100k": 1.2, "anaesthetists_per_100k": 0.4, "obstetricians_per_100k": 0.6, "nurses_per_100k": 18.7, "meets_who_minimum": False, "workforce_gap_score": 84, "note": "Largest rural county — critically understaffed relative to population"},
        {"county": "Lofa", "population": 276000, "surgeons_per_100k": 0.7, "anaesthetists_per_100k": 0.4, "obstetricians_per_100k": 0.4, "nurses_per_100k": 14.2, "meets_who_minimum": False, "workforce_gap_score": 91, "note": "Ebola destroyed 94% of health infrastructure and workforce 2014-2016"},
        {"county": "Grand Gedeh", "population": 135000, "surgeons_per_100k": 0.7, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 0.7, "nurses_per_100k": 12.4, "meets_who_minimum": False, "workforce_gap_score": 94, "note": "No anaesthetist in entire county — any surgical facility requires staff transfer"},
        {"county": "Maryland", "population": 135000, "surgeons_per_100k": 1.5, "anaesthetists_per_100k": 0.7, "obstetricians_per_100k": 1.5, "nurses_per_100k": 19.3, "meets_who_minimum": False, "workforce_gap_score": 72, "note": "J.J. Dossen Hospital maintains minimum surgical capacity"},
        {"county": "Margibi", "population": 209000, "surgeons_per_100k": 1.9, "anaesthetists_per_100k": 1.0, "obstetricians_per_100k": 1.4, "nurses_per_100k": 31.2, "meets_who_minimum": False, "workforce_gap_score": 63, "note": "Proximity to Monrovia allows some workforce sharing"},
        {"county": "Grand Bassa", "population": 221000, "surgeons_per_100k": 0.9, "anaesthetists_per_100k": 0.5, "obstetricians_per_100k": 0.9, "nurses_per_100k": 16.8, "meets_who_minimum": False, "workforce_gap_score": 79, "note": "Buchanan port city has some capacity but rural areas critically underserved"},
        {"county": "River Gee", "population": 71000, "surgeons_per_100k": 1.4, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 1.4, "nurses_per_100k": 11.3, "meets_who_minimum": False, "workforce_gap_score": 93, "note": "No anaesthetist — Fish Town Hospital surgical capacity severely limited"},
        {"county": "Sinoe", "population": 102000, "surgeons_per_100k": 1.0, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 1.0, "nurses_per_100k": 13.1, "meets_who_minimum": False, "workforce_gap_score": 88, "note": "Greenville hospital lacks anaesthesia capacity"},
        {"county": "Gbarpolu", "population": 83000, "surgeons_per_100k": 0.0, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 0.0, "nurses_per_100k": 8.4, "meets_who_minimum": False, "workforce_gap_score": 99, "note": "No surgical staff at all — entirely dependent on referral to Bong or Montserrado"},
        {"county": "Grand Cape Mount", "population": 127000, "surgeons_per_100k": 0.8, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 0.8, "nurses_per_100k": 10.7, "meets_who_minimum": False, "workforce_gap_score": 92, "note": "St. Timothy Hospital has nursing staff but no anaesthesia"},
        {"county": "Bomi", "population": 84000, "surgeons_per_100k": 1.2, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 1.2, "nurses_per_100k": 15.6, "meets_who_minimum": False, "workforce_gap_score": 87, "note": "No anaesthetist — surgical procedures require transfer to Montserrado"},
        {"county": "Grand Kru", "population": 57000, "surgeons_per_100k": 1.8, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 1.8, "nurses_per_100k": 9.8, "meets_who_minimum": False, "workforce_gap_score": 91, "note": "Barclayville — most isolated county with no anaesthesia capacity"},
        {"county": "River Cess", "population": 72000, "surgeons_per_100k": 0.0, "anaesthetists_per_100k": 0.0, "obstetricians_per_100k": 0.0, "nurses_per_100k": 7.2, "meets_who_minimum": False, "workforce_gap_score": 99, "note": "No surgical staff — most underserved county in Liberia"}
      ],
      "training_institutions": [
        {"name": "A.M. Dogliotti College of Medicine", "location": "Monrovia, Montserrado", "lat": 6.32, "lng": -10.80, "programs": ["Surgery", "Obstetrics", "Anaesthesia", "Nursing"], "annual_surgical_graduates": 12, "note": "Only medical school in Liberia — produces 12 surgical specialists annually"},
        {"name": "Phebe Hospital School of Nursing", "location": "Gbarnga, Bong", "lat": 7.03, "lng": -9.47, "programs": ["Nursing", "Midwifery"], "annual_surgical_graduates": 45, "note": "Primary nursing training institution outside Monrovia"},
        {"name": "Tubman National Institute of Medical Arts", "location": "Monrovia, Montserrado", "lat": 6.30, "lng": -10.79, "programs": ["Nursing", "Medical Technology", "Pharmacy"], "annual_surgical_graduates": 60, "note": "Produces majority of Liberia allied health workforce"}
      ],
      "priority_sites_alignment": [
        {
          "location": "Zorzor, Lofa County",
          "recommended_facility_type": "Obstetric & Surgical Centre",
          "county_workforce_gap_score": 91,
          "staffing_requirement": {"surgeons_needed": 2, "anaesthetists_needed": 1, "obstetricians_needed": 2, "nurses_needed": 15},
          "current_county_capacity": {"surgeons_available": 2, "anaesthetists_available": 1, "obstetricians_available": 1, "nurses_available": 39},
          "staffing_gap": {"surgeons": 0, "anaesthetists": 0, "obstetricians": 1, "nurses": 0},
          "feasibility": "FEASIBLE WITH TRAINING",
          "recommendation": "Existing Curran Lutheran staff can transition. 1 additional obstetrician required — 18-month training pipeline via A.M. Dogliotti. Facility operational within 24 months.",
          "estimated_time_to_staff_months": 24
        },
        {
          "location": "Tapita, Nimba County",
          "recommended_facility_type": "Trauma & General Surgical Centre",
          "county_workforce_gap_score": 84,
          "staffing_requirement": {"surgeons_needed": 2, "anaesthetists_needed": 2, "obstetricians_needed": 1, "nurses_needed": 20},
          "current_county_capacity": {"surgeons_available": 6, "anaesthetists_available": 2, "obstetricians_available": 3, "nurses_available": 88},
          "staffing_gap": {"surgeons": 0, "anaesthetists": 0, "obstetricians": 0, "nurses": 0},
          "feasibility": "IMMEDIATELY FEASIBLE",
          "recommendation": "Nimba County has sufficient workforce concentrated at Ganta United Methodist Hospital. Staff redeployment to Tapita is operationally viable. ArcelorMittal medical staff provides supplementary capacity.",
          "estimated_time_to_staff_months": 6
        },
        {
          "location": "Toe Town, Grand Gedeh County",
          "recommended_facility_type": "General Surgical Centre",
          "county_workforce_gap_score": 94,
          "staffing_requirement": {"surgeons_needed": 1, "anaesthetists_needed": 1, "obstetricians_needed": 1, "nurses_needed": 12},
          "current_county_capacity": {"surgeons_available": 1, "anaesthetists_available": 0, "obstetricians_available": 1, "nurses_available": 17},
          "staffing_gap": {"surgeons": 0, "anaesthetists": 1, "obstetricians": 0, "nurses": 0},
          "feasibility": "REQUIRES WORKFORCE INVESTMENT",
          "recommendation": "Critical anaesthesia gap — Grand Gedeh has zero anaesthetists. Requires sponsoring 2 candidates through A.M. Dogliotti 24-month anaesthesia programme before facility can operate.",
          "estimated_time_to_staff_months": 36
        }
      ],
      "system_summary": {
        "counties_with_no_anaesthetist": 7,
        "counties_with_no_surgical_staff": 2,
        "total_additional_surgeons_needed_for_who_minimum": 134,
        "total_additional_anaesthetists_needed_for_who_minimum": 187,
        "years_to_fill_gap_at_current_training_rate": 11.2,
        "key_insight": "Anaesthesia is the binding constraint on surgical scale-up in Liberia. 7 of 15 counties have zero anaesthetists. Infrastructure investment without parallel anaesthesia training pipeline will produce facilities that cannot operate."
      }
    }
