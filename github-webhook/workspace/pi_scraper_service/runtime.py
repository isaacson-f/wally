from pydantic_settings import BaseSettings, SettingsConfigDict


class RuntimeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PI_SCRAPER_", extra="ignore")

    playwright_browser: str = "camoufox"
    default_timeout_seconds: int = 60
    artifact_root: str = "artifacts"
