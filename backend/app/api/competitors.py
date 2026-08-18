from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from backend.app.core.database import get_db
from backend.app.models.database_models import Competitor
from backend.app.schemas.competitor_schema import CompetitorCreate, CompetitorResponse

router = APIRouter(prefix="/competitors", tags=["Competitors"])

@router.get("", response_model=List[CompetitorResponse])
async def list_competitors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).order_by(Competitor.id.asc()))
    return result.scalars().all()

@router.post("", response_model=CompetitorResponse)
async def create_competitor(payload: CompetitorCreate, db: AsyncSession = Depends(get_db)):
    # Check duplicate
    existing = await db.execute(select(Competitor).where(Competitor.name == payload.name))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Competitor with this name already exists")
    
    comp = Competitor(**payload.model_dump())
    db.add(comp)
    await db.commit()
    await db.refresh(comp)
    return comp

@router.get("/{id}", response_model=CompetitorResponse)
async def get_competitor(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).where(Competitor.id == id))
    comp = result.scalars().first()
    if not comp:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return comp
