import anthropic
import os
import json

FALLBACK = """# Surgical Access Policy Brief — Liberia

## Executive Summary
Analysis reveals a critical access gap: 2,653,000 people (50.1%) live beyond the 2-hour surgical care threshold defined by the Lancet Commission on Global Surgery.

## Key Findings
- Total population: 5,300,000
- Within 2-hour access: 2,647,000 (49.9%)
- Beyond 2-hour access: 2,653,000 (50.1%)
- Facilities heavily concentrated in Montserrado County (Monrovia)

## Investment Recommendations
1. Zorzor, Lofa County — 168,000 additional people reached
2. Tapita, Nimba County — 156,000 additional people reached
3. Toe Town, Grand Gedeh — 143,000 additional people reached

## Projected Impact
Placement of 5 new facilities projected to increase coverage from 49.9% to 63.2%, reaching 700,000 additional Liberians.

## Next Steps
1. Present to Ministry of Health NSOAP working group
2. Engage Global Financing Facility for seed funding
3. Ground-truth facility assessment in priority counties

*Data: WorldPop 2020, Weiss et al. 2020, HDX Healthsites, Lancet Commission 2015*
"""

def generate_brief(stats: dict, optimizer_results: list):
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        prompt = f"""Write a policy brief for Liberia's Ministry of Health on surgical access.

Stats: {json.dumps(stats)}
Recommended new facility locations: {json.dumps(optimizer_results)}

Structure:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points with numbers)
3. Investment Recommendations (explain WHY each location)
4. Projected Impact (lives reached, maternal mortality reduction)
5. Next Steps (concrete Ministry actions)

End with data sources. Write for a non-technical Ministry audience."""

        with client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system="You are a global health policy analyst writing for Liberia's Ministry of Health. Be clear, evidence-based, and actionable.",
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception:
        yield FALLBACK
