import React from 'react';
import { Code, Check, X } from 'lucide-react';

export default function DOMDiffViewer({ originalSelectors = {}, repairedSelectors = {}, isRepaired = true }) {
  const fields = [
    { label: 'Item Container', key: 'item_container', before: '.product-card', after: '[data-testid="product-item"]' },
    { label: 'Product Name', key: 'product_name', before: '.product-title', after: '[data-testid="product-title"]' },
    { label: 'Price Tag', key: 'price', before: '.price', after: '[data-testid="price"]' },
    { label: 'Currency', key: 'currency', before: '.currency', after: '[data-testid="currency"]' },
    { label: 'Stock Status', key: 'availability', before: '.stock-status', after: '[data-testid="stock"]' },
    { label: 'Product Link', key: 'product_url', before: '.product-link', after: '[data-testid="product-link"]' },
  ];

  return (
    <div className="card-3d p-6">
      <div className="flex items-center justify-between mb-5 pb-3 border-b border-[#111827]/10">
        <div className="flex items-center gap-2.5">
          <Code className="w-5 h-5 text-[#111827]" />
          <h2 className="text-base font-bold font-heading text-[#111827]">AST Selector Transformation & DOM Diff</h2>
        </div>
        <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-lg bg-[#FAF8F5] border border-[#111827]/10 text-[#111827]">
          Heuristic Mutation Resolver
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* BEFORE COLUMN */}
        <div className="p-4 rounded-xl bg-[#FFF1F2] border border-[#FECDD3]">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono font-bold uppercase text-[#E11D48] flex items-center gap-1.5">
              <X className="w-3.5 h-3.5" /> Broken Selectors (Before)
            </span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-white text-[#E11D48] border border-[#FECDD3]">
              0 Records Extracted
            </span>
          </div>

          <div className="space-y-2 text-xs font-mono">
            {fields.map((f) => (
              <div key={f.key} className="flex justify-between items-center py-1.5 px-2.5 rounded-lg bg-white border border-[#FECDD3]/50">
                <span className="text-[#6B7280]">{f.label}:</span>
                <code className="text-[#E11D48] font-bold line-through">{originalSelectors[f.key] || f.before}</code>
              </div>
            ))}
          </div>
        </div>

        {/* AFTER REPAIR COLUMN */}
        <div className="p-4 rounded-xl bg-[#ECFDF5] border border-[#A7F3D0]">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono font-bold uppercase text-[#059669] flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5" /> Repaired & Promoted (After)
            </span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-white text-[#059669] border border-[#A7F3D0]">
              6/6 Recovered (100%)
            </span>
          </div>

          <div className="space-y-2 text-xs font-mono">
            {fields.map((f) => (
              <div key={f.key} className="flex justify-between items-center py-1.5 px-2.5 rounded-lg bg-white border border-[#A7F3D0]/60">
                <span className="text-[#6B7280]">{f.label}:</span>
                <code className="text-[#059669] font-bold">{repairedSelectors[f.key] || f.after}</code>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
