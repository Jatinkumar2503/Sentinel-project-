from pydantic import BaseModel
from typing import Dict, Any, List

class HealthScoreBreakdown(BaseModel):
    completeness: float
    schema_validity: float
    volumetric_consistency: float
    historical_consistency: float
    anomaly_score: float
    composite_health_score: float
    is_degraded: bool
    issues_detected: List[str]

class HealthReportResponse(BaseModel):
    scraper_id: int
    health_score: float
    status: str
    breakdown: HealthScoreBreakdown
