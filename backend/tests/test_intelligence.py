import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.core.database import Base
from backend.app.models.database_models import Competitor, Product, IntelligenceEvent
from backend.app.services.intelligence_engine import intelligence_engine

@pytest.mark.asyncio
async def test_intelligence_engine_detects_price_drop():
    # Setup in-memory sqlite
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    TestSession = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

    async with TestSession() as session:
        # Create competitor
        comp = Competitor(name="Test Corp", base_url="http://test.com", category="Laptops")
        session.add(comp)
        await session.commit()
        await session.refresh(comp)

        # Baseline product run
        initial_records = [{
            "product_name": "Test Laptop Ultra",
            "product_url": "http://test.com/ultra",
            "price": 100000.0,
            "currency": "INR",
            "availability": "in_stock",
            "discount": 0.0,
            "rating": 4.5
        }]
        events1 = await intelligence_engine.process_scraped_products(session, comp.id, initial_records)
        assert len(events1) == 1
        assert events1[0]["type"] == "NEW_PRODUCT"

        # Subsequent run with 15% price drop
        dropped_records = [{
            "product_name": "Test Laptop Ultra",
            "product_url": "http://test.com/ultra",
            "price": 85000.0,  # 15% drop
            "currency": "INR",
            "availability": "in_stock",
            "discount": 15.0,
            "rating": 4.5
        }]
        events2 = await intelligence_engine.process_scraped_products(session, comp.id, dropped_records)
        assert len(events2) == 1
        assert events2[0]["type"] == "PRICE_DROP"
