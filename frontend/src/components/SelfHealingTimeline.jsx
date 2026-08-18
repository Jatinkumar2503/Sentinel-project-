import React from 'react';
import { CheckCircle2, AlertTriangle, Cpu, ShieldCheck, Zap, ArrowRight, Activity, Terminal } from 'lucide-react';

export default function SelfHealingTimeline({ timelineEvents = [], isHealing, currentProgress = 0, latestHealingEvent }) {
  const defaultEvents = [
    {
      timestamp: '14:02:01',
      step: 'INITIATED',
      title: 'Collector Executed on Target Endpoint',
      detail: 'Executing Bright Data Scraper Studio collector with default baseline selector profile.',
      status: 'success'
    },
    {
      timestamp: '14:02:05',
      step: 'DOM_ANALYSIS',
      title: 'Target DOM Layout Mutation Detected',
      detail: 'Target website mutated CSS class names from .price to data-testid="price". Price selector failed.',
      status: 'warning'
    },
    {
      timestamp: '14:02:08',
      step: 'STRATEGY_GENERATED',
      title: 'Autonomous AST Selector Repair Synthesized',
      detail: 'Generated updated selector manifest: [data-testid="price"].',
      status: 'active'
    },
    {
      timestamp: '14:02:12',
      step: 'VALIDATION_GATE',
      title: '4-Tier Quality Validation Gate Inspection',
      detail: 'Validating 6 recovered records across Pydantic schema, statistical distribution & price bounds.',
      status: 'success'
    },
    {
      timestamp: '14:02:14',
      step: 'COMPLETED',
      title: 'Collector Restored & Promoted to Production',
      detail: 'Collector healed, validated and promoted to production with 99.2% Health Score.',
      status: 'success'
    }
  ];

  const eventsToDisplay = timelineEvents.length > 0 ? timelineEvents : defaultEvents;

  return (
    <div className="card-3d p-6 relative overflow-hidden">
      {/* Editorial Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 pb-4 border-b border-[#111827]/10">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-[#D97706]/10 text-[#D97706] border border-[#D97706]/20">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold font-heading text-[#111827] flex items-center gap-2">
              Autonomous Self-Healing Pipeline
              {isHealing && (
                <span className="px-2.5 py-0.5 text-[10px] font-mono font-bold bg-[#D97706] text-white rounded-full animate-pulse">
                  HEALING ({currentProgress}%)
                </span>
              )}
            </h2>
            <p className="text-xs text-[#4B5563] font-sans font-medium">
              Live telemetry: Failure Detection → AST Mutation Analysis → Sandbox → Validation → Production
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-[#6B7280]">Status:</span>
          <span className={`px-3 py-1 rounded-xl border font-bold ${
            isHealing 
              ? 'bg-[#FEF3C7] text-[#D97706] border-[#FCD34D]' 
              : 'bg-[#D1FAE5] text-[#059669] border-[#6EE7B7]'
          }`}>
            {isHealing ? 'REPAIRING DOM MUTATION' : 'AUTONOMOUS DEFENSE ACTIVE'}
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      {isHealing && (
        <div className="mb-6">
          <div className="flex justify-between text-xs font-mono font-bold text-[#111827] mb-1.5">
            <span>Executing Heuristic AST Selector Synthesis...</span>
            <span>{currentProgress}%</span>
          </div>
          <div className="w-full bg-[#EFECE6] h-2.5 rounded-full overflow-hidden border border-[#111827]/10">
            <div
              className="bg-gradient-to-r from-[#D97706] to-[#059669] h-full transition-all duration-300 rounded-full"
              style={{ width: `${currentProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Timeline Stream */}
      <div className="relative pl-6 space-y-5 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-[#111827]/15">
        {eventsToDisplay.map((event, idx) => {
          let badgeBg = 'bg-[#FAF8F5] border-[#111827]/10 text-[#111827]';
          let icon = <CheckCircle2 className="w-4 h-4 text-[#059669]" />;

          if (event.step === 'INITIATED' || event.step === 'DOM_ANALYSIS') {
            badgeBg = 'bg-[#FFFBEB] border-[#FCD34D] text-[#D97706]';
            icon = <AlertTriangle className="w-4 h-4 text-[#D97706]" />;
          } else if (event.step === 'STRATEGY_GENERATED' || event.step === 'SANDBOX_RUN') {
            badgeBg = 'bg-[#EEF2FF] border-[#C7D2FE] text-[#4F46E5]';
            icon = <Cpu className="w-4 h-4 text-[#4F46E5]" />;
          } else if (event.step === 'COMPLETED') {
            badgeBg = 'bg-[#ECFDF5] border-[#A7F3D0] text-[#059669]';
            icon = <ShieldCheck className="w-4 h-4 text-[#059669]" />;
          }

          return (
            <div key={idx} className="relative group">
              <div className="absolute -left-[27px] top-1.5 w-3.5 h-3.5 rounded-full bg-white border-2 border-[#111827] shadow-xs" />

              <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#111827]/10 hover:border-[#111827]/30 transition-all shadow-2xs">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    {icon}
                    <h3 className="text-sm font-bold text-[#111827]">{event.title}</h3>
                  </div>
                  <span className="font-mono text-xs text-[#6B7280] bg-white px-2.5 py-0.5 rounded-md border border-[#111827]/10 font-semibold">
                    {event.timestamp}
                  </span>
                </div>
                <p className="text-xs text-[#4B5563] font-mono leading-relaxed">{event.detail}</p>

                {event.extra?.repaired_selectors && (
                  <div className="mt-3 p-3 rounded-lg bg-white border border-[#4F46E5]/30 text-xs font-mono text-[#111827] flex items-center justify-between">
                    <span className="text-[#6B7280]">Repaired Price Selector:</span>
                    <code className="bg-[#EEF2FF] text-[#4F46E5] font-bold px-2 py-0.5 rounded border border-[#C7D2FE]">
                      {event.extra.repaired_selectors.price}
                    </code>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
