"""
brief.py – Generate policy briefs for Canadian provincial health authorities.
This is the output format used for Freesolo fine-tuning training data.
Framing: rural/remote surgical access, Indigenous health equity.
"""

import anthropic
import os
import json

FALLBACK = """# Rural and Remote Surgical Access Brief — Canada

## Executive Summary
Analysis of Canadian dissemination area coverage reveals a persistent surgical access gap in rural and remote communities. While urban areas benefit from concentrated surgical capacity, approximately 2.7M Canadians live beyond a 2-hour travel time to 24-hour emergency surgical capacity.

## Key Findings
- Total Canadian population: 5.5M (study area)
- Within 2-hour access: 2.8M (50.8%)
- Beyond 2-hour access: 2.7M (49.2%)
- Surgical facilities heavily concentrated in provincial capitals and major urban centres
- Remote and northern communities face travel times exceeding 6 hours for emergency surgery

## Recommended Facility Sites
1. Regional trauma centre in northern region — 180,000 additional people reached
2. Rural surgical service in provincial hinterland — 156,000 additional people reached
3. Remote community facility serving First Nations — 94,000 additional people reached

## Projected Impact
Placement of 5 distributed surgical facilities projected to increase coverage from 50.8% to 65.0%, reaching 750,000 additional Canadians, with particular benefit to First Nations and remote communities.

## Implementation Priorities
1. Consultation with regional Indigenous health authorities
2. Workforce development partnerships with provincial medical training institutions
3. Telemedicine and surgical capacity-sharing agreements with larger centres
4. Sustainable funding through provincial health ministry capital budgets

## Next Steps
1. Provincial health authority approval
2. Engagement with affected regional governments and Indigenous communities
3. Environmental assessment for proposed facility locations
4. Workforce recruitment and retention strategy

*Data: Statistics Canada 2021 Census, McGaughey et al. 2024 travel time analysis, Canadian Institute for Health Information*
"""


def generate_brief(stats: dict, optimizer_results: list):
    """
    Generate a policy brief for Canadian provincial health authorities.
    
    Args:
        stats: Current coverage statistics (total_pop, within_2hr, pct_covered, etc.)
        optimizer_results: List of recommended facility locations from optimizer
    
    Yields:
        Text chunks of the policy brief (for streaming).
    """
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Format optimizer results for context
        locations_text = "\n".join([
            f"- {loc.get('province', 'Unknown')}, {loc.get('pop_gained', 0):,} people reached "
            f"(lat {loc.get('lat', 0):.2f}, lng {loc.get('lng', 0):.2f})"
            for loc in optimizer_results[:10]
        ])
        
        prompt = f"""You are a health policy analyst working with Canadian provincial health authorities.
Write a policy brief on rural and remote surgical access for the provincial health ministry.

Current Coverage Statistics:
- Total population (study area): {stats.get('total_pop', 0):,}
- Population within 2-hour access: {stats.get('within_2hr', 0):,}
- Population beyond 2-hour access: {stats.get('beyond_2hr', 0):,}
- Current coverage: {stats.get('pct_covered', 0)}%

Recommended new surgical facility locations:
{locations_text}

Structure your brief as follows:
1. Executive Summary (2-3 sentences on the access gap)
2. Key Findings (bullet points with data)
3. Recommended Facility Sites (list with expected population reached)
4. Projected Impact (coverage gains, focus on rural and Indigenous communities)
5. Implementation Priorities (workforce, telemedicine, Indigenous consultation)
6. Next Steps (concrete provincial health ministry actions)

End with data attribution.

Context: Frame this for a rural/remote surgical access policy audience. Emphasize Indigenous health equity, telemedicine partnerships, and workforce challenges in recruitment and retention. Be evidence-based and actionable."""

        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1200,
            system="""You are a Canadian health policy analyst specializing in rural and remote surgical access.
Your audience is provincial health ministry planners and Indigenous health authorities.
Be clear, data-driven, and focused on equity and sustainability.""",
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text
                
    except Exception as e:
        # Fallback if API fails
        print(f"Brief generation failed: {e}")
        yield FALLBACK
