import React from 'react';
import { motion } from 'motion/react';
import { LayoutDashboard, Map as MapIcon, TrendingUp, Users, CloudRain, HelpCircle, LogOut } from 'lucide-react';

const Sidebar = ({ onTabChange, activeTab }) => {
  return (
    <aside className="w-64 bg-white border-r border-gray-100 flex flex-col py-10 z-[2000] relative">
      <div className="flex flex-col gap-3 px-6">
        <SidebarItem 
          icon={<LayoutDashboard size={20} />} 
          active={activeTab === 'missions'} 
          onClick={() => onTabChange('missions')} 
          label="Mission Map" 
        />
        <SidebarItem 
          icon={<TrendingUp size={20} />} 
          active={activeTab === 'investment'} 
          onClick={() => onTabChange('investment')} 
          label="Investment" 
        />
        <SidebarItem 
          icon={<Users size={20} />} 
          active={activeTab === 'workforce'} 
          onClick={() => onTabChange('workforce')} 
          label="Workforce" 
        />
        <SidebarItem 
          icon={<CloudRain size={20} />} 
          active={activeTab === 'seasonal'} 
          onClick={() => onTabChange('seasonal')} 
          label="Seasonal Access" 
        />
      </div>
      
      <div className="mt-auto flex flex-col gap-3 px-6">
        <SidebarItem 
          icon={<HelpCircle size={20} />} 
          onClick={() => {}} 
          label="Support" 
        />
        <SidebarItem 
          icon={<LogOut size={20} />} 
          onClick={() => window.location.reload()} 
          label="Sign Out" 
        />
      </div>
    </aside>
  );
};

const SidebarItem = ({ icon, active, onClick, label }) => (
  <button 
    onClick={onClick}
    className={`w-full p-4 rounded-2xl transition-all group relative flex items-center gap-4 ${
      active ? 'text-[#0057B8] bg-[#F4F7FB] font-bold shadow-sm' : 'text-[#7A808C] hover:bg-gray-50'
    }`}
  >
    <div className={`${active ? 'text-[#0057B8]' : 'text-[#A0AEC0] group-hover:text-[#7A808C]'}`}>
      {icon}
    </div>
    <span className="text-[12px] uppercase font-black tracking-[0.1em]">{label}</span>
    
    {active && (
      <motion.div 
        layoutId="sidebar-active-indicator"
        className="absolute left-0 w-1.5 h-8 bg-[#0057B8] rounded-r-full"
        initial={{ opacity: 0, x: -5 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.2 }}
      />
    )}
  </button>
);

export default Sidebar;
