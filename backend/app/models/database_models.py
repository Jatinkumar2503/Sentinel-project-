import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    base_url = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    scrapers = relationship("Scraper", back_populates="competitor", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="competitor", cascade="all, delete-orphan")
    intelligence_events = relationship("IntelligenceEvent", back_populates="competitor", cascade="all, delete-orphan")

class Scraper(Base):
    __tablename__ = "scrapers"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False)
    name = Column(String(100), nullable=False)
    bright_data_scraper_id = Column(String(100), nullable=False)
    collector_id = Column(String(100), nullable=False)
    target_url = Column(String(255), nullable=False)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, DEGRADED, HEALING, PAUSED
    health_score = Column(Float, default=100.0)
    last_run_at = Column(DateTime, nullable=True)
    selector_manifest = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    competitor = relationship("Competitor", back_populates="scrapers")
    runs = relationship("CollectionRun", back_populates="scraper", cascade="all, delete-orphan")
    healing_events = relationship("HealingEvent", back_populates="scraper", cascade="all, delete-orphan")

class CollectionRun(Base):
    __tablename__ = "collection_runs"

    id = Column(Integer, primary_key=True, index=True)
    scraper_id = Column(Integer, ForeignKey("scrapers.id"), nullable=False)
    execution_id = Column(String(100), unique=True, index=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="RUNNING")  # SUCCESS, DEGRADED, FAILED, HEALED
    raw_records_count = Column(Integer, default=0)
    valid_records_count = Column(Integer, default=0)
    health_score = Column(Float, default=0.0)
    health_breakdown = Column(JSON, default=dict)
    error_message = Column(Text, nullable=True)
    raw_output_sample = Column(JSON, default=list)

    scraper = relationship("Scraper", back_populates="runs")
    healing_events = relationship("HealingEvent", back_populates="run", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False)
    sku = Column(String(100), index=True)
    product_name = Column(String(255), nullable=False)
    current_price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    currency = Column(String(10), default="INR")
    availability = Column(String(50), default="in_stock")  # in_stock, out_of_stock, backorder
    discount_pct = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    product_url = Column(String(500), nullable=False)
    last_scraped_at = Column(DateTime, default=datetime.datetime.utcnow)

    competitor = relationship("Competitor", back_populates="products")
    history = relationship("ProductHistory", back_populates="product", cascade="all, delete-orphan")
    intelligence_events = relationship("IntelligenceEvent", back_populates="product", cascade="all, delete-orphan")

class ProductHistory(Base):
    __tablename__ = "product_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    discount_pct = Column(Float, default=0.0)
    availability = Column(String(50), default="in_stock")
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="history")

class HealingEvent(Base):
    __tablename__ = "healing_events"

    id = Column(Integer, primary_key=True, index=True)
    scraper_id = Column(Integer, ForeignKey("scrapers.id"), nullable=False)
    run_id = Column(Integer, ForeignKey("collection_runs.id"), nullable=True)
    trigger_reason = Column(String(255), nullable=False)
    failure_type = Column(String(100), nullable=False)  # SELECTOR_MISMATCH, MISSING_FIELDS, DOM_RESTRUCTURE
    original_selectors = Column(JSON, default=dict)
    repaired_selectors = Column(JSON, default=dict)
    dom_diff_summary = Column(JSON, default=dict)
    records_before = Column(Integer, default=0)
    records_after = Column(Integer, default=0)
    health_before = Column(Float, default=0.0)
    health_after = Column(Float, default=0.0)
    validation_status = Column(String(50), default="PASSED")  # PASSED, REJECTED, QUARANTINED
    duration_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    scraper = relationship("Scraper", back_populates="healing_events")
    run = relationship("CollectionRun", back_populates="healing_events")

class IntelligenceEvent(Base):
    __tablename__ = "intelligence_events"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    event_type = Column(String(50), nullable=False)  # PRICE_DROP, PRICE_INCREASE, NEW_PRODUCT, OUT_OF_STOCK, HIGH_DISCOUNT
    severity = Column(String(20), default="INFO")  # INFO, WARNING, CRITICAL
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    competitor = relationship("Competitor", back_populates="intelligence_events")
    product = relationship("Product", back_populates="intelligence_events")
