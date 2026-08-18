from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.models.database_models import Scraper, CollectionRun
from backend.app.schemas.health_schema import HealthReportResponse

router = APIRouter(prefix="/health", tags=["Health Monitor"])

@router.get("/scrapers/{id}", response_model=Dict[str, Any])
async def get_scraper_health(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Scraper).where(Scraper.id == id))
    scraper = result.scalars().first()
    if not scraper:
        raise HTTPException(status_code=404, detail="Scraper not found")

    # Get latest run breakdown
    run_res = await db.execute(
        select(CollectionRun).where(CollectionRun.scraper_id == id).order_by(CollectionRun.id.desc()).limit(1)
    )
    latest_run = run_res.scalars().first()

    breakdown = latest_run.health_breakdown if latest_run and latest_run.health_breakdown else {
        "completeness": 100.0,
        "schema_validity": 100.0,
        "volumetric_consistency": 100.0,
        "historical_consistency": 100.0,
        "anomaly_score": 100.0,
        "composite_health_score": scraper.health_score,
        "is_degraded": scraper.health_score < 70.0,
        "issues_detected": []
    }

    return {
        "scraper_id": scraper.id,
        "scraper_name": scraper.name,
        "health_score": scraper.health_score,
        "status": scraper.status,
        "last_run_at": scraper.last_run_at,
        "breakdown": breakdown
    }

@router.get("/fleet", response_model=List[Dict[str, Any]])
async def get_fleet_health(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Scraper).order_by(Scraper.id.asc()))
    scrapers = result.scalars().all()
    fleet = []
    for s in scrapers:
        fleet.append({
            "id": s.id,
            "name": s.name,
            "status": s.status,
            "health_score": s.health_score,
            "last_run_at": s.last_run_at
        })
    return fleet
