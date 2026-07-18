import { useState, useEffect } from "react"
import { fetchInvestmentAnalysis } from "../api"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts"

const PRIORITY_COLOR = { "CRITICAL": "#FF4B6E", "HIGH": "#F4A261", "MODERATE": "#fbbf24" }
const ACTION_COLOR   = { "UPGRADE": "#00E5FF", "BUILD": "#F4A261" }

export default function InvestmentTab({ coverageCurve }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchInvestmentAnalysis()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingState label="Investment Analysis" />

  const roi = data.roi_summary
  const hasCurve = coverageCurve && coverageCurve.length > 0

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50" style={{ scrollbarWidth: "thin" }}>
      <div className="max-w-6xl mx-auto px-8 py-8 flex flex-col gap-8">

        {/* Header */}
        <div>
          <div className="text-[9px] font-black text-gray-400 uppercase tracking-[0.3em] mb-1">Investment Protocol</div>
          <h1 className="text-2xl font-black text-slate-800 tracking-tight">Investment Analysis</h1>
          <p className="text-gray-500 text-sm mt-1">Facility-level cost-effectiveness modelling for surgical access expansion</p>
        </div>

        {/* ROI Summary Cards */}
        <div className="grid grid-cols-4 gap-4">
          <StatCard label="Total Investment" value={`$${(roi.portfolio_total.total_investment_usd/1e6).toFixed(1)}M`} sub="Portfolio total" accent="#00E5FF" />
          <StatCard label="Lives Saved/Yr" value={roi.portfolio_total.total_lives_saved_annually} sub="Preventable deaths averted" accent="#4ade80" />
          <StatCard label="Cost per DALY" value="$186" sub="vs $1,740 WHO threshold" accent="#a78bfa" />
          <StatCard label="10-yr ROI" value={`${roi.roi_analysis.roi_ratio}x`} sub="Every $1 → $30.80 returned" accent="#F4A261" />
        </div>

        {/* Coverage Curve */}
        {hasCurve ? (
          <Section title="Coverage Curve" subtitle="Population coverage gain per facility added (from optimizer run)">
            <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={coverageCurve} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="n_facilities" label={{ value: "Facilities Added", position: "insideBottom", offset: -2, style: { fontSize: 10, fill: "#94a3b8" } }} tick={{ fontSize: 11, fill: "#94a3b8" }} />
                  <YAxis domain={[50, 100]} tickFormatter={v => `${v}%`} tick={{ fontSize: 11, fill: "#94a3b8" }} />
                  <Tooltip formatter={(v) => `${v}%`} contentStyle={{ borderRadius: 8, border: "1px solid #e2e8f0", fontSize: 12 }} />
                  <Line type="monotone" dataKey="pct_covered" stroke="#00E5FF" strokeWidth={2.5} dot={{ fill: "#00E5FF", r: 5 }} activeDot={{ r: 7 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Section>
        ) : (
          <div className="bg-white border border-dashed border-gray-200 rounded-2xl p-6 text-center text-gray-400 text-sm">
            Run the optimizer on the Mission Map to generate the coverage curve chart
          </div>
        )}

        {/* Priority Sites */}
        <Section title="Priority Facility Recommendations" subtitle="Ranked by composite health burden score">
          <div className="flex flex-col gap-4">
            {data.facility_type_recommendations.map(site => (
              <div key={site.rank} className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="flex items-center gap-3 mb-1">
                      <span className="text-lg font-black text-slate-800">#{site.rank} — {site.location}</span>
                      <span className="text-[9px] font-black px-2 py-0.5 rounded-full uppercase tracking-widest" style={{ background: PRIORITY_COLOR[site.priority] + "20", color: PRIORITY_COLOR[site.priority] }}>
                        {site.priority}
                      </span>
                    </div>
                    <div className="text-sm text-gray-500">{site.recommended_type}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-black text-slate-800">{site.composite_score}</div>
                    <div className="text-[9px] font-bold text-gray-400 uppercase">Score</div>
                  </div>
                </div>
                <p className="text-sm text-gray-600 leading-relaxed border-t border-gray-50 pt-4">{site.facility_justification}</p>
                <div className="flex items-center gap-4 mt-4">
                  <div className="text-sm font-black text-slate-800">{site.estimated_lives_saved_annually} lives/yr</div>
                  <div className="text-sm text-gray-400">·</div>
                  <div className="text-sm text-gray-500">{(site.access_analysis.population_beyond_2hr).toLocaleString()} people reached</div>
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* Build vs Upgrade Matrix */}
        <Section title="Build vs Upgrade Matrix" subtitle="Cost, coverage gain, and risk per site">
          <div className="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="px-5 py-3 text-left text-[9px] font-black text-gray-400 uppercase tracking-widest">Site</th>
                  <th className="px-5 py-3 text-left text-[9px] font-black text-gray-400 uppercase tracking-widest">Action</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Cost</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">$/Person</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Coverage Gain</th>
                  <th className="px-5 py-3 text-left text-[9px] font-black text-gray-400 uppercase tracking-widest">Risk</th>
                </tr>
              </thead>
              <tbody>
                {data.build_vs_upgrade.map((row, i) => (
                  <tr key={i} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                    <td className="px-5 py-4 font-bold text-slate-800">{row.site}</td>
                    <td className="px-5 py-4">
                      <span className="text-[9px] font-black px-2 py-1 rounded-full uppercase tracking-widest" style={{ background: ACTION_COLOR[row.action] + "20", color: ACTION_COLOR[row.action] }}>
                        {row.action}
                      </span>
                    </td>
                    <td className="px-5 py-4 text-right font-bold text-slate-700">${(row.estimated_cost_usd/1e6).toFixed(1)}M</td>
                    <td className="px-5 py-4 text-right text-gray-600">${row.cost_per_person_usd.toFixed(2)}</td>
                    <td className="px-5 py-4 text-right text-gray-600">{row.coverage_gain_people.toLocaleString()}</td>
                    <td className="px-5 py-4 text-gray-500 text-xs">{row.risk.split("—")[0]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>

        {/* Financing */}
        <Section title="Financing Pathways" subtitle="Identified funding mechanisms">
          <div className="grid grid-cols-3 gap-4">
            {roi.financing_pathways.map((fp, i) => (
              <div key={i} className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
                <div className="text-2xl font-black text-slate-800 mb-1">{fp.estimated_coverage_pct}%</div>
                <div className="text-sm font-bold text-slate-700 mb-2">{fp.source}</div>
                <div className="text-xs text-gray-400">{fp.relevance}</div>
              </div>
            ))}
          </div>
        </Section>

      </div>
    </div>
  )
}

function Section({ title, subtitle, children }) {
  return (
    <div>
      <div className="mb-4">
        <h2 className="text-base font-black text-slate-800 uppercase tracking-tight">{title}</h2>
        {subtitle && <p className="text-gray-400 text-xs mt-0.5">{subtitle}</p>}
      </div>
      {children}
    </div>
  )
}

function StatCard({ label, value, sub, accent }) {
  return (
    <div className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
      <div className="text-[9px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">{label}</div>
      <div className="text-2xl font-black tracking-tight" style={{ color: accent }}>{value}</div>
      <div className="text-xs text-gray-400 mt-1">{sub}</div>
    </div>
  )
}

function LoadingState({ label }) {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 rounded-full border-2 border-earth-blue border-t-transparent animate-spin" />
        <div className="text-[10px] font-black text-gray-400 uppercase tracking-[0.3em]">Loading {label}</div>
      </div>
    </div>
  )
}
