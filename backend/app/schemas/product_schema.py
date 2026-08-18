from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

class BrightDataScrapedProduct(BaseModel):
    product_name: str = Field(..., min_length=1)
    product_url: str = Field(..., min_length=5)
    price: float = Field(..., gt=0)
    currency: str = Field(default="INR")
    availability: str = Field(default="in_stock")
    discount: float = Field(default=0.0, ge=0.0, le=100.0)
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    scraped_at: Optional[str] = None

    @field_validator("availability")
    @classmethod
    def validate_availability(cls, v: str) -> str:
        clean = v.lower().strip()
        if "out" in clean or "unavailable" in clean:
            return "out_of_stock"
        return "in_stock"

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitor_id: int
    sku: Optional[str] = None
    product_name: str
    current_price: float
    original_price: Optional[float] = None
    currency: str
    availability: str
    discount_pct: float
    rating: float
    product_url: str
    last_scraped_at: datetime
