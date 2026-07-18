import { useState, useEffect } from "react"
import { fetchWorkforceAlignment } from "../api"

const GAP_COLOR = (score) => {
  if (score >= 90) return { bg: "#FF4B6E20", text: "#FF4B6E", label: "CRITICAL" }
  if (score >= 70) return { bg: "#F4A26120", text: "#F4A261", label: "SEVERE" }
  return { bg: "#fbbf2420", text: "#f59e0b", label: "MODERATE" }
}

const FEASIBILITY_STYLE = {
  "IMMEDIATELY FEASIBLE":       { bg: "#4ade8020", text: "#16a34a" },
  "FEASIBLE WITH TRAINING":     { bg: "#fbbf2420", text: "#d97706" },
  "REQUIRES WORKFORCE INVESTMENT": { bg: "#FF4B6E20", text: "#FF4B6E" }
}

export default function WorkforceTab() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWorkforceAlignment()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingState label="Workforce Data" />

  const summary = data.system_summary

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50" style={{ scrollbarWidth: "thin" }}>
      <div className="max-w-6xl mx-auto px-8 py-8 flex flex-col gap-8">

        {/* Header */}
        <div>
          <div className="text-[9px] font-black text-gray-400 uppercase tracking-[0.3em] mb-1">Human Capital Protocol</div>
          <h1 className="text-2xl font-black text-slate-800 tracking-tight">Workforce Alignment</h1>
          <p className="text-gray-500 text-sm mt-1">County-level surgical workforce analysis vs. WHO minimum staffing standards</p>
        </div>

        {/* Key Insight Banner */}
        <div className="bg-[#FF4B6E10] border border-[#FF4B6E30] rounded-2xl px-6 py-4 flex items-center gap-4">
          <div className="w-2 h-10 bg-[#FF4B6E] rounded-full flex-shrink-0" />
          <p className="text-sm font-bold text-slate-700">
            <span className="text-[#FF4B6E]">Critical insight: </span>
            {summary.key_insight}
          </p>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-4 gap-4">
          <StatCard label="Counties with No Anaesthetist" value={summary.counties_with_no_anaesthetist} sub="of 15 counties" accent="#FF4B6E" />
          <StatCard label="Counties with No Surgical Staff" value={summary.counties_with_no_surgical_staff} sub="of 15 counties" accent="#FF4B6E" />
          <StatCard label="Surgeons Needed for WHO Min" value={summary.total_additional_surgeons_needed_for_who_minimum} sub="additional required" accent="#F4A261" />
          <StatCard label="Years to Fill Gap" value={`${summary.years_to_fill_gap_at_current_training_rate}`} sub="at current training rate" accent="#a78bfa" />
        </div>

        {/* County Workforce Table */}
        <div>
          <div className="mb-4">
            <h2 className="text-base font-black text-slate-800 uppercase tracking-tight">County Workforce vs WHO Minimums</h2>
            <p className="text-gray-400 text-xs mt-0.5">WHO minimum: 4 surgeons, 4 anaesthetists, 4 obstetricians, 100 nurses per 100,000 population</p>
          </div>
          <div className="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-100">
                    <th className="px-5 py-3 text-left text-[9px] font-black text-gray-400 uppercase tracking-widest">County</th>
                    <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Pop.</th>
                    <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Surgeons</th>
                    <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Anaesthetists</th>
                    <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">OBs</th>
                    <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Nurses</th>
                    <th className="px-5 py-3 text-center text-[9px] font-black text-gray-400 uppercase tracking-widest">Gap Score</th>
                  </tr>
                </thead>
                <tbody>
                  {data.county_workforce.sort((a, b) => b.workforce_gap_score - a.workforce_gap_score).map((c, i) => {
                    const style = GAP_COLOR(c.workforce_gap_score)
                    return (
                      <tr key={i} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                        <td className="px-5 py-3 font-bold text-slate-800">{c.county}</td>
                        <td className="px-5 py-3 text-right text-gray-500 text-xs">{(c.population/1000).toFixed(0)}K</td>
                        <td className="px-5 py-3 text-right">
                          <MetricCell value={c.surgeons_per_100k} who={4} />
                        </td>
                        <td className="px-5 py-3 text-right">
                          <MetricCell value={c.anaesthetists_per_100k} who={4} highlight />
                        </td>
                        <td className="px-5 py-3 text-right">
                          <MetricCell value={c.obstetricians_per_100k} who={4} />
                        </td>
                        <td className="px-5 py-3 text-right">
                          <MetricCell value={c.nurses_per_100k} who={100} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <span className="text-[9px] font-black px-2.5 py-1 rounded-full uppercase tracking-widest" style={{ background: style.bg, color: style.text }}>
                            {style.label} {c.workforce_gap_score}
                          </span>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Priority Site Feasibility */}
        <div>
          <div className="mb-4">
            <h2 className="text-base font-black text-slate-800 uppercase tracking-tight">Priority Site Staffing Feasibility</h2>
          </div>
          <div className="grid grid-cols-3 gap-4">
            {data.priority_sites_alignment.map((site, i) => {
              const fs = FEASIBILITY_STYLE[site.feasibility] || {}
              return (
                <div key={i} className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm flex flex-col gap-4">
                  <div>
                    <div className="text-sm font-black text-slate-800 mb-1">{site.location}</div>
                    <div className="text-xs text-gray-400">{site.recommended_facility_type}</div>
                  </div>
                  <div className="inline-flex">
                    <span className="text-[9px] font-black px-3 py-1.5 rounded-full uppercase tracking-widest" style={{ background: fs.bg, color: fs.text }}>
                      {site.feasibility}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 leading-relaxed">{site.recommendation}</p>
                  <div className="text-xs text-gray-400 border-t border-gray-50 pt-3">
                    Operational in <span className="font-bold text-slate-700">{site.estimated_time_to_staff_months} months</span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Training Institutions */}
        <div>
          <div className="mb-4">
            <h2 className="text-base font-black text-slate-800 uppercase tracking-tight">Training Pipeline</h2>
          </div>
          <div className="grid grid-cols-3 gap-4">
            {data.training_institutions.map((inst, i) => (
              <div key={i} className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
                <div className="text-sm font-black text-slate-800 mb-1">{inst.name}</div>
                <div className="text-xs text-gray-400 mb-3">{inst.location}</div>
                <div className="text-xl font-black text-earth-blue mb-1">{inst.annual_surgical_graduates}</div>
                <div className="text-xs text-gray-400">graduates/year</div>
                <p className="text-xs text-gray-500 mt-3">{inst.note}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}

function MetricCell({ value, who, highlight }) {
  const pct = value / who
  const color = value === 0 ? "#FF4B6E" : pct < 0.25 ? "#F4A261" : pct < 0.5 ? "#fbbf24" : "#64748b"
  return (
    <span className="font-bold" style={{ color, fontWeight: highlight && value === 0 ? 900 : 600 }}>
      {value.toFixed(1)}
    </span>
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
