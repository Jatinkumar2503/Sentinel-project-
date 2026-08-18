import React from 'react';
import { Shield, Radio, Activity, Sparkles, Database, ArrowUpRight } from 'lucide-react';

export default function Header({ isWsConnected, onQuickTriggerDemo, isRunningDemo }) {
  return (
    <header className="card-3d p-5 mb-6 border border-[#111827]/10 flex flex-col xl:flex-row items-stretch xl:items-center justify-between gap-5 bg-white shadow-xs">
      {/* Brand & Editorial Title */}
      <div className="flex items-center gap-4">
        <div className="p-3 rounded-2xl bg-[#111827] text-white shadow-md flex items-center justify-center shrink-0" style={{ width: '48px', height: '48px' }}>
          <Shield size={26} style={{ width: '26px', height: '26px' }} />
        </div>
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-2xl font-extrabold tracking-tight font-heading text-[#111827]">
              SENTINEL AI
            </h1>
            <span className="text-[10px] font-mono font-bold uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-[#111827]/5 text-[#111827] border border-[#111827]/15">
              PROD v1.0
            </span>
          </div>
          <p className="text-xs text-[#4B5563] font-sans font-medium mt-0.5">
            Self-Healing Competitive Intelligence Platform • Powered by Bright Data Scraper Studio
          </p>
        </div>
      </div>

      {/* Telemetry Status Badges */}
      <div className="flex flex-wrap items-center gap-3 text-xs font-mono">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#FAF8F5] border border-[#111827]/10 text-[#111827] font-medium">
          <Database size={15} style={{ width: '15px', height: '15px' }} className="text-[#D97706] shrink-0" />
          <span className="text-[#6B7280]">Studio:</span>
          <span className="font-bold text-[#111827]">Bright Data Scraper Studio</span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#FAF8F5] border border-[#111827]/10 text-[#111827] font-medium">
          <Activity size={15} style={{ width: '15px', height: '15px' }} className="text-[#059669] shrink-0" />
          <span className="text-[#6B7280]">Health Gate:</span>
          <span className="font-bold text-[#059669]">4-Layer Active</span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#FAF8F5] border border-[#111827]/10 text-[#111827] font-medium">
          <Radio size={15} style={{ width: '15px', height: '15px' }} className={`shrink-0 ${isWsConnected ? 'text-[#059669] animate-pulse' : 'text-[#E11D48]'}`} />
          <span className="text-[#6B7280]">Stream:</span>
          <span className={`font-bold ${isWsConnected ? 'text-[#059669]' : 'text-[#E11D48]'}`}>
            {isWsConnected ? 'CONNECTED' : 'DISCONNECTED'}
          </span>
        </div>
      </div>

      {/* 3D Tactile CTA Button */}
      <div className="shrink-0">
        <button
          onClick={onQuickTriggerDemo}
          disabled={isRunningDemo}
          className="btn-3d w-full sm:w-auto px-5 py-2.5 rounded-xl bg-[#111827] hover:bg-black text-white text-xs font-bold font-sans tracking-wide flex items-center justify-center gap-2 transition-all cursor-pointer disabled:opacity-50"
        >
          <Sparkles size={16} style={{ width: '16px', height: '16px' }} className="text-[#F59E0B]" />
          <span>{isRunningDemo ? 'RUNNING SELF-HEALING LOOP...' : 'TRIGGER CHAOS DEMO LOOP'}</span>
          <ArrowUpRight size={16} style={{ width: '16px', height: '16px' }} className="text-white/70" />
        </button>
      </div>
    </header>
  );
}
