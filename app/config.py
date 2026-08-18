from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "dashboardku"
    DB_USER: str = "dashboardku"
    DB_PASS: str = "secret"

    # Auth
    APP_USERNAME: str = "admin"
    APP_PASSWORD: str = "changeme"
    APP_PASSWORD_HASH: str = ""  # Optional: pre-hashed password (bcrypt)
    SECRET_KEY: str = "dev-secret-change-me"

    # Webhook
    WAHA_WEBHOOK_URL: str = ""

    # App
    APP_ENV: str = "development"
    DEBUG: bool = True

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
