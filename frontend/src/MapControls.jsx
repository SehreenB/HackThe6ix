import React from 'react';
import { Plus, Minus } from 'lucide-react';

export const ZoomControls = ({ map }) => {
  const handleZoom = (delta) => {
    if (!map) return;
    map.setZoom(map.getZoom() + delta);
  };

  return (
    <div className="absolute bottom-10 right-10 z-[2000] flex flex-col gap-2">
      <button 
        onClick={() => handleZoom(1)}
        className="w-12 h-12 bg-white/95 backdrop-blur-xl border border-gray-200 rounded-xl shadow-2xl flex items-center justify-center text-gray-600 hover:text-earth-blue transition-all active:scale-95"
      >
        <Plus size={20} />
      </button>
      <button 
        onClick={() => handleZoom(-1)}
        className="w-12 h-12 bg-white/95 backdrop-blur-xl border border-gray-200 rounded-xl shadow-2xl flex items-center justify-center text-gray-600 hover:text-earth-blue transition-all active:scale-95"
      >
        <Minus size={20} />
      </button>
    </div>
  );
};

export const MapLegend = () => {
  return (
    <div className="absolute bottom-4 left-10 z-[2000] bg-white/95 backdrop-blur-2xl border border-gray-200/50 rounded-full shadow-[0_10px_40px_rgba(0,0,0,0.1)] py-2 px-6 flex items-center gap-6">
      
      {/* Protocol Items */}
      <div className="flex items-center gap-4">
        <LegendItem color="#FF4B6E" label="Bellwether" />
        <LegendItem color="#00E5FF" label="Basic" />
        <LegendItem color="#F4A261" label="Recommended" />
      </div>

      {/* Thin Vertical Tac-Divider */}
      <div className="h-4 w-px bg-gray-200 mx-1" />

      {/* Threshold Items */}
      <div className="flex items-center gap-4">
        <SpectrumItem color="#23a152" label="<30m" />
        <SpectrumItem color="#efd81d" label="60m" />
        <SpectrumItem color="#f39c12" label="120m" />
        <SpectrumItem color="#e74c3c" label=">120m" />
      </div>
    </div>
  );
};

const LegendItem = ({ color, label }) => (
  <div className="flex items-center gap-2">
    <div className="w-2.5 h-2.5 rounded-full border border-white shadow-sm" style={{ background: color }} />
    <span className="text-[9px] font-black text-slate-700 uppercase tracking-tight">{label}</span>
  </div>
);

const SpectrumItem = ({ color, label }) => (
  <div className="flex items-center gap-2">
    <div className="w-2.5 h-2.5 rounded-sm border border-white/50 shadow-sm" style={{ background: color }} />
    <span className="text-[9px] font-bold text-slate-500 tracking-tighter">{label}</span>
  </div>
);
