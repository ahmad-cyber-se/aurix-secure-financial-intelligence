from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AURIX Secure Financial Intelligence Prototype"
    api_v1_prefix: str = ""
    database_url: str
    database_url_migrations: str | None = None
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    jwt_issuer: str = "aurix-prototype"
    jwt_audience: str = "aurix-web"
    cors_origins: str = ""
    frontend_url: str | None = None
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [self.frontend_url or "", *self.cors_origins.split(",")]
        return [origin.strip() for origin in origins if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
