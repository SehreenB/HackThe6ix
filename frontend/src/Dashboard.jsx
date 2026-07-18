import { useState } from "react"
import { Activity, Users, Percent, Hospital, Layers, Zap, FileText, ChevronDown } from "lucide-react"
import { runOptimizer } from "./api"
import { motion } from "motion/react"

export default function Dashboard({ stats, originalPct, updatedStats, onOptimizeComplete, onBriefOpen, facilityCount }) {
  const [n, setN] = useState(3)
  const [isOptimizing, setIsOptimizing] = useState(false)

  async function handleOptimize() {
    setIsOptimizing(true)
    try {
      const result = await runOptimizer(n)
      onOptimizeComplete(result)
    } catch {
      alert("Optimizer failed. Check that the backend is running.")
    }
    setIsOptimizing(false)
  }

  const displayStats = updatedStats || stats

  if (!stats) return (
    <div className="w-[360px] bg-white border border-gray-100 rounded-2xl p-12 shadow-2xl flex flex-col items-center justify-center gap-4">
      <div className="w-8 h-8 rounded-full border-2 border-earth-blue border-t-transparent animate-spin" />
      <div className="text-gray-400 font-black tracking-[0.3em] text-[10px] uppercase">Protocol Init</div>
    </div>
  )

  return (
    <div className="w-[360px] bg-white/95 backdrop-blur-2xl border border-gray-200/50 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.1)] overflow-hidden flex flex-col">
      
      {/* Tactical Header */}
      <div className="bg-gray-50/80 px-5 py-4 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-white border border-gray-100 rounded-lg flex items-center justify-center shadow-sm">
            <Activity size={16} className="text-earth-blue" />
          </div>
          <div>
            <div className="text-slate-800 font-black text-[10px] tracking-[0.1em] uppercase leading-none">Intelligence</div>
            <div className="text-gray-400 text-[8px] font-bold tracking-[0.2em] uppercase mt-1">LBR-MISSION-01</div>
          </div>
        </div>
        <div className="flex items-center gap-2 px-2.5 py-1 bg-white border border-gray-100 rounded-full">
          <span className="w-1.5 h-1.5 rounded-full bg-earth-green animate-pulse shadow-[0_0_8px_#4ade80]" />
          <span className="text-[8px] font-black text-gray-400 uppercase tracking-widest">Live</span>
        </div>
      </div>

      <div className="p-5 flex flex-col gap-6">
        
        {/* Coverage Monitor */}
        <div className="relative">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[9px] font-black text-gray-400 uppercase tracking-[0.25em]">National Coverage</span>
            <span className="text-[9px] font-black text-earth-blue bg-earth-blue/10 px-2 py-0.5 rounded uppercase tracking-widest">
              Base: 42.5%
            </span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-black text-slate-800 tracking-tighter">
              {displayStats?.pct_covered?.toFixed(1) || "42.5"}
            </span>
            <span className="text-sm font-black text-gray-400">%</span>
          </div>
          <div className="mt-4 h-1 w-full bg-gray-100 rounded-full overflow-hidden">
            <motion.div 
              initial={{ width: 0 }}
              animate={{ width: `${displayStats?.pct_covered || 42.5}%` }}
              className="h-full bg-earth-blue shadow-[0_0_10px_rgba(0,180,255,0.4)]"
            />
          </div>
        </div>

        {/* Tactical Divider */}
        <div className="h-px w-full bg-gradient-to-r from-transparent via-gray-100 to-transparent" />

        {/* Access Gap Monitor */}
        <div>
          <span className="text-[9px] font-black text-gray-400 uppercase tracking-[0.25em] mb-2 block">Population Gap</span>
          <div className="flex items-center justify-between">
            <div className="text-2xl font-black text-slate-800 tracking-tight">
              {displayStats?.beyond_2hr?.toLocaleString() || "2,841,176"}
            </div>
            <div className="flex flex-col items-end">
               <span className="text-[8px] font-bold text-gray-400 uppercase">Threshold</span>
               <span className="text-[9px] font-black text-slate-800 uppercase tracking-tighter">120 MIN</span>
            </div>
          </div>
        </div>

        {/* System Assets Row */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-50/50 border border-gray-100 rounded-xl p-3.5 flex items-center gap-3">
             <Hospital size={14} className="text-gray-400" />
             <div>
               <div className="text-[7px] font-black text-gray-400 uppercase tracking-[0.1em] mb-0.5">Surgical Sites</div>
               <div className="text-xs font-black text-slate-800">{facilityCount || 38}</div>
             </div>
          </div>
          <div className="bg-gray-50/50 border border-gray-100 rounded-xl p-3.5 flex items-center gap-3">
             <Layers size={14} className="text-gray-400" />
             <div>
               <div className="text-[7px] font-black text-gray-400 uppercase tracking-[0.1em] mb-0.5">Active Layers</div>
               <div className="text-xs font-black text-slate-800">14</div>
             </div>
          </div>
        </div>

        {/* Mission Strategy Panel */}
        <div className="mt-2 flex flex-col gap-3">
          <div className="flex items-center gap-2 mb-1">
            <Zap size={10} className="text-earth-blue" />
            <span className="text-[9px] font-black text-gray-400 uppercase tracking-[0.3em]">Strategy Analysis</span>
          </div>
          
          <div className="flex gap-2">
            <div className="relative flex-1 group">
              <select
                value={n}
                onChange={e => setN(Number(e.target.value))}
                className="w-full h-10 bg-gray-50 border border-gray-100 rounded-xl px-4 pr-10 text-[10px] font-black text-slate-800 uppercase appearance-none cursor-pointer focus:outline-none focus:border-earth-blue/30 transition-all hover:bg-white"
              >
                {[1, 2, 3, 5, 10].map(v => (
                  <option key={v} value={v}>{v} Strategic Assets</option>
                ))}
              </select>
              <ChevronDown size={12} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none group-hover:text-gray-600 transition-colors" />
            </div>

            <button
              onClick={handleOptimize}
              disabled={isOptimizing}
              className={`h-10 px-5 rounded-xl flex items-center justify-center gap-2 transition-all active:scale-95 shadow-sm font-black uppercase tracking-widest text-[9px] ${
                isOptimizing 
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                : 'bg-earth-blue text-white hover:bg-earth-blue/90 hover:shadow-lg hover:shadow-earth-blue/20'
              }`}
            >
              <Zap size={12} className={isOptimizing ? 'animate-pulse' : ''} />
              <span>{isOptimizing ? "Processing" : "Analyse"}</span>
            </button>
          </div>

          <button
            onClick={onBriefOpen}
            className="w-full h-11 bg-slate-800 text-white rounded-xl flex items-center justify-center gap-2.5 transition-all hover:bg-slate-700 active:scale-95 shadow-lg font-black uppercase tracking-[0.2em] text-[10px]"
          >
            <FileText size={14} className="text-earth-blue" />
            <span>Export Protocol Brief</span>
          </button>
        </div>

        {/* Technical Footer */}
        <div className="flex items-center justify-center gap-4 opacity-40">
           <span className="text-[7px] font-bold text-gray-400 uppercase tracking-widest">Liberia-OS-v1.4</span>
           <div className="w-1 h-1 rounded-full bg-gray-300" />
           <span className="text-[7px] font-bold text-gray-400 uppercase tracking-widest">Geospatial Secured</span>
        </div>
      </div>
    </div>
  )
}