import React from 'react';
import { Database, AlertTriangle, Zap, TrendingDown, ArrowRight } from 'lucide-react';

export default function HeroExplanation() {
  const steps = [
    {
      num: '01',
      title: 'Scrape Public Web Data',
      desc: 'Custom Bright Data Scraper Studio collectors continuously extract competitor pricing & stock catalogs.',
      icon: Database,
      color: 'bg-[#FEF3C7] text-[#D97706] border-[#FCD34D]',
    },
    {
      num: '02',
      title: 'Detect Selector Failure',
      desc: 'When competitor websites redesign or change class names (e.g. .price fails), Health score drops.',
      icon: AlertTriangle,
      color: 'bg-[#FFE4E6] text-[#E11D48] border-[#FDA4AF]',
    },
    {
      num: '03',
      title: 'Autonomous Self-Healing',
      desc: 'AST heuristic engine inspects DOM, repairs broken selectors ([data-testid="price"]), and validates in sandbox.',
      icon: Zap,
      color: 'bg-[#EEF2FF] text-[#4F46E5] border-[#C7D2FE]',
    },
    {
      num: '04',
      title: 'Deliver Price Intel',
      desc: 'Validated records trigger real-time price drop, discount spike, and inventory stockout business alerts.',
      icon: TrendingDown,
      color: 'bg-[#D1FAE5] text-[#059669] border-[#6EE7B7]',
    },
  ];

  return (
    <div className="card-porcelain p-6 mb-8 bg-gradient-to-r from-white via-[#FAF8F5] to-white border border-[#111827]/10">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-4 border-b border-[#111827]/10">
        <div>
          <span className="text-[10px] font-mono font-extrabold uppercase tracking-widest px-3 py-1 rounded-full bg-[#111827] text-white">
            HOW SENTINEL AI WORKS
          </span>
          <h2 className="text-xl font-extrabold font-heading text-[#111827] mt-2">
            The Autonomous Self-Healing Pipeline Explained
          </h2>
        </div>
        <p className="text-xs text-[#4B5563] font-sans font-medium max-w-md">
          Traditional scrapers silently fail when website layouts change. Sentinel AI monitors extraction health, repairs selectors automatically using Bright Data, and delivers uninterrupted competitive intel.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {steps.map((step, idx) => {
          const IconComponent = step.icon;
          return (
            <div key={idx} className="relative p-5 rounded-2xl bg-white border border-[#111827]/10 flex flex-col justify-between shadow-xs hover:border-[#111827]/30 transition-all">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-mono font-extrabold text-[#9CA3AF]">{step.num}</span>
                  <div className={`p-2.5 rounded-xl border flex items-center justify-center ${step.color}`} style={{ width: '38px', height: '38px' }}>
                    <IconComponent size={18} style={{ width: '18px', height: '18px' }} />
                  </div>
                </div>
                <h3 className="text-sm font-bold font-sans text-[#111827] mb-1">{step.title}</h3>
                <p className="text-xs text-[#4B5563] font-sans font-medium leading-relaxed">{step.desc}</p>
              </div>

              {idx < steps.length - 1 && (
                <div className="hidden lg:block absolute -right-4 top-1/2 -translate-y-1/2 z-10 p-1 rounded-full bg-white border border-[#111827]/15 text-[#6B7280] shadow-xs">
                  <ArrowRight size={12} style={{ width: '12px', height: '12px' }} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
