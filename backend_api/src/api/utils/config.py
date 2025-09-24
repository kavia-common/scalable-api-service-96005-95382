import os
from functools import lru_cache

from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load .env if present
load_dotenv()


class Settings(BaseModel):
    GRAFANA_BASE_URL: str = Field(default=os.getenv("GRAFANA_BASE_URL", "http://localhost:3000"))
    GRAFANA_API_KEY: str = Field(default=os.getenv("GRAFANA_API_KEY", ""))
    TOKEN_SECRET: str = Field(default=os.getenv("TOKEN_SECRET", ""))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
