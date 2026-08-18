from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class ScraperBase(BaseModel):
    competitor_id: int
    name: str
    bright_data_scraper_id: str
    collector_id: str
    target_url: str
    selector_manifest: Optional[Dict[str, Any]] = None

class ScraperCreate(ScraperBase):
    pass

class ScraperResponse(ScraperBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    health_score: float
    last_run_at: Optional[datetime] = None
    created_at: datetime

class CollectionRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scraper_id: int
    execution_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str
    raw_records_count: int
    valid_records_count: int
    health_score: float
    health_breakdown: Dict[str, Any]
    error_message: Optional[str] = None
    raw_output_sample: List[Dict[str, Any]] = []
