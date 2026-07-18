import React from 'react';
import { motion } from 'motion/react';
import { Globe, Shield, BarChart3, Info, Settings, Search, Menu, MapPin, Activity } from 'lucide-react';
import Logo from './Logo';

const Navbar = ({ onTabChange, activeTab, searchableData = [], onSearchSelect }) => {
  const [query, setQuery] = React.useState('');
  const [results, setResults] = React.useState([]);
  const [isOpen, setIsOpen] = React.useState(false);

  const handleSearch = (e) => {
    const val = e.target.value;
    setQuery(val);
    
    if (val.length > 1) {
      const filtered = searchableData.filter(item => 
        item.name.toLowerCase().includes(val.toLowerCase()) ||
        (item.county && item.county.toLowerCase().includes(val.toLowerCase()))
      ).slice(0, 6);
      setResults(filtered);
      setIsOpen(true);
    } else {
      setResults([]);
      setIsOpen(false);
    }
  };

  const handleSelect = (item) => {
    onSearchSelect(item);
    setQuery(item.name);
    setIsOpen(false);
  };

  return (
    <header className="h-16 border-b border-gray-100 bg-white flex items-center justify-between px-8 z-[3000] sticky top-0 font-['Inter']">
      <div className="flex items-center gap-12">
        <div className="cursor-pointer hover:opacity-80 transition-opacity relative w-48 h-16" onClick={() => onTabChange('missions')}>
          <div className="absolute top-1/2 -translate-y-1/2 left-0 pointer-events-none">
            <Logo size={130} />
          </div>
        </div>
        
        <nav className="hidden lg:flex items-center gap-10">
          <NavLink label="Mission Map" active={activeTab === 'missions'} onClick={() => onTabChange('missions')} />
          <NavLink label="Investment" active={activeTab === 'investment'} onClick={() => onTabChange('investment')} />
          <NavLink label="Workforce" active={activeTab === 'workforce'} onClick={() => onTabChange('workforce')} />
          <NavLink label="Seasonal Access" active={activeTab === 'seasonal'} onClick={() => onTabChange('seasonal')} />
        </nav>
      </div>

      <div className="flex-1 max-w-lg mx-12 hidden md:block">
        <div className="relative group">
          <Search size={14} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-earth-blue transition-colors" />
          <input 
            type="text" 
            value={query}
            onChange={handleSearch}
            onFocus={() => query.length > 1 && setIsOpen(true)}
            placeholder="Search geospatial data..." 
            className="w-full bg-gray-50 border border-gray-100 rounded-xl py-2 pl-12 pr-6 text-xs text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-earth-blue/30 focus:bg-white transition-all"
          />

          {/* Search Results Dropdown */}
          {isOpen && results.length > 0 && (
            <div className="absolute top-full left-0 w-full mt-2 bg-white border border-gray-100 rounded-xl shadow-2xl overflow-hidden z-[4000] animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="p-2 border-b border-gray-50 bg-gray-50/50">
                <span className="text-[9px] uppercase tracking-[0.2em] font-black text-gray-400 px-3">Geospatial Matches</span>
              </div>
              {results.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelect(item)}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-0 text-left group"
                >
                  <div className={`p-1.5 rounded-lg ${item.type === 'County' ? 'bg-earth-blue/10 text-earth-blue' : 'bg-earth-green/10 text-earth-green'}`}>
                    {item.type === 'County' ? <Globe size={12} /> : <Activity size={12} />}
                  </div>
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-gray-900 group-hover:text-earth-blue transition-colors">{item.name}</span>
                    <span className="text-[10px] text-gray-400">{item.type || 'Location'}{item.county ? ` • ${item.county}` : ''}</span>
                  </div>
                  <div className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity">
                    <MapPin size={12} className="text-earth-blue" />
                  </div>
                </button>
              ))}
            </div>
          )}

          {isOpen && results.length === 0 && query.length > 1 && (
            <div className="absolute top-full left-0 w-full mt-2 bg-white border border-gray-100 rounded-xl shadow-2xl p-4 text-center z-[4000]">
              <span className="text-xs text-gray-400">No geospatial identifiers found</span>
            </div>
          )}
        </div>
      </div>

      <div className="flex items-center gap-8">
        <div className="hidden sm:flex flex-col items-end">
          <span className="text-[9px] text-gray-400 uppercase tracking-[0.2em] font-bold">System Status</span>
          <span className="text-[9px] text-earth-green font-black uppercase tracking-[0.2em] flex items-center gap-1.5">
            <span className="w-1 h-1 rounded-full bg-earth-green shadow-[0_0_8px_#4ade80]"></span>
            Nominal
          </span>
        </div>
        <button className="p-2 hover:bg-gray-100 rounded-xl transition-colors text-gray-400 hover:text-gray-900">
          <Settings size={18} />
        </button>
      </div>
    </header>
  );
};

const NavLink = ({ label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`text-[10px] font-black uppercase tracking-[0.3em] transition-all hover:text-earth-blue relative py-2 ${active ? 'text-gray-900' : 'text-gray-400'}`}
  >
    {label}
    {active && (
      <motion.span 
        layoutId="nav-active"
        className="absolute bottom-0 left-0 w-full h-[3px] bg-earth-blue rounded-full shadow-[0_4px_12px_rgba(0,180,255,0.4)]"
      ></motion.span>
    )}
  </button>
);

export default Navbar;
