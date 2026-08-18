from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Sentinel AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Storage
    DATABASE_URL: str = "sqlite+aiosqlite:///./sentinel.db"
    
    # Bright Data Scraper Studio & API
    BRIGHT_DATA_API_KEY: Optional[str] = "bd_demo_mock_key_sentinel_2026"
    BRIGHT_DATA_CUSTOMER_ID: Optional[str] = "hl_sentinel_corp"
    BRIGHT_DATA_ZONE: Optional[str] = "scraper_studio_prod"
    BRIGHT_DATA_COLLECTOR_ID: str = "c_sentinel_laptops_v1"
    BRIGHT_DATA_BASE_API_URL: str = "https://api.brightdata.com"
    
    # Self-Healing Thresholds
    HEALTH_CRITICAL_THRESHOLD: float = 70.0  # Below 70 triggers self-healing
    VALIDATION_PASS_THRESHOLD: float = 90.0  # 90% required to promote candidate
    
    # Mock / Demo Lab Target Ports & Paths
    CHAOS_LAB_ENABLED: bool = True
    CHAOS_LAB_URL: str = "http://127.0.0.1:8000/demo-site"
    
    # Data directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"

settings = Settings()
