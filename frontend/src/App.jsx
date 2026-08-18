import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HeroExplanation from './components/HeroExplanation';
import MetricCard from './components/MetricCard';
import SelfHealingTimeline from './components/SelfHealingTimeline';
import DOMDiffViewer from './components/DOMDiffViewer';
import HealthRadar from './components/HealthRadar';
import IntelligenceFeed from './components/IntelligenceFeed';
import CompetitorMatrix from './components/CompetitorMatrix';
import ChaosLabPanel from './components/ChaosLabPanel';

import {
  fetchDashboardSummary,
  fetchScrapers,
  fetchCompetitors,
  fetchIntelligenceEvents,
  fetchHealingEvents,
  fetchScraperHealth,
  triggerScraperRun,
  triggerManualHealing,
  mutateDemoPrice,
  resetDemoLab
} from './services/api';
import { WebSocketService } from './services/websocket';
import { ShieldCheck, Activity, Cpu, Bell, Layers, Sparkles } from 'lucide-react';

export default function App() {
  const [summary, setSummary] = useState({
    total_competitors: 2,
    total_scrapers: 2,
    healthy_scrapers: 2,
    degraded_scrapers: 0,
    healing_scrapers: 0,
    total_products_monitored: 6,
    recent_intelligence_events: 5,
    total_repairs_executed: 7,
    healing_success_rate: 100.0,
    average_health_score: 98.2,
  });

  const [scrapers, setScrapers] = useState([]);
  const [intelligenceEvents, setIntelligenceEvents] = useState([]);
  const [healingEvents, setHealingEvents] = useState([]);
  const [healthData, setHealthData] = useState({
    health_score: 98.5,
    breakdown: {
      completeness: 100.0,
      schema_validity: 100.0,
      volumetric_consistency: 100.0,
      historical_consistency: 100.0,
      anomaly_score: 100.0,
    }
  });

  const [isWsConnected, setIsWsConnected] = useState(false);
  const [liveTimeline, setLiveTimeline] = useState([]);
  const [isHealing, setIsHealing] = useState(false);
  const [healingProgress, setHealingProgress] = useState(0);
  const [runningScraperId, setRunningScraperId] = useState(null);
  const [isRunningDemo, setIsRunningDemo] = useState(false);
  const [activeVersion, setActiveVersion] = useState('v1');
  const [activeTab, setActiveTab] = useState('overview');

  // Load Initial Telemetry
  const loadData = async () => {
    try {
      const [sum, scr, intel, heal] = await Promise.all([
        fetchDashboardSummary(),
        fetchScrapers(),
        fetchIntelligenceEvents(),
        fetchHealingEvents(),
      ]);
      setSummary(sum);
      setScrapers(scr);
      setIntelligenceEvents(intel);
      setHealingEvents(heal);

      if (scr.length > 0) {
        const h = await fetchScraperHealth(scr[0].id);
        setHealthData(h);
      }
    } catch (err) {
      console.error('Error loading data:', err);
    }
  };

  useEffect(() => {
    loadData();

    const ws = new WebSocketService((payload) => {
      setIsWsConnected(true);
      const { type, data } = payload;

      if (type === 'SELF_HEALING_TIMELINE_EVENT') {
        setLiveTimeline((prev) => [data, ...prev.slice(0, 15)]);
        setIsHealing(data.progress < 100);
        setHealingProgress(data.progress);
        if (data.progress === 100) {
          loadData();
        }
      } else if (type === 'INTELLIGENCE_EVENT_ALERT') {
        setIntelligenceEvents((prev) => [data, ...prev]);
        loadData();
      } else if (type === 'COLLECTION_RUN_COMPLETED') {
        setRunningScraperId(null);
        loadData();
      }
    });

    ws.connect();
    setIsWsConnected(true);

    return () => ws.disconnect();
  }, []);

  // Event Handlers
  const handleRunScraper = async (scraperId) => {
    setRunningScraperId(scraperId);
    try {
      await triggerScraperRun(scraperId);
      await loadData();
    } catch (err) {
      console.error('Error running scraper:', err);
    } finally {
      setRunningScraperId(null);
    }
  };

  const handleHealScraper = async (scraperId) => {
    setIsHealing(true);
    setHealingProgress(10);
    try {
      await triggerManualHealing(scraperId);
      await loadData();
    } catch (err) {
      console.error('Error triggering manual healing:', err);
    }
  };

  const handleSwitchVersion = async (v) => {
    setActiveVersion(v);
    if (scrapers.length > 0) {
      scrapers[0].target_url = `http://127.0.0.1:8000/demo-site/${v}`;
    }
  };

  const handleInjectPriceDrop = async (prodId, price) => {
    try {
      await mutateDemoPrice(prodId, price);
      if (scrapers.length > 0) {
        await handleRunScraper(scrapers[0].id);
      }
    } catch (err) {
      console.error('Error injecting price drop:', err);
    }
  };

  const handleResetDemo = async () => {
    await resetDemoLab();
    setActiveVersion('v1');
    await loadData();
  };

  // Automated Demo Flow
  const handleQuickTriggerDemo = async () => {
    setIsRunningDemo(true);
    try {
      setActiveVersion('v2');
      setLiveTimeline([
        {
          timestamp: new Date().toLocaleTimeString(),
          step: 'INITIATED',
          title: '🔥 Live Demo: Target Website Layout Mutated to V2',
          detail: 'Target changed selectors to data-testid="price". Baseline scraper broken.',
        }
      ]);

      if (scrapers.length > 0) {
        await triggerScraperRun(scrapers[0].id, true);
      }

      await mutateDemoPrice('LP-001', 124999.0);
      if (scrapers.length > 0) {
        await triggerScraperRun(scrapers[0].id, true);
      }

      await loadData();
    } catch (err) {
      console.error('Error running quick demo:', err);
    } finally {
      setIsRunningDemo(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8F6F0] text-[#111827] px-4 py-6 sm:px-8 sm:py-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Top Header */}
        <Header
          isWsConnected={isWsConnected}
          onQuickTriggerDemo={handleQuickTriggerDemo}
          isRunningDemo={isRunningDemo}
        />

        {/* Hero Explanation Banner */}
        <HeroExplanation />

        {/* Top Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <MetricCard
            title="Studio Collectors"
            value={summary.total_scrapers}
            subtitle={`${summary.healthy_scrapers} 100% Healthy`}
            iconType="cpu"
            color="dark"
            trend="+100% Uptime"
          />
          <MetricCard
            title="Fleet Extraction Health"
            value={`${summary.average_health_score}%`}
            subtitle="4-Layer Validated"
            iconType="activity"
            color="emerald"
            trend="Active Gate"
          />
          <MetricCard
            title="Self-Healing Repairs"
            value={summary.total_repairs_executed}
            subtitle={`${summary.healing_success_rate}% Success Rate`}
            iconType="shield"
            color="indigo"
            trend="100% Healed"
          />
          <MetricCard
            title="Competitive Alerts"
            value={summary.recent_intelligence_events}
            subtitle="Real-time Price & Stock"
            iconType="bell"
            color="amber"
            trend="Live Stream"
          />
        </div>

        {/* Main Grid: Self-Healing Timeline & Health Scoring */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column (8 cols): Self-Healing Timeline & DOM Diff */}
          <div className="lg:col-span-7 space-y-8">
            <SelfHealingTimeline
              timelineEvents={liveTimeline}
              isHealing={isHealing}
              currentProgress={healingProgress}
              latestHealingEvent={healingEvents[0]}
            />

            <DOMDiffViewer
              originalSelectors={scrapers[0]?.selector_manifest}
              repairedSelectors={healingEvents[0]?.repaired_selectors}
              isRepaired={true}
            />
          </div>

          {/* Right Column (5 cols): Scraper Health Scoring & Competitive Delta Feed */}
          <div className="lg:col-span-5 space-y-8">
            <HealthRadar
              healthScore={healthData.health_score}
              breakdown={healthData.breakdown}
            />

            <IntelligenceFeed events={intelligenceEvents} />
          </div>
        </div>

        {/* Competitor Collectors Table */}
        <CompetitorMatrix
          scrapers={scrapers}
          onRunScraper={handleRunScraper}
          onHealScraper={handleHealScraper}
          runningScraperId={runningScraperId}
        />

        {/* Chaos Demo Lab Interactive Panel */}
        <ChaosLabPanel
          onSwitchVersion={handleSwitchVersion}
          onInjectPriceDrop={handleInjectPriceDrop}
          onResetDemo={handleResetDemo}
          activeVersion={activeVersion}
        />

      </div>
    </div>
  );
}
