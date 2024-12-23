from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

# Initialize settings
settings = Settings()
