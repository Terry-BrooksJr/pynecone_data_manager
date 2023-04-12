from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Data Manager Webhook API"
    admin_email: str

    class Config:
        env_file = "webhook.env"
