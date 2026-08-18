import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add parent directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
import logging

from backend.app.core.config import settings
from backend.app.core.database import init_db, AsyncSessionLocal
from backend.app.models.database_models import Competitor, Scraper, Product, IntelligenceEvent, HealingEvent
from backend.app.services.bright_data_service import DEFAULT_SELECTORS

# Import routers
from backend.app.api.competitors import router as competitors_router
from backend.app.api.scrapers import router as scrapers_router
from backend.app.api.health import router as health_router
from backend.app.api.self_healing import router as self_healing_router
from backend.app.api.intelligence import router as intelligence_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.demo_targets import router as demo_targets_router
from backend.app.api.websockets import router as ws_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("sentinel")

async def seed_initial_data():
    """Seeds baseline competitors and scrapers if database is empty"""
    async with AsyncSessionLocal() as session:
        comp_count = await session.execute(select(Competitor))
        if not comp_count.scalars().first():
            logger.info("Seeding initial competitor and custom scraper definitions...")
            
            # Competitor 1: MegaStore Electronics (Primary Demo Target)
            c1 = Competitor(
                name="MegaStore Electronics",
                base_url="http://127.0.0.1:8000/demo-site/v1",
                category="Laptops & Computing"
            )
            session.add(c1)
            await session.flush()

            s1 = Scraper(
                competitor_id=c1.id,
                name="MegaStore Laptop Catalog Collector",
                bright_data_scraper_id="sc_custom_megastore_laptops_v1",
                collector_id="c_megastore_laptops_prod",
                target_url="http://127.0.0.1:8000/demo-site/v1",
                selector_manifest=DEFAULT_SELECTORS,
                status="ACTIVE",
                health_score=98.5
            )
            session.add(s1)

            # Competitor 2: TechNova Retail
            c2 = Competitor(
                name="TechNova Direct",
                base_url="https://technova-electronics.example.com/products",
                category="Workstations & PC"
            )
            session.add(c2)
            await session.flush()

            s2 = Scraper(
                competitor_id=c2.id,
                name="TechNova Premium Workstation Collector",
                bright_data_scraper_id="sc_custom_technova_ws_v1",
                collector_id="c_technova_ws_prod",
                target_url="http://127.0.0.1:8000/demo-site/v1",
                selector_manifest=DEFAULT_SELECTORS,
                status="ACTIVE",
                health_score=96.8
            )
            session.add(s2)

            # Seed initial intelligence events
            e1 = IntelligenceEvent(
                competitor_id=c1.id,
                event_type="PRICE_DROP",
                severity="CRITICAL",
                title="📉 Competitor Price Reduction: AeroBook Pro 16",
                description="MegaStore Electronics reduced AeroBook Pro 16 by ₹15,000 (-10.0%). Action recommended for matched inventory.",
                metadata_json={"old_price": 149999, "new_price": 134999, "diff_pct": -10.0}
            )
            session.add(e1)

            await session.commit()
            logger.info("Initial seed completed successfully.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Sentinel AI Backend Engine...")
    await init_db()
    await seed_initial_data()
    yield
    logger.info("Shutting down Sentinel AI Backend Engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade, Self-Healing Competitive Intelligence Platform powered by Bright Data Scraper Studio",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(competitors_router, prefix=settings.API_V1_STR)
app.include_router(scrapers_router, prefix=settings.API_V1_STR)
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(self_healing_router, prefix=settings.API_V1_STR)
app.include_router(intelligence_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(demo_targets_router)  # /demo-site/v1, /demo-site/v2, etc.
app.include_router(ws_router)

@app.get("/")
async def root():
    return {
        "system": "Sentinel AI - Self-Healing Competitive Intelligence Platform",
        "status": "ONLINE",
        "bright_data_scraper_studio": "CONNECTED",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }
