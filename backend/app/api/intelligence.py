from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from backend.app.core.database import get_db
from backend.app.models.database_models import IntelligenceEvent, Product, ProductHistory
from backend.app.schemas.intelligence_schema import IntelligenceEventResponse
from backend.app.schemas.product_schema import ProductResponse

router = APIRouter(prefix="/intelligence", tags=["Competitive Intelligence"])

@router.get("/events", response_model=List[IntelligenceEventResponse])
async def list_intelligence_events(
    severity: Optional[str] = None,
    competitor_id: Optional[int] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(IntelligenceEvent).order_by(IntelligenceEvent.id.desc())
    if severity:
        query = query.where(IntelligenceEvent.severity == severity.upper())
    if competitor_id:
        query = query.where(IntelligenceEvent.competitor_id == competitor_id)
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/products", response_model=List[ProductResponse])
async def list_monitored_products(
    competitor_id: Optional[int] = None,
    availability: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Product).order_by(Product.id.asc())
    if competitor_id:
        query = query.where(Product.competitor_id == competitor_id)
    if availability:
        query = query.where(Product.availability == availability)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/products/{id}/history")
async def get_product_price_history(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProductHistory).where(ProductHistory.product_id == id).order_by(ProductHistory.recorded_at.asc())
    )
    history = result.scalars().all()
    return [{"price": h.price, "discount_pct": h.discount_pct, "availability": h.availability, "timestamp": h.recorded_at} for h in history]
