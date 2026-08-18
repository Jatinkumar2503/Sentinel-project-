import React, { useState } from 'react';
import { Sparkles, RefreshCw, Layers, DollarSign } from 'lucide-react';

export default function ChaosLabPanel({ onSwitchVersion, onInjectPriceDrop, onResetDemo, activeVersion = 'v1' }) {
  const [injectedPrice, setInjectedPrice] = useState(129999);
  const [selectedProduct, setSelectedProduct] = useState('LP-001');

  return (
    <div className="card-3d p-6 border-2 border-[#111827]/10">
      <div className="flex items-center justify-between mb-5 pb-3 border-b border-[#111827]/10">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-[#4F46E5]/10 text-[#4F46E5] border border-[#4F46E5]/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold font-heading text-[#111827]">Chaos Lab & Synthetic Target Simulator</h2>
            <p className="text-xs text-[#4B5563] font-sans font-medium">
              Live website mutator for deterministic evaluation and proof of self-healing
            </p>
          </div>
        </div>

        <button
          onClick={onResetDemo}
          className="btn-3d px-3.5 py-2 rounded-xl bg-white hover:bg-[#FAF8F5] text-[#111827] border border-[#111827]/15 text-xs font-mono font-bold transition-all cursor-pointer flex items-center gap-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Reset Demo Lab
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Target Website DOM Switcher */}
        <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#111827]/10">
          <h3 className="text-xs font-mono font-bold uppercase text-[#111827] mb-2 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-[#D97706]" /> 1. Mutate Competitor Website DOM
          </h3>
          <p className="text-xs text-[#4B5563] font-sans font-medium mb-3">
            Change DOM hierarchy on target site to test scraper failure & immediate self-healing:
          </p>

          <div className="grid grid-cols-3 gap-2.5">
            <button
              onClick={() => onSwitchVersion('v1')}
              className={`p-3 rounded-xl border text-xs font-mono font-bold transition-all cursor-pointer ${
                activeVersion === 'v1'
                  ? 'bg-[#111827] text-white border-[#111827] shadow-md'
                  : 'bg-white text-[#111827] border-[#111827]/15 hover:border-[#111827]/40'
              }`}
            >
              <div>Version 1.0</div>
              <div className="text-[10px] opacity-80 mt-0.5">Baseline CSS</div>
            </button>

            <button
              onClick={() => onSwitchVersion('v2')}
              className={`p-3 rounded-xl border text-xs font-mono font-bold transition-all cursor-pointer ${
                activeVersion === 'v2'
                  ? 'bg-[#E11D48] text-white border-[#E11D48] shadow-md'
                  : 'bg-white text-[#E11D48] border-[#E11D48]/30 hover:border-[#E11D48]'
              }`}
            >
              <div>Version 2.0</div>
              <div className="text-[10px] opacity-80 mt-0.5">data-testid Break</div>
            </button>

            <button
              onClick={() => onSwitchVersion('v3')}
              className={`p-3 rounded-xl border text-xs font-mono font-bold transition-all cursor-pointer ${
                activeVersion === 'v3'
                  ? 'bg-[#4F46E5] text-white border-[#4F46E5] shadow-md'
                  : 'bg-white text-[#4F46E5] border-[#4F46E5]/30 hover:border-[#4F46E5]'
              }`}
            >
              <div>Version 3.0</div>
              <div className="text-[10px] opacity-80 mt-0.5">Microdata AST</div>
            </button>
          </div>
        </div>

        {/* Dynamic Competitive Price Injection */}
        <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#111827]/10">
          <h3 className="text-xs font-mono font-bold uppercase text-[#111827] mb-2 flex items-center gap-1.5">
            <DollarSign className="w-3.5 h-3.5 text-[#059669]" /> 2. Inject Real-Time Price Cut
          </h3>
          <p className="text-xs text-[#4B5563] font-sans font-medium mb-3">
            Trigger competitive price reduction to test Sentinel's automatic market intelligence alerts:
          </p>

          <div className="flex gap-2.5">
            <input
              type="number"
              value={injectedPrice}
              onChange={(e) => setInjectedPrice(Number(e.target.value))}
              className="flex-1 bg-white border border-[#111827]/20 rounded-xl px-3.5 py-2 text-xs font-mono font-bold text-[#111827] focus:outline-none focus:border-[#111827]"
              placeholder="e.g. 129999"
            />
            <button
              onClick={() => onInjectPriceDrop(selectedProduct, injectedPrice)}
              className="btn-3d px-4 py-2 rounded-xl bg-[#059669] hover:bg-[#047857] text-white text-xs font-mono font-bold transition-all cursor-pointer active:scale-95"
            >
              Inject Price Cut
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
