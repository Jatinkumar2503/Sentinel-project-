from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.models.database_models import Scraper, HealingEvent
from backend.app.schemas.healing_schema import HealingEventResponse, HealingTriggerRequest
from backend.app.services.self_healer import self_healer
from backend.app.services.bright_data_service import DEFAULT_SELECTORS

router = APIRouter(prefix="/self-healing", tags=["Self Healing"])

@router.get("/events", response_model=List[HealingEventResponse])
async def list_healing_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HealingEvent).order_by(HealingEvent.id.desc()).limit(20))
    return result.scalars().all()

@router.post("/trigger", response_model=Dict[str, Any])
async def trigger_manual_healing(payload: HealingTriggerRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Scraper).where(Scraper.id == payload.scraper_id))
    scraper = result.scalars().first()
    if not scraper:
        raise HTTPException(status_code=404, detail="Scraper not found")

    heal_res = await self_healer.heal_scraper(
        scraper_id=scraper.id,
        target_url=scraper.target_url,
        current_selectors=scraper.selector_manifest or DEFAULT_SELECTORS,
        health_before=scraper.health_score
    )

    if heal_res["status"] == "RESTORED":
        scraper.selector_manifest = heal_res["repaired_selectors"]
        scraper.health_score = heal_res["health_after"]
        scraper.status = "ACTIVE"

        healing_event = HealingEvent(
            scraper_id=scraper.id,
            trigger_reason="Manual Operator Self-Healing Invocation",
            failure_type="MANUAL_REPAIR",
            original_selectors=heal_res["original_selectors"],
            repaired_selectors=heal_res["repaired_selectors"],
            dom_diff_summary=heal_res["dom_diff_summary"],
            records_before=heal_res["records_before"],
            records_after=heal_res["records_after"],
            health_before=heal_res["health_before"],
            health_after=heal_res["health_after"],
            validation_status="PASSED",
            duration_ms=heal_res["duration_ms"]
        )
        db.add(healing_event)
        await db.commit()

    return heal_res
