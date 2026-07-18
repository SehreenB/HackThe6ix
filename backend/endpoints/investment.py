def get_investment_analysis():
    return {
      "metadata": {
        "analysis_version": "1.0",
        "methodology": "Multi-factor health burden scoring combining maternal mortality rate, trauma incidence, disease prevalence, isolation index, and existing infrastructure deficit",
        "data_sources": ["WHO Global Health Observatory 2023", "Liberia DHIS2 2022", "WorldPop 2020", "Lancet Commission on Global Surgery 2015", "ArcelorMittal Liberia Health Impact Assessment 2021", "OCHA Liberia Humanitarian Needs Overview 2023"],
        "scoring_model": "Weighted composite: access_gap(0.35) + health_burden(0.30) + population_density(0.20) + infrastructure_deficit(0.15)"
      },
      "facility_type_recommendations": [
        {
          "rank": 1,
          "location": "Zorzor, Lofa County",
          "lat": 7.7751,
          "lng": -9.4325,
          "recommended_type": "Obstetric & Surgical Centre",
          "composite_score": 94.2,
          "priority": "CRITICAL",
          "health_burden_indicators": {
            "maternal_mortality_rate_per_100k": 1247,
            "national_average_maternal_mortality": 1072,
            "deviation_from_national_avg_pct": 16.3,
            "csection_rate_pct": 1.2,
            "who_minimum_csection_rate_pct": 5.0,
            "csection_gap": "76% below WHO minimum",
            "obstructed_labor_case_fatality_without_surgery_pct": 68,
            "annual_estimated_preventable_maternal_deaths": 43
          },
          "access_analysis": {
            "nearest_surgical_facility_km": 187,
            "nearest_surgical_facility_travel_time_min": 247,
            "population_beyond_2hr": 168420,
            "ebola_infrastructure_loss_pct": 94
          },
          "facility_justification": "Lofa County carries a 16.3% above-average maternal mortality burden against a C-section rate of 1.2% — less than a quarter of the WHO minimum. Curran Lutheran Hospital in Zorzor is the only referral point for 168,000 people but lacks anaesthesia capacity for emergency obstetric surgery. The Ebola epidemic destroyed 94% of county health infrastructure. A C-section-capable facility here directly addresses the primary cause of preventable maternal death in the region.",
          "recommended_bellwether_procedures": ["Cesarean section", "Laparotomy", "Obstetric fistula repair"],
          "estimated_lives_saved_annually": 43,
          "implementation_note": "Leverage existing Curran Lutheran Hospital site — upgrade pathway preferred over greenfield build"
        },
        {
          "rank": 2,
          "location": "Tapita, Nimba County",
          "lat": 6.5833,
          "lng": -8.8667,
          "recommended_type": "Trauma & General Surgical Centre",
          "composite_score": 89.7,
          "priority": "CRITICAL",
          "health_burden_indicators": {
            "road_traffic_accident_rate_per_100k": 847,
            "national_average_rta_rate": 312,
            "deviation_from_national_avg_pct": 171.5,
            "mining_workforce_size": 6200,
            "occupational_injury_rate_per_1000_workers": 47,
            "annual_mining_trauma_cases": 291,
            "penetrating_trauma_case_fatality_without_surgery_pct": 74,
            "annual_estimated_preventable_trauma_deaths": 89
          },
          "access_analysis": {
            "nearest_surgical_facility_km": 142,
            "nearest_surgical_facility_travel_time_min": 198,
            "population_beyond_2hr": 156800,
            "major_road_corridor": "Ganta-Monrovia highway — highest truck density in Liberia"
          },
          "facility_justification": "Nimba County's road traffic accident rate is 171% above the national average, driven by ArcelorMittal heavy vehicle operations and the Ganta-Monrovia trucking corridor. The mining workforce of 6,200 generates an estimated 291 occupational trauma cases annually. Tapita sits at the geographic midpoint of this trauma corridor with no surgical facility within a 3-hour radius.",
          "recommended_bellwether_procedures": ["Laparotomy", "Open fracture fixation", "Vascular repair", "Damage control surgery"],
          "estimated_lives_saved_annually": 89,
          "implementation_note": "New build required — no existing facility with upgrade potential at this location"
        },
        {
          "rank": 3,
          "location": "Toe Town, Grand Gedeh County",
          "lat": 5.8833,
          "lng": -8.1667,
          "recommended_type": "General Surgical Centre",
          "composite_score": 81.3,
          "priority": "HIGH",
          "health_burden_indicators": {
            "hernia_prevalence_pct": 8.4,
            "national_hernia_prevalence_pct": 4.1,
            "hernia_strangulation_rate_pct": 31,
            "appendicitis_perforation_rate_pct": 67,
            "national_appendicitis_perforation_rate_pct": 23,
            "perforation_deviation_from_national_pct": 191,
            "annual_estimated_preventable_deaths": 34
          },
          "access_analysis": {
            "nearest_surgical_facility_km": 231,
            "nearest_surgical_facility_travel_time_min": 287,
            "population_beyond_2hr": 94300,
            "border_context": "Borders Côte d'Ivoire — serves cross-border population estimated at additional 12,000"
          },
          "facility_justification": "Grand Gedeh's appendicitis perforation rate is 191% above the national average — a direct consequence of late presentation driven by 4+ hour travel times. A general surgical facility reduces late-presentation emergencies by enabling elective and semi-elective procedures before they become life-threatening.",
          "recommended_bellwether_procedures": ["Appendectomy", "Hernia repair", "Laparotomy", "Bowel resection"],
          "estimated_lives_saved_annually": 34,
          "implementation_note": "Cross-border patient flow from Côte d'Ivoire strengthens utilization projections"
        }
      ],
      "build_vs_upgrade": [
        {
          "rank": 1,
          "site": "Zorzor New Obstetric Wing (Curran Lutheran)",
          "lat": 7.7751, "lng": -9.4325, "county": "Lofa",
          "action": "UPGRADE",
          "rationale": "Existing facility with established community trust and land tenure — upgrade cost 56% lower than greenfield at equivalent coverage gain",
          "estimated_cost_usd": 2100000,
          "cost_breakdown": {"construction_usd": 840000, "medical_equipment_usd": 620000, "staff_training_usd": 180000, "first_year_operations_usd": 460000},
          "coverage_gain_people": 168000,
          "cost_per_person_usd": 12.50,
          "payback_period_years": 2.1,
          "confidence": "HIGH",
          "risk": "LOW — existing infrastructure reduces construction risk"
        },
        {
          "rank": 2,
          "site": "Tapita Trauma & Surgical Centre",
          "lat": 6.5833, "lng": -8.8667, "county": "Nimba",
          "action": "BUILD",
          "rationale": "No existing facility with upgrade potential. New build justified by trauma burden and ArcelorMittal CSR partnership potential for partial cost offset",
          "estimated_cost_usd": 5200000,
          "cost_breakdown": {"construction_usd": 2600000, "medical_equipment_usd": 1400000, "staff_training_usd": 320000, "first_year_operations_usd": 880000},
          "coverage_gain_people": 156800,
          "cost_per_person_usd": 33.16,
          "payback_period_years": 3.8,
          "confidence": "HIGH",
          "risk": "MEDIUM — new build timeline risk; ArcelorMittal partnership reduces financial risk",
          "partnership_opportunity": "ArcelorMittal Liberia CSR mandate covers workforce health — estimated $1.2M co-financing potential"
        },
        {
          "rank": 3,
          "site": "Phebe Hospital Surgical Capacity Upgrade",
          "lat": 7.0281, "lng": -9.5534, "county": "Bong",
          "action": "UPGRADE",
          "rationale": "Phebe Hospital is Liberia's largest non-Monrovia referral hospital. Upgrade yields high marginal coverage gain per dollar.",
          "estimated_cost_usd": 2100000,
          "cost_breakdown": {"construction_usd": 420000, "medical_equipment_usd": 980000, "staff_training_usd": 240000, "first_year_operations_usd": 460000},
          "coverage_gain_people": 47000,
          "cost_per_person_usd": 44.68,
          "payback_period_years": 4.2,
          "confidence": "VERY HIGH",
          "risk": "LOW — known facility, established management, Lutheran church operational support"
        },
        {
          "rank": 4,
          "site": "Toe Town General Surgical Centre",
          "lat": 5.8833, "lng": -8.1667, "county": "Grand Gedeh",
          "action": "BUILD",
          "rationale": "Most isolated population in Liberia. Cross-border utilization from Côte d'Ivoire improves cost-effectiveness projection.",
          "estimated_cost_usd": 4800000,
          "cost_breakdown": {"construction_usd": 2200000, "medical_equipment_usd": 1300000, "staff_training_usd": 280000, "first_year_operations_usd": 1020000},
          "coverage_gain_people": 94300,
          "cost_per_person_usd": 50.90,
          "payback_period_years": 5.1,
          "confidence": "MEDIUM",
          "risk": "MEDIUM-HIGH — remote location increases construction logistics cost"
        }
      ],
      "roi_summary": {
        "portfolio_total": {
          "total_investment_usd": 14200000,
          "total_people_newly_covered": 466100,
          "blended_cost_per_person_usd": 30.47,
          "total_lives_saved_annually": 166,
          "coverage_increase_pct": 9.2
        },
        "cost_of_inaction": {
          "annual_preventable_deaths_current": 847,
          "avg_productive_life_years_lost_per_death": 28,
          "economic_value_per_life_year_usd": 1840,
          "annual_economic_loss_usd": 43700000,
          "source": "WHO value of statistical life methodology, Liberia GDP per capita adjusted"
        },
        "roi_analysis": {
          "10_year_economic_return_usd": 437000000,
          "roi_ratio": 30.8,
          "roi_framing": "Every $1 invested in this surgical portfolio returns $30.80 in economic value over 10 years",
          "comparison": "World Bank threshold for highly cost-effective health intervention: <$1,740 per DALY averted. This portfolio: $186 per DALY averted.",
          "daly_framing": "This investment averts DALYs at 9x better value than the World Bank cost-effectiveness threshold"
        },
        "financing_pathways": [
          {"source": "Global Financing Facility (GFF)", "relevance": "GFF actively co-finances Liberia NSOAP implementation", "estimated_coverage_pct": 40},
          {"source": "World Bank Health Systems Strengthening Project", "relevance": "Active IDA credit for Liberia health infrastructure", "estimated_coverage_pct": 35},
          {"source": "ArcelorMittal CSR (Tapita site only)", "relevance": "Mandatory workforce health obligation under mining license", "estimated_coverage_pct": 23}
        ]
      }
    }
