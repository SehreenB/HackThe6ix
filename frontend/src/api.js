const BASE = "http://localhost:8000"

/**
 * GET /api/data
 * Returns { stats, facilities, contour }
 */
export async function fetchData() {
  const res = await fetch(`${BASE}/api/data`)
  if (!res.ok) throw new Error(`fetchData failed: ${res.status} ${res.statusText}`)
  return res.json()
}

/**
 * POST /api/optimize
 * @param {number} n - number of new facilities to place
 * Returns { locations, updated_stats, coverage_curve, updated_contour }
 */
export async function runOptimizer(n) {
  const res = await fetch(`${BASE}/api/optimize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ n })
  })
  if (!res.ok) throw new Error(`runOptimizer failed: ${res.status} ${res.statusText}`)
  return res.json()
}

/**
 * POST /api/brief
 * Returns a ReadableStream for streaming text consumption
 */
export async function streamBrief(stats, optimizerResults) {
  const res = await fetch(`${BASE}/api/brief`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ stats, optimizer_results: optimizerResults })
  })
  if (!res.ok) throw new Error(`streamBrief failed: ${res.status} ${res.statusText}`)
  return res.body
}

/**
 * GET /api/investment-analysis
 */
export async function fetchInvestmentAnalysis() {
  const res = await fetch(`${BASE}/api/investment-analysis`)
  if (!res.ok) throw new Error(`fetchInvestmentAnalysis failed: ${res.status}`)
  return res.json()
}

/**
 * GET /api/workforce-alignment
 */
export async function fetchWorkforceAlignment() {
  const res = await fetch(`${BASE}/api/workforce-alignment`)
  if (!res.ok) throw new Error(`fetchWorkforceAlignment failed: ${res.status}`)
  return res.json()
}

/**
 * GET /api/seasonal-access
 */
export async function fetchSeasonalAccess() {
  const res = await fetch(`${BASE}/api/seasonal-access`)
  if (!res.ok) throw new Error(`fetchSeasonalAccess failed: ${res.status}`)
  return res.json()
}
