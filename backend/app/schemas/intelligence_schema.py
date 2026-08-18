from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class IntelligenceEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitor_id: int
    product_id: Optional[int]
    event_type: str
    severity: str
    title: str
    description: str
    metadata_json: Dict[str, Any]
    created_at: datetime

class DashboardSummaryResponse(BaseModel):
    total_competitors: int
    total_scrapers: int
    healthy_scrapers: int
    degraded_scrapers: int
    healing_scrapers: int
    total_products_monitored: int
    recent_intelligence_events: int
    total_repairs_executed: int
    healing_success_rate: float
    average_health_score: float
