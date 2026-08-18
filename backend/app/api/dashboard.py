from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Dict, Any
from backend.app.core.database import get_db
from backend.app.models.database_models import Competitor, Scraper, Product, IntelligenceEvent, HealingEvent
from backend.app.schemas.intelligence_schema import DashboardSummaryResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard KPIs"])

@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    # Competitor count
    comp_c = await db.scalar(select(func.count(Competitor.id))) or 0
    # Scraper counts
    scrapers = (await db.execute(select(Scraper))).scalars().all()
    total_scrapers = len(scrapers)
    healthy_scrapers = sum(1 for s in scrapers if s.health_score >= 70.0 and s.status == "ACTIVE")
    degraded_scrapers = sum(1 for s in scrapers if s.health_score < 70.0 or s.status == "DEGRADED")
    healing_scrapers = sum(1 for s in scrapers if s.status == "HEALING")
    avg_health = sum(s.health_score for s in scrapers) / max(total_scrapers, 1) if scrapers else 100.0

    # Products count
    prod_c = await db.scalar(select(func.count(Product.id))) or 0
    # Intelligence Events count
    intel_c = await db.scalar(select(func.count(IntelligenceEvent.id))) or 0
    # Healing Events count & success rate
    healing_events = (await db.execute(select(HealingEvent))).scalars().all()
    total_repairs = len(healing_events)
    successful_repairs = sum(1 for h in healing_events if h.validation_status == "PASSED")
    recovery_rate = (successful_repairs / max(total_repairs, 1)) * 100.0 if total_repairs > 0 else 100.0

    return DashboardSummaryResponse(
        total_competitors=comp_c,
        total_scrapers=total_scrapers,
        healthy_scrapers=healthy_scrapers,
        degraded_scrapers=degraded_scrapers,
        healing_scrapers=healing_scrapers,
        total_products_monitored=prod_c,
        recent_intelligence_events=intel_c,
        total_repairs_executed=total_repairs,
        healing_success_rate=round(recovery_rate, 1),
        average_health_score=round(avg_health, 1)
    )
