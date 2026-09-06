from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AURIX Secure Financial Intelligence Prototype"
    api_v1_prefix: str = ""
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/aurix"
    database_url_migrations: str | None = None
    jwt_secret: str = "change-me-in-env"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    jwt_issuer: str = "aurix-prototype"
    jwt_audience: str = "aurix-web"
    cors_origins: str = "http://localhost:3000"
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
