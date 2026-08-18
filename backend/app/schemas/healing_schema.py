from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class HealingEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scraper_id: int
    run_id: Optional[int]
    trigger_reason: str
    failure_type: str
    original_selectors: Dict[str, Any]
    repaired_selectors: Dict[str, Any]
    dom_diff_summary: Dict[str, Any]
    records_before: int
    records_after: int
    health_before: float
    health_after: float
    validation_status: str
    duration_ms: int
    created_at: datetime

class HealingTriggerRequest(BaseModel):
    scraper_id: int
    force_repair: bool = False
