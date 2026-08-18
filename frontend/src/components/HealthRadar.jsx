import React from 'react';
import { Activity } from 'lucide-react';

export default function HealthRadar({ healthScore = 98.5, breakdown = {} }) {
  const completeness = breakdown.completeness ?? 100.0;
  const schema = breakdown.schema_validity ?? 100.0;
  const volumetric = breakdown.volumetric_consistency ?? 100.0;
  const historical = breakdown.historical_consistency ?? 100.0;
  const anomaly = breakdown.anomaly_score ?? 100.0;

  const metrics = [
    { label: 'Completeness (30%)', value: completeness, desc: 'Non-null required field slots' },
    { label: 'Schema Validity (20%)', value: schema, desc: 'Strict Pydantic type checks' },
    { label: 'Volumetric (20%)', value: volumetric, desc: 'Record count consistency' },
    { label: 'Historical Drift (15%)', value: historical, desc: 'Prior run entity overlap' },
    { label: 'Anomaly Sanity (15%)', value: anomaly, desc: 'Price distribution z-score bounds' },
  ];

  const isDegraded = healthScore < 70.0;

  return (
    <div className="card-3d p-6">
      <div className="flex items-center justify-between mb-5 pb-3 border-b border-[#111827]/10">
        <div className="flex items-center gap-2.5">
          <Activity className="w-5 h-5 text-[#059669]" />
          <h2 className="text-base font-bold font-heading text-[#111827]">Multi-Dimensional Health Scoring</h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-[#6B7280]">Composite:</span>
          <span className={`text-sm font-mono font-extrabold px-3 py-1 rounded-xl border ${
            isDegraded
              ? 'bg-[#FFE4E6] text-[#E11D48] border-[#FDA4AF]'
              : 'bg-[#D1FAE5] text-[#059669] border-[#6EE7B7]'
          }`}>
            {healthScore.toFixed(1)}%
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {metrics.map((m, idx) => (
          <div key={idx}>
            <div className="flex justify-between items-center text-xs font-mono mb-1.5">
              <span className="text-[#111827] font-bold">{m.label}</span>
              <span className="text-[#059669] font-extrabold">{m.value.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-[#EFECE6] h-2.5 rounded-full overflow-hidden border border-[#111827]/10">
              <div
                className={`h-full rounded-full transition-all duration-500 ${
                  m.value >= 80 ? 'bg-gradient-to-r from-[#059669] to-[#10B981]' :
                  m.value >= 50 ? 'bg-gradient-to-r from-[#D97706] to-[#F59E0B]' :
                  'bg-gradient-to-r from-[#E11D48] to-[#F43F5E]'
                }`}
                style={{ width: `${Math.max(5, m.value)}%` }}
              />
            </div>
            <p className="text-[11px] text-[#6B7280] font-sans mt-1">{m.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
