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
      desc: 'When competitor websites redesign or change class names (e.g. .price fails), extraction health drops.',
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
      desc: 'Validated records trigger real-time price drop, discount surge, and inventory stockout business alerts.',
      icon: TrendingDown,
      color: 'bg-[#D1FAE5] text-[#059669] border-[#6EE7B7]',
    },
  ];

  return (
    <div className="card-porcelain p-8 mb-10 bg-white border border-[#111827]/10 w-full shadow-md">
      {/* Header Banner Title */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 mb-6 border-b border-[#111827]/10">
        <div>
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#111827] text-white text-[11px] font-mono font-bold uppercase tracking-widest mb-2">
            <span>HOW SENTINEL AI WORKS</span>
          </div>
          <h2 className="text-2xl font-extrabold font-heading text-[#111827] tracking-tight">
            The Autonomous Self-Healing Pipeline
          </h2>
        </div>
        <p className="text-sm text-[#4B5563] font-sans font-medium max-w-xl leading-relaxed">
          Traditional scrapers silently fail when website layouts change. Sentinel AI monitors extraction health, repairs broken CSS/XPath selectors automatically using Bright Data, and delivers uninterrupted competitive market intelligence.
        </p>
      </div>

      {/* 4 Interactive Flow Steps */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
        {steps.map((step, idx) => {
          const IconComponent = step.icon;
          return (
            <div key={idx} className="relative p-6 rounded-2xl bg-[#FAF8F5] border border-[#111827]/10 flex flex-col justify-between hover:border-[#111827]/30 hover:bg-white transition-all shadow-2xs">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-mono font-extrabold text-[#9CA3AF] tracking-wider">{step.num}</span>
                  <div className={`p-3 rounded-xl border flex items-center justify-center shrink-0 ${step.color}`} style={{ width: '42px', height: '42px' }}>
                    <IconComponent size={20} style={{ width: '20px', height: '20px' }} />
                  </div>
                </div>
                <h3 className="text-base font-bold font-sans text-[#111827] mb-2">{step.title}</h3>
                <p className="text-xs text-[#4B5563] font-sans font-medium leading-relaxed">{step.desc}</p>
              </div>

              {idx < steps.length - 1 && (
                <div className="hidden xl:block absolute -right-3.5 top-1/2 -translate-y-1/2 z-10 p-1.5 rounded-full bg-white border border-[#111827]/15 text-[#6B7280] shadow-sm">
                  <ArrowRight size={14} style={{ width: '14px', height: '14px' }} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
