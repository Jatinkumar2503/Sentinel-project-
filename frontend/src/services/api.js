const API_BASE = '/api';

export async function fetchDashboardSummary() {
  const res = await fetch(`${API_BASE}/dashboard/summary`);
  if (!res.ok) throw new Error('Failed to fetch dashboard summary');
  return res.json();
}

export async function fetchCompetitors() {
  const res = await fetch(`${API_BASE}/competitors`);
  if (!res.ok) throw new Error('Failed to fetch competitors');
  return res.json();
}

export async function fetchScrapers() {
  const res = await fetch(`${API_BASE}/scrapers`);
  if (!res.ok) throw new Error('Failed to fetch scrapers');
  return res.json();
}

export async function triggerScraperRun(scraperId, autoHeal = true) {
  const res = await fetch(`${API_BASE}/scrapers/${scraperId}/run?auto_heal=${autoHeal}`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to execute scraper run');
  return res.json();
}

export async function fetchScraperHealth(scraperId) {
  const res = await fetch(`${API_BASE}/health/scrapers/${scraperId}`);
  if (!res.ok) throw new Error('Failed to fetch scraper health');
  return res.json();
}

export async function fetchHealingEvents() {
  const res = await fetch(`${API_BASE}/self-healing/events`);
  if (!res.ok) throw new Error('Failed to fetch healing events');
  return res.json();
}

export async function triggerManualHealing(scraperId) {
  const res = await fetch(`${API_BASE}/self-healing/trigger`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scraper_id: scraperId, force_repair: true }),
  });
  if (!res.ok) throw new Error('Failed to trigger manual self-healing');
  return res.json();
}

export async function fetchIntelligenceEvents() {
  const res = await fetch(`${API_BASE}/intelligence/events?limit=30`);
  if (!res.ok) throw new Error('Failed to fetch intelligence events');
  return res.json();
}

export async function fetchProducts() {
  const res = await fetch(`${API_BASE}/intelligence/products`);
  if (!res.ok) throw new Error('Failed to fetch monitored products');
  return res.json();
}

export async function mutateDemoPrice(productId, newPrice) {
  const res = await fetch(`/demo-site/mutate-price?product_id=${productId}&new_price=${newPrice}`, {
    method: 'POST',
  });
  return res.json();
}

export async function resetDemoLab() {
  const res = await fetch('/demo-site/reset', { method: 'POST' });
  return res.json();
}
