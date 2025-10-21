from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    POSTGRES_USER: str = "InsuranceUser"
    POSTGRES_PASSWORD: str = "InsurancePass"
    POSTGRES_DB: str = "InsuranceDB"
    DATABASE_URL: str = Field(default_factory=lambda: os.getenv("DATABASE_URL"))
    LOG_LEVEL: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    SCHEDULER_ENABLED: bool = Field(default_factory=lambda: os.getenv("SCHEDULER_ENABLED", "True") == "True")
    SCHEDULER_INTERVAL_SECONDS: int = Field(default_factory=lambda: int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "600")))
    TZ: str = Field(default_factory=lambda: os.getenv("TZ", "local"))
    SQL_ECHO: bool = False
    POOL_PRE_PING: bool = True
    POOL_SIZE: int = 5
    DB_TIMEOUT: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
