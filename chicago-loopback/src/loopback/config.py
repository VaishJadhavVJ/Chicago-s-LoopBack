from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = Field(default="postgresql+psycopg2://postgres:postgres@localhost:5432/loopback")

    MAPBOX_TOKEN: str = Field(default="")
    MAX_MAPBOX_ROUTES: int = Field(default=3)

    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini")

    GEOHASH_PRECISION: int = Field(default=7)
    ISSUE_NEAR_ROUTE_METERS: int = Field(default=80)
    MAX_LLM_SEVERITY_ADJUST: int = Field(default=1)

settings = Settings()