from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str 
    DATABASE_URL: str 
    LOG_LEVEL: str = Field("INFO")
    TZ: str = Field("local")
    SQL_ECHO: bool = False
    POOL_PRE_PING: bool = True
    POOL_SIZE: int = 5
    DB_TIMEOUT: int = 30
    REDIS_URL: str 
    SCHEDULER_ENABLED: bool = Field("true")
    SCHEDULER_INTERVAL_SECONDS: int = Field(600)
    API_TITLE: str = "Car Insurance Project"
    API_VERSION: str = "v1"
    OPENAPI_VERSION: str = "3.0.3"
    OPENAPI_URL_PREFIX: str = "/docs"
    OPENAPI_SWAGGER_UI_PATH: str = "/"
    OPENAPI_SWAGGER_UI_URL: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()