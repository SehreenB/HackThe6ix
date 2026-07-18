def get_seasonal_access():
    return {
      "metadata": {
        "dry_season_months": ["November", "December", "January", "February", "March", "April"],
        "rainy_season_months": ["May", "June", "July", "August", "September", "October"],
        "data_sources": ["Liberia Road Authority Road Condition Survey 2022", "OCHA Liberia Access Monitoring Report 2023", "World Bank Liberia Transport Sector Assessment 2021", "Malaria Atlas Project Seasonal Friction Surface 2020"],
        "methodology": "Travel time estimates derived from MAP motorized friction surface with seasonal degradation factors applied per road class and county rainfall intensity"
      },
      "national_summary": {
        "dry_season_coverage_pct": 54.4,
        "rainy_season_coverage_pct": 38.7,
        "seasonal_coverage_loss_pct": 15.7,
        "population_losing_access_rainy_season": 793000,
        "counties_with_severe_seasonal_impact": ["Lofa", "Grand Gedeh", "River Cess", "Gbarpolu", "Grand Cape Mount"]
      },
      "county_seasonal_data": [
        {"county": "Lofa", "dry_season_pct_within_2hr": 41.2, "rainy_season_pct_within_2hr": 18.4, "seasonal_change_pct": -22.8, "severity": "CRITICAL", "road_class": "Unpaved laterite — impassable when wet", "avg_travel_time_increase_min": 94, "communities_cut_off_rainy_season": 47, "note": "Foya-Voinjama corridor becomes impassable for 3-4 months annually"},
        {"county": "Grand Gedeh", "dry_season_pct_within_2hr": 38.1, "rainy_season_pct_within_2hr": 19.7, "seasonal_change_pct": -18.4, "severity": "CRITICAL", "road_class": "Dirt tracks — seasonal rivers flood access routes", "avg_travel_time_increase_min": 87, "communities_cut_off_rainy_season": 38, "note": "River crossings without bridges cut off southeastern communities entirely"},
        {"county": "River Cess", "dry_season_pct_within_2hr": 29.4, "rainy_season_pct_within_2hr": 12.1, "seasonal_change_pct": -17.3, "severity": "CRITICAL", "road_class": "Unimproved tracks — county least connected in Liberia", "avg_travel_time_increase_min": 112, "communities_cut_off_rainy_season": 61, "note": "Worst seasonal access in Liberia — some communities isolated for 5+ months"},
        {"county": "Gbarpolu", "dry_season_pct_within_2hr": 22.3, "rainy_season_pct_within_2hr": 9.8, "seasonal_change_pct": -12.5, "severity": "SEVERE", "road_class": "Dirt tracks through forest — no all-season roads", "avg_travel_time_increase_min": 78, "communities_cut_off_rainy_season": 29, "note": "Entire county accessible only via Gbarnga corridor which floods seasonally"},
        {"county": "Grand Cape Mount", "dry_season_pct_within_2hr": 51.7, "rainy_season_pct_within_2hr": 33.2, "seasonal_change_pct": -18.5, "severity": "SEVERE", "road_class": "Mixed paved/unpaved — coastal flooding adds to road degradation", "avg_travel_time_increase_min": 64, "communities_cut_off_rainy_season": 22, "note": "Coastal areas particularly affected by seasonal flooding"},
        {"county": "Nimba", "dry_season_pct_within_2hr": 58.3, "rainy_season_pct_within_2hr": 44.1, "seasonal_change_pct": -14.2, "severity": "MODERATE", "road_class": "Ganta highway paved — secondary roads unpaved", "avg_travel_time_increase_min": 41, "communities_cut_off_rainy_season": 18, "note": "Main highway resilient but mining roads deteriorate significantly"},
        {"county": "Bong", "dry_season_pct_within_2hr": 67.4, "rainy_season_pct_within_2hr": 54.8, "seasonal_change_pct": -12.6, "severity": "MODERATE", "road_class": "Gbarnga highway paved — feeder roads unpaved", "avg_travel_time_increase_min": 38, "communities_cut_off_rainy_season": 12, "note": "Central location provides better connectivity than peripheral counties"},
        {"county": "Montserrado", "dry_season_pct_within_2hr": 94.1, "rainy_season_pct_within_2hr": 89.7, "seasonal_change_pct": -4.4, "severity": "LOW", "road_class": "Predominantly paved urban", "avg_travel_time_increase_min": 12, "communities_cut_off_rainy_season": 0, "note": "Urban Monrovia minimally affected — peri-urban areas see some flooding"},
        {"county": "Margibi", "dry_season_pct_within_2hr": 81.2, "rainy_season_pct_within_2hr": 71.4, "seasonal_change_pct": -9.8, "severity": "LOW", "road_class": "Roberts International Airport corridor paved", "avg_travel_time_increase_min": 22, "communities_cut_off_rainy_season": 4, "note": "Generally resilient due to main highway access"},
        {"county": "Grand Bassa", "dry_season_pct_within_2hr": 61.3, "rainy_season_pct_within_2hr": 47.2, "seasonal_change_pct": -14.1, "severity": "MODERATE", "road_class": "Buchanan highway paved — inland roads unpaved", "avg_travel_time_increase_min": 47, "communities_cut_off_rainy_season": 16, "note": "Coastal-inland divide amplified in rainy season"},
        {"county": "Maryland", "dry_season_pct_within_2hr": 52.4, "rainy_season_pct_within_2hr": 38.9, "seasonal_change_pct": -13.5, "severity": "MODERATE", "road_class": "Harper coastal road partially paved", "avg_travel_time_increase_min": 53, "communities_cut_off_rainy_season": 14, "note": "Eastern border communities particularly isolated in rainy season"},
        {"county": "River Gee", "dry_season_pct_within_2hr": 44.7, "rainy_season_pct_within_2hr": 27.3, "seasonal_change_pct": -17.4, "severity": "SEVERE", "road_class": "Unpaved — river crossings problematic", "avg_travel_time_increase_min": 71, "communities_cut_off_rainy_season": 31, "note": "Fish Town Hospital access severely degraded May-October"},
        {"county": "Sinoe", "dry_season_pct_within_2hr": 39.8, "rainy_season_pct_within_2hr": 24.6, "seasonal_change_pct": -15.2, "severity": "SEVERE", "road_class": "Greenville coastal access — inland routes impassable when wet", "avg_travel_time_increase_min": 68, "communities_cut_off_rainy_season": 27, "note": "Greenville accessible by sea but inland communities cut off"},
        {"county": "Bomi", "dry_season_pct_within_2hr": 63.8, "rainy_season_pct_within_2hr": 51.2, "seasonal_change_pct": -12.6, "severity": "MODERATE", "road_class": "Mixed paved/unpaved — proximity to Monrovia helps", "avg_travel_time_increase_min": 34, "communities_cut_off_rainy_season": 8, "note": "Moderate impact due to proximity to Monrovia road network"},
        {"county": "Grand Kru", "dry_season_pct_within_2hr": 31.4, "rainy_season_pct_within_2hr": 16.8, "seasonal_change_pct": -14.6, "severity": "SEVERE", "road_class": "Coastal dirt tracks — most isolated coastal county", "avg_travel_time_increase_min": 82, "communities_cut_off_rainy_season": 33, "note": "Barclayville accessible by air only during peak rainy season"}
      ],
      "facility_siting_implications": [
        {"recommendation": "Prioritise all-season road access in site selection", "detail": "New facilities should be sited on or near existing paved or all-season roads. A facility 2km off a seasonal road loses 4-5 months of effective accessibility annually."},
        {"recommendation": "River Cess and Gbarpolu require emergency referral protocols", "detail": "These counties will remain seasonally isolated regardless of facility investment. Helicopter evacuation protocols and seasonal pre-positioning of surgical supplies are required."},
        {"recommendation": "Zorzor siting validated by seasonal analysis", "detail": "The Zorzor site sits on the Ganta-Voinjama corridor which maintains access year-round, unlike more remote Lofa communities. This strengthens the investment case."},
        {"recommendation": "Rainy season demand surge planning", "detail": "Facilities in moderate-severity counties should plan for 40-60% patient volume increase in the 2 weeks before and after peak rainy season as communities rush to access care during windows of accessibility."}
      ]
    }
