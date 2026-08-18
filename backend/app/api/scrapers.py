import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any, Optional
from backend.app.core.database import get_db, AsyncSessionLocal
from backend.app.models.database_models import Scraper, CollectionRun, Competitor, HealingEvent
from backend.app.schemas.scraper_schema import ScraperCreate, ScraperResponse, CollectionRunResponse
from backend.app.services.bright_data_service import bright_data_service, DEFAULT_SELECTORS
from backend.app.services.health_monitor import health_monitor
from backend.app.services.validation_engine import validation_engine
from backend.app.services.self_healer import self_healer
from backend.app.services.intelligence_engine import intelligence_engine
from backend.app.core.ws_manager import ws_manager

router = APIRouter(prefix="/scrapers", tags=["Scrapers"])

@router.get("", response_model=List[ScraperResponse])
async def list_scrapers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Scraper).order_by(Scraper.id.asc()))
    return result.scalars().all()

@router.post("", response_model=ScraperResponse)
async def create_scraper(payload: ScraperCreate, db: AsyncSession = Depends(get_db)):
    # Check competitor
    comp = await db.execute(select(Competitor).where(Competitor.id == payload.competitor_id))
    if not comp.scalars().first():
        raise HTTPException(status_code=404, detail="Competitor not found")

    scraper = Scraper(
        competitor_id=payload.competitor_id,
        name=payload.name,
        bright_data_scraper_id=payload.bright_data_scraper_id,
        collector_id=payload.collector_id,
        target_url=payload.target_url,
        selector_manifest=payload.selector_manifest or DEFAULT_SELECTORS,
        status="ACTIVE",
        health_score=100.0
    )
    db.add(scraper)
    await db.commit()
    await db.refresh(scraper)
    return scraper

@router.get("/{id}", response_model=ScraperResponse)
async def get_scraper(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Scraper).where(Scraper.id == id))
    scraper = result.scalars().first()
    if not scraper:
        raise HTTPException(status_code=404, detail="Scraper not found")
    return scraper

@router.post("/{id}/run", response_model=CollectionRunResponse)
async def run_scraper(
    id: int,
    auto_heal: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """
    Executes Bright Data Scraper Studio Collector, scores extraction health,
    triggers self-healing if degraded, validates records, and updates intelligence.
    """
    result = await db.execute(select(Scraper).where(Scraper.id == id))
    scraper = result.scalars().first()
    if not scraper:
        raise HTTPException(status_code=404, detail="Scraper not found")

    execution_id = f"run_{uuid.uuid4().hex[:8]}"
    start_time = datetime.datetime.utcnow()

    # Broadcast run started
    await ws_manager.broadcast("COLLECTION_RUN_STARTED", {
        "scraper_id": scraper.id,
        "scraper_name": scraper.name,
        "execution_id": execution_id
    })

    # Step 1: Execute collector with current selectors
    current_selectors = scraper.selector_manifest or DEFAULT_SELECTORS
    collector_res = await bright_data_service.trigger_collector(
        target_url=scraper.target_url,
        custom_selectors=current_selectors
    )
    raw_records = collector_res.get("records", [])

    # Step 2: Evaluate Health Score
    health_eval = health_monitor.evaluate_run(raw_records, expected_count=6)
    health_score = health_eval["composite_health_score"]
    is_degraded = health_eval["is_degraded"]

    run_status = "SUCCESS"
    healing_record = None
    processed_records = raw_records

    # Step 3: Self-Healing Trigger if degraded
    if is_degraded and auto_heal:
        scraper.status = "HEALING"
        await db.commit()

        heal_result = await self_healer.heal_scraper(
            scraper_id=scraper.id,
            target_url=scraper.target_url,
            current_selectors=current_selectors,
            broken_records_count=len(raw_records),
            health_before=health_score
        )

        if heal_result["status"] == "RESTORED":
            # Update scraper selector manifest with healed selectors
            scraper.selector_manifest = heal_result["repaired_selectors"]
            scraper.health_score = heal_result["health_after"]
            scraper.status = "ACTIVE"
            health_score = heal_result["health_after"]
            processed_records = heal_result["recovered_records"]
            run_status = "HEALED"

            # Create healing event record
            healing_record = HealingEvent(
                scraper_id=scraper.id,
                trigger_reason="Extraction health degradation below 70%",
                failure_type="SELECTOR_MISMATCH",
                original_selectors=heal_result["original_selectors"],
                repaired_selectors=heal_result["repaired_selectors"],
                dom_diff_summary=heal_result["dom_diff_summary"],
                records_before=heal_result["records_before"],
                records_after=heal_result["records_after"],
                health_before=heal_result["health_before"],
                health_after=heal_result["health_after"],
                validation_status="PASSED",
                duration_ms=heal_result["duration_ms"]
            )
            db.add(healing_record)
        else:
            scraper.status = "DEGRADED"
            scraper.health_score = health_score
            run_status = "DEGRADED"
    else:
        scraper.health_score = health_score
        scraper.status = "DEGRADED" if is_degraded else "ACTIVE"

    # Step 4: Multi-Layer Validation
    val_res = validation_engine.validate_dataset(processed_records, expected_records_count=6)
    valid_records = val_res["valid_records"]

    # Step 5: Feed into Competitive Intelligence Engine
    if val_res["verdict"] in ["PASSED", "QUARANTINED"] and valid_records:
        await intelligence_engine.process_scraped_products(
            db=db,
            competitor_id=scraper.competitor_id,
            scraped_records=valid_records
        )

    # Step 6: Persist Collection Run
    scraper.last_run_at = datetime.datetime.utcnow()
    run = CollectionRun(
        scraper_id=scraper.id,
        execution_id=execution_id,
        started_at=start_time,
        completed_at=datetime.datetime.utcnow(),
        status=run_status,
        raw_records_count=len(processed_records),
        valid_records_count=len(valid_records),
        health_score=health_score,
        health_breakdown=health_eval,
        raw_output_sample=processed_records[:3]
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)

    # Broadcast completed
    await ws_manager.broadcast("COLLECTION_RUN_COMPLETED", {
        "run_id": run.id,
        "scraper_id": scraper.id,
        "status": run.status,
        "health_score": health_score,
        "records_count": len(valid_records)
    })

    return run

@router.get("/{id}/runs", response_model=List[CollectionRunResponse])
async def list_scraper_runs(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CollectionRun).where(CollectionRun.scraper_id == id).order_by(CollectionRun.id.desc()).limit(20)
    )
    return result.scalars().all()
