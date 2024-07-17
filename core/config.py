import os
import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Config(BaseSettings):
    ENV: str
    APP_HOST: str = "localhost"
    APP_PORT: int = 8080
    DB_URL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    DB_URL: str
    model_config = SettingsConfigDict(env_file=DOTENV)


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config():
    dotenv.load_dotenv(dotenv_path=DOTENV)
    env = os.getenv("ENV")
    config_type = {
        "development": DevelopmentConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config = get_config()
