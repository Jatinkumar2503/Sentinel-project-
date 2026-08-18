import React from 'react';
import { Play, Zap, Database } from 'lucide-react';

export default function CompetitorMatrix({ scrapers = [], onRunScraper, onHealScraper, runningScraperId }) {
  return (
    <div className="card-3d p-6">
      <div className="flex items-center justify-between mb-5 pb-3 border-b border-[#111827]/10">
        <div>
          <h2 className="text-base font-bold font-heading text-[#111827]">Competitors & Scraper Studio Fleet</h2>
          <p className="text-xs text-[#4B5563] font-sans font-medium mt-0.5">
            Active custom collectors running on public competitor targets
          </p>
        </div>
        <span className="text-xs font-mono font-bold px-3 py-1 rounded-xl bg-[#FAF8F5] border border-[#111827]/10 text-[#111827]">
          {scrapers.length} Active Scrapers
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-sans">
          <thead>
            <tr className="border-b border-[#111827]/10 text-[#6B7280] font-mono uppercase text-[11px] tracking-wider">
              <th className="pb-3 px-3">Collector Name</th>
              <th className="pb-3 px-3">Target Endpoint</th>
              <th className="pb-3 px-3">Studio Collector ID</th>
              <th className="pb-3 px-3 text-center">Health Score</th>
              <th className="pb-3 px-3 text-center">Status</th>
              <th className="pb-3 px-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#111827]/10">
            {scrapers.map((s) => {
              const isRunning = runningScraperId === s.id;
              const isDegraded = s.health_score < 70.0;

              return (
                <tr key={s.id} className="hover:bg-[#FAF8F5] transition-colors">
                  <td className="py-4 px-3 font-bold text-[#111827]">
                    {s.name}
                  </td>
                  <td className="py-4 px-3 text-[#4B5563] font-mono truncate max-w-[200px]">
                    {s.target_url}
                  </td>
                  <td className="py-4 px-3 font-mono font-bold text-[#4F46E5]">
                    {s.bright_data_scraper_id}
                  </td>
                  <td className="py-4 px-3 text-center">
                    <span className={`px-2.5 py-1 rounded-xl font-mono font-bold border ${
                      isDegraded 
                        ? 'bg-[#FFE4E6] text-[#E11D48] border-[#FDA4AF]' 
                        : 'bg-[#D1FAE5] text-[#059669] border-[#6EE7B7]'
                    }`}>
                      {s.health_score.toFixed(1)}%
                    </span>
                  </td>
                  <td className="py-4 px-3 text-center">
                    <span className="px-2.5 py-1 rounded-xl bg-[#FAF8F5] border border-[#111827]/10 text-[#111827] font-mono font-bold">
                      {s.status}
                    </span>
                  </td>
                  <td className="py-4 px-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => onRunScraper(s.id)}
                        disabled={isRunning}
                        className="btn-3d px-3 py-1.5 rounded-xl bg-[#111827] hover:bg-black text-white text-xs font-mono transition-all cursor-pointer disabled:opacity-50 flex items-center gap-1.5"
                      >
                        <Play className={`w-3.5 h-3.5 ${isRunning ? 'animate-spin' : ''}`} />
                        {isRunning ? 'Running...' : 'Run'}
                      </button>

                      <button
                        onClick={() => onHealScraper(s.id)}
                        className="btn-3d px-3 py-1.5 rounded-xl bg-[#D97706] hover:bg-[#B45309] text-white text-xs font-mono transition-all cursor-pointer flex items-center gap-1.5"
                      >
                        <Zap className="w-3.5 h-3.5" />
                        Heal
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
