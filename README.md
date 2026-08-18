# 🕷️ Sentinel AI — Self-Healing Competitive Intelligence Platform
> **Powered by Bright Data Scraper Studio**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Bright Data](https://img.shields.io/badge/Bright_Data-Scraper_Studio-00f0ff.svg?style=flat)](https://brightdata.com)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Problem Statement
Companies rely on public web data to monitor competitor catalogs, pricing shifts, and inventory dynamics. However, **competitor websites constantly change** their DOM structures, class names, and layout hierarchies. Traditional scrapers silently fail or return partial, degraded records, leaving businesses with stale or corrupted intelligence.

---

## 💡 Solution: Sentinel AI
**Sentinel AI** bridges **Bright Data Scraper Studio** with an autonomous self-healing intelligence pipeline:
1. **Continuous Collection**: Gathers structured competitor pricing, availability, discounts, and ratings via custom Scraper Studio collectors.
2. **Health Monitoring**: Evaluates every extraction across a 5-dimension scoring matrix (completeness, schema validity, volumetric consistency, historical drift, anomaly score).
3. **Autonomous Self-Healing**: Instantly detects selector degradation (e.g. `.price` broken by DOM mutations), synthesizes replacement selectors via DOM AST inspection, and re-executes collectors in an isolated sandbox.
4. **4-Tier Validation Gateway**: Rigorously verifies candidates across structural types, statistical distribution (IQR), historical sanity, and business invariants before promotion.
5. **Competitive Delta Intelligence**: Automatically computes price drops, stockouts, new product launches, and discount spikes into actionable alerts.

---

## 🏛️ System Architecture

```mermaid
flowchart TB
    subgraph ClientLayer["Frontend Mission Control (React 18 + Vite + Tailwind)"]
        UI_Dash["Executive KPI Dashboard"]
        UI_Timeline["Live Self-Healing Timeline & DOM Diff"]
        UI_Intel["Real-time Competitive Delta Feed"]
        UI_Chaos["Chaos Lab & Mutation Simulator"]
    end

    subgraph APILayer["Orchestration Engine (FastAPI Async + WebSockets)"]
        API_Gateway["FastAPI Gateway & WebSocket Hub"]
        HealthEngine["5-Dimension Health Monitor"]
        SelfHealing["Autonomous Self-Healing State Machine"]
        Validator["4-Tier Quality & Validation Gateway"]
        IntelEngine["Competitive Delta & Anomaly Engine"]
    end

    subgraph BrightDataLayer["Bright Data Scraper Studio Subsystem"]
        BD_Studio["Custom Scraper Studio Definition"]
        BD_Collector["Remote / Local Collector Runners"]
        BD_Healer["Bright Data Self-Healing API & AST Parser"]
    end

    subgraph StorageLayer["Data & Persistence Layer"]
        DB[(SQLite / PostgreSQL Async)]
    end

    ClientLayer <-->|REST & WebSocket| API_Gateway
    API_Gateway --> BD_Studio --> BD_Collector
    BD_Collector -->|Scraped JSON| HealthEngine
    HealthEngine -->|Score >= 70%| Validator
    HealthEngine -->|Degraded < 70%| SelfHealing
    SelfHealing -->|Repaired Selectors| BD_Collector
    BD_Collector -->|Candidate Records| Validator
    Validator -->|Passed (>90%)| IntelEngine
    IntelEngine --> DB
    IntelEngine -->|Real-time Alerts| API_Gateway
```

---

## 📊 Scraper Health Scoring Formula

$$\text{Health Score} = 0.30 \cdot S_{\text{completeness}} + 0.20 \cdot S_{\text{schema}} + 0.20 \cdot S_{\text{volumetric}} + 0.15 \cdot S_{\text{historical}} + 0.15 \cdot S_{\text{anomaly}}$$

- **Completeness ($S_{\text{completeness}}$)**: Non-null presence of mandatory fields (`product_name`, `price`, `availability`, `product_url`).
- **Schema Validity ($S_{\text{schema}}$)**: Percentage passing strict Pydantic v2 type checks.
- **Volumetric Consistency ($S_{\text{volumetric}}$)**: Deviation from expected catalog quantity.
- **Historical Drift ($S_{\text{historical}}$)**: Catalog overlap with prior runs.
- **Anomaly Score ($S_{\text{anomaly}}$)**: Price distribution bounds and outlier penalty.

---

## 🛡️ 4-Tier Validation Gateway

Before any candidate data updates production intelligence:
1. **Tier 1 (Structural)**: Pydantic v2 type validation, URL format, and mandatory field checks.
2. **Tier 2 (Statistical)**: Interquartile Range (IQR) outlier detection to catch decimal point shifts ($19.99 vs $1999).
3. **Tier 3 (Historical Sanity)**: Flags anomalous massive catalog turnover in a single run.
4. **Tier 4 (Business Invariants)**:
   - `price > 0`
   - `0 <= discount_percentage <= 100`
   - `0.0 <= rating <= 5.0`
   - Canonical URL domain matches competitor base URL

---

## 🧪 Controlled Demo Environment (Chaos Lab)

Sentinel AI includes a built-in multi-version website target server:
- **Version 1.0 (Baseline)**: Standard CSS selectors (`.product-card`, `.price`, `.product-title`).
- **Version 2.0 (Mutated DOM)**: Renamed attributes (`[data-testid="price"]`, `.c-val-amount`) simulating frontend redesigns.
- **Version 3.0 (Semantic Microdata)**: Schema.org hierarchy (`itemprop="price"`).

### Demo Failure & Self-Healing Cycle:
```
1. Scraper runs against V1.0  ──►  100% Health (6/6 records)
2. Target switches to V2.0   ──►  Degradation Alert (Health drops to 28%)
3. Sentinel detects change   ──►  Autonomous Self-Healing initiated
4. AST Selector repaired     ──►  .price transformed to [data-testid="price"]
5. Sandbox re-execution      ──►  6/6 records extracted
6. 4-Tier Validation Gate    ──►  PASSED (Validation Score: 98.8%)
7. Competitive Intelligence  ──►  Price drop delta alert dispatched
```

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- **Python 3.10+** (tested on Python 3.14)
- **Node.js 18+** & npm

### 1. Clone & Install Backend
```bash
cd backend
python -m pip install -r requirements.txt
```

### 2. Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 3. Run Development Servers
In Terminal 1 (Backend):
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

In Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Open your browser at **`http://127.0.0.1:5173`** to access the Sentinel AI Mission Control Dashboard.

---

## 🧪 Running Automated Tests

Run the complete pytest test suite:
```bash
python -m pytest backend/tests/ -v
```

---

## 📹 4-Minute Presentation & Demo Script

| Timestamp | Section | Key Demo Action |
|:---|:---|:---|
| **0:00 - 0:25** | **The Problem** | Explain why competitor scrapers silently degrade when websites change. |
| **0:25 - 0:55** | **Product Tour** | Showcase Sentinel AI Dashboard, KPIs, and live collector fleet. |
| **0:55 - 1:25** | **Bright Data Integration** | Show custom Scraper Studio definitions & structured JSON output. |
| **1:25 - 1:55** | **Breaking the Target** | Switch Chaos Lab target to V2.0 with mutated attributes. |
| **1:55 - 2:35** | **Autonomous Self-Healing** | Watch the Live Timeline stream AST parsing, selector repair, and sandbox recovery. |
| **2:35 - 3:15** | **4-Tier Validation** | Review validation gate metrics and promoted selector manifest. |
| **3:15 - 3:45** | **Competitive Delta Intel** | Demonstrate real-time price drop detection and actionable alerts. |
| **3:45 - 4:00** | **Conclusion** | Highlight enterprise value: zero maintenance, resilient public web data. |

---

## 🤖 AI Development Disclosure
AI coding assistants were utilized during development for implementation assistance, architecture ideation, boilerplate generation, and test creation. All code was reviewed, debugged, tested, and understood by the team. The team remains responsible for the technical architecture, implementation, and submission.

---

## 📄 License
MIT License. Created for the **Bright Data Hackathon 2026**.
