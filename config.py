from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    govee_api_key: str
    govee_base_url: str = "https://openapi.api.govee.com/router/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()