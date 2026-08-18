from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class CompetitorBase(BaseModel):
    name: str
    base_url: str
    category: str
    is_active: bool = True

class CompetitorCreate(CompetitorBase):
    pass

class CompetitorResponse(CompetitorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
