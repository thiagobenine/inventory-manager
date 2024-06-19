from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str = "mongodb://localhost:27017"
    PROJECT_NAME: str = "Inventory Manager"
    DEBUG: bool = True
    TELEGRAM_WEBHOOK_URL: str = "fake"
    TELEGRAM_BOT_TOKEN: str = "fake"
    PORT: int = 5000
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
