from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_user: str
    database_password: str

    default_notification_recipient: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
