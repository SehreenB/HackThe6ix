import { useState, useEffect } from "react"
import { fetchSeasonalAccess } from "../api"

const SEVERITY_STYLE = {
  "CRITICAL": { bg: "#FF4B6E20", text: "#FF4B6E", bar: "#FF4B6E" },
  "SEVERE":   { bg: "#F4A26120", text: "#F4A261", bar: "#F4A261" },
  "MODERATE": { bg: "#fbbf2420", text: "#d97706", bar: "#fbbf24" },
  "LOW":      { bg: "#4ade8020", text: "#16a34a", bar: "#4ade80" }
}

export default function SeasonalTab() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSeasonalAccess()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingState label="Seasonal Access Data" />

  const nat = data.national_summary

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50" style={{ scrollbarWidth: "thin" }}>
      <div className="max-w-6xl mx-auto px-8 py-8 flex flex-col gap-8">

        {/* Header */}
        <div>
          <div className="text-[9px] font-black text-gray-400 uppercase tracking-[0.3em] mb-1">Temporal Access Protocol</div>
          <h1 className="text-2xl font-black text-slate-800 tracking-tight">Seasonal Access Analysis</h1>
          <p className="text-gray-500 text-sm mt-1">Road viability and surgical access variability across dry and rainy seasons</p>
        </div>

        {/* National Summary Cards */}
        <div className="grid grid-cols-4 gap-4">
          <StatCard label="Dry Season Coverage" value={`${nat.dry_season_coverage_pct}%`} sub="Nov–Apr baseline" accent="#00E5FF" />
          <StatCard label="Rainy Season Coverage" value={`${nat.rainy_season_coverage_pct}%`} sub="May–Oct degraded" accent="#F4A261" />
          <StatCard label="Seasonal Loss" value={`${nat.seasonal_coverage_loss_pct}%`} sub="coverage drop" accent="#FF4B6E" />
          <StatCard label="People Losing Access" value="793K" sub="in rainy season" accent="#FF4B6E" />
        </div>

        {/* Season Banner */}
        <div className="bg-[#FF4B6E10] border border-[#FF4B6E30] rounded-2xl px-6 py-4 flex items-center gap-4">
          <div className="w-2 h-10 bg-[#FF4B6E] rounded-full flex-shrink-0" />
          <p className="text-sm font-bold text-slate-700">
            <span className="text-[#FF4B6E]">793,000 people</span> lose surgical access entirely in the rainy season — primarily in Lofa, Grand Gedeh, River Cess, Gbarpolu, and Grand Cape Mount counties.
          </p>
        </div>

        {/* County Seasonal Table */}
        <div>
          <div className="mb-4">
            <h2 className="text-base font-black text-slate-800 uppercase tracking-tight">County Seasonal Coverage</h2>
            <p className="text-gray-400 text-xs mt-0.5">% of county population within 2-hour surgical access by season</p>
          </div>
          <div className="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="px-5 py-3 text-left text-[9px] font-black text-gray-400 uppercase tracking-widest">County</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Dry Season</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Rainy Season</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Change</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">+Travel Time</th>
                  <th className="px-5 py-3 text-right text-[9px] font-black text-gray-400 uppercase tracking-widest">Cut Off</th>
                  <th className="px-5 py-3 text-center text-[9px] font-black text-gray-400 uppercase tracking-widest">Severity</th>
                </tr>
              </thead>
              <tbody>
                {data.county_seasonal_data
                  .sort((a, b) => a.seasonal_change_pct - b.seasonal_change_pct)
                  .map((c, i) => {
                  const style = SEVERITY_STYLE[c.severity] || {}
                  return (
                    <tr key={i} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                      <td className="px-5 py-3 font-bold text-slate-800">{c.county}</td>
                      <td className="px-5 py-3 text-right font-bold text-slate-700">{c.dry_season_pct_within_2hr}%</td>
                      <td className="px-5 py-3 text-right">
                        <span className="font-bold" style={{ color: style.text || "#64748b" }}>
                          {c.rainy_season_pct_within_2hr}%
                        </span>
                      </td>
                      <td className="px-5 py-3 text-right">
                        <span className="font-bold text-[#FF4B6E]">{c.seasonal_change_pct}%</span>
                      </td>
                      <td className="px-5 py-3 text-right text-gray-500">+{c.avg_travel_time_increase_min} min</td>
                      <td className="px-5 py-3 text-right text-gray-500">{c.communities_cut_off_rainy_season}</td>
                      <td className="px-5 py-3 text-center">
                        <span className="text-[9px] font-black px-2.5 py-1 rounded-full uppercase tracking-widest" style={{ background: style.bg, color: style.text }}>
                          {c.severity}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Visual comparison bars */}
        <div>
          <div className="mb-4">
            <h2 className="text-base font-black text-slate-800 uppercase tracking-tight">Seasonal Coverage Gap by County</h2>
          </div>
          <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col gap-4">
            {data.county_seasonal_data
              .sort((a, b) => a.seasonal_change_pct - b.seasonal_change_pct)
              .slice(0, 10)
              .map((c, i) => {
              const style = SEVERITY_STYLE[c.severity] || {}
              return (
                <div key={i} className="flex items-center gap-4">
                  <div className="w-28 text-xs font-bold text-slate-700 text-right flex-shrink-0">{c.county}</div>
                  <div className="flex-1 flex items-center gap-2">
                    <div className="h-6 rounded-md bg-[#00E5FF20] flex items-center" style={{ width: `${c.dry_season_pct_within_2hr}%` }}>
                      <span className="text-[8px] font-black text-[#00E5FF] px-2">{c.dry_season_pct_within_2hr}%</span>
                    </div>
                    <div className="h-6 rounded-md" style={{ width: `${Math.abs(c.seasonal_change_pct)}%`, background: style.bg, borderLeft: `2px solid ${style.bar}` }}>
                      <span className="text-[8px] font-black px-2 leading-6 inline-block" style={{ color: style.text }}>{c.seasonal_change_pct}%</span>
                    </div>
                  </div>
                </div>
              )
            })}
            <div className="flex items-center gap-4 pt-2 border-t border-gray-50">
              <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-sm bg-[#00E5FF20] border border-[#00E5FF40]" /><span className="text-[9px] text-gray-400">Dry Season</span></div>
              <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-sm bg-[#FF4B6E20] border border-[#FF4B6E40]" /><span className="text-[9px] text-gray-400">Rainy Season Loss</span></div>
            </div>
          </div>
        </div>

        {/* Facility Siting Implications */}
        <div>
          <div className="mb-4">
            <h2 className="text-base font-black text-slate-800 uppercase tracking-tight">Facility Siting Implications</h2>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {data.facility_siting_implications.map((imp, i) => (
              <div key={i} className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
                <div className="text-sm font-black text-slate-800 mb-2">{imp.recommendation}</div>
                <p className="text-xs text-gray-500 leading-relaxed">{imp.detail}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
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
