import React from 'react';
import { TrendingDown, TrendingUp, AlertOctagon, PackageCheck, Flame, BellRing } from 'lucide-react';

export default function IntelligenceFeed({ events = [] }) {
  const getEventIcon = (type) => {
    if (type === 'PRICE_DROP') return <TrendingDown className="w-4 h-4 text-[#E11D48]" />;
    if (type === 'PRICE_INCREASE') return <TrendingUp className="w-4 h-4 text-[#059669]" />;
    if (type === 'OUT_OF_STOCK') return <AlertOctagon className="w-4 h-4 text-[#D97706]" />;
    if (type === 'NEW_PRODUCT') return <Flame className="w-4 h-4 text-[#4F46E5]" />;
    return <PackageCheck className="w-4 h-4 text-[#111827]" />;
  };

  const getSeverityBadge = (severity) => {
    if (severity === 'CRITICAL') {
      return 'bg-[#FFE4E6] text-[#E11D48] border-[#FDA4AF]';
    }
    if (severity === 'WARNING') {
      return 'bg-[#FEF3C7] text-[#D97706] border-[#FCD34D]';
    }
    return 'bg-[#E0E7FF] text-[#4F46E5] border-[#A5B4FC]';
  };

  return (
    <div className="card-3d p-6">
      <div className="flex items-center justify-between mb-5 pb-3 border-b border-[#111827]/10">
        <div className="flex items-center gap-2.5">
          <BellRing className="w-5 h-5 text-[#111827]" />
          <h2 className="text-base font-bold font-heading text-[#111827]">Live Competitive Delta Intelligence</h2>
        </div>
        <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-lg bg-[#FAF8F5] border border-[#111827]/10 text-[#111827]">
          {events.length} Actionable Events
        </span>
      </div>

      <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
        {events.length === 0 ? (
          <div className="text-center py-10 text-[#6B7280] font-sans text-xs">
            No competitive alerts detected yet. Run collectors or inject chaos to observe.
          </div>
        ) : (
          events.map((ev) => (
            <div
              key={ev.id || Math.random()}
              className="p-4 rounded-xl bg-[#FAF8F5] border border-[#111827]/10 hover:border-[#111827]/30 transition-all shadow-2xs group"
            >
              <div className="flex items-start justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-xl bg-white border border-[#111827]/10 shadow-2xs">
                    {getEventIcon(ev.event_type)}
                  </div>
                  <h4 className="text-xs font-bold text-[#111827] group-hover:text-[#4F46E5] transition-colors">
                    {ev.title}
                  </h4>
                </div>
                <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full border ${getSeverityBadge(ev.severity)}`}>
                  {ev.severity}
                </span>
              </div>
              <p className="text-xs text-[#4B5563] font-sans leading-relaxed pl-9 font-medium">
                {ev.description}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
