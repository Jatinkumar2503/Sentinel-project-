import React from 'react';
import { Cpu, Activity, ShieldCheck, Bell } from 'lucide-react';

export default function MetricCard({ title, value, subtitle, iconType = 'cpu', color = 'dark', trend }) {
  const colorVariants = {
    dark: 'bg-[#111827] text-white border-[#111827]',
    amber: 'bg-[#FEF3C7] text-[#D97706] border-[#FCD34D]',
    emerald: 'bg-[#D1FAE5] text-[#059669] border-[#6EE7B7]',
    indigo: 'bg-[#E0E7FF] text-[#4F46E5] border-[#A5B4FC]',
    rose: 'bg-[#FFE4E6] text-[#E11D48] border-[#FDA4AF]'
  };

  const badgeVariants = {
    dark: 'bg-[#111827]/10 text-[#111827]',
    amber: 'bg-[#D97706]/10 text-[#D97706]',
    emerald: 'bg-[#059669]/10 text-[#059669]',
    indigo: 'bg-[#4F46E5]/10 text-[#4F46E5]',
  };

  const renderIcon = () => {
    switch (iconType) {
      case 'cpu':
        return <Cpu size={18} style={{ width: '18px', height: '18px' }} />;
      case 'activity':
        return <Activity size={18} style={{ width: '18px', height: '18px' }} />;
      case 'shield':
        return <ShieldCheck size={18} style={{ width: '18px', height: '18px' }} />;
      case 'bell':
        return <Bell size={18} style={{ width: '18px', height: '18px' }} />;
      default:
        return <Activity size={18} style={{ width: '18px', height: '18px' }} />;
    }
  };

  return (
    <div className="card-porcelain p-6 bg-white border border-[#111827]/10 flex flex-col justify-between h-full min-h-[140px]">
      <div className="flex items-start justify-between gap-3 mb-3">
        <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-[#6B7280] block leading-tight">{title}</span>
        <div className={`p-2.5 rounded-xl border flex items-center justify-center shrink-0 ${colorVariants[color] || colorVariants.dark}`} style={{ width: '38px', height: '38px' }}>
          {renderIcon()}
        </div>
      </div>

      <div>
        <div className="flex items-baseline gap-2 flex-wrap">
          <span className="text-2xl font-extrabold text-[#111827] font-mono tracking-tight">{value}</span>
          {trend && (
            <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full border whitespace-nowrap ${badgeVariants[color] || badgeVariants.dark}`}>
              {trend}
            </span>
          )}
        </div>
        {subtitle && <p className="text-xs font-sans text-[#4B5563] font-medium mt-1.5 leading-snug">{subtitle}</p>}
      </div>
    </div>
  );
}
