from pydantic_settings import BaseSettings
import os

PROFILE = os.environ.get("ENVIRONMENT", "local")


class Config(BaseSettings):
    app_name: str = "My Application"
    debug_mode: bool = False
    rag_api_url: str = ""
    websocket_url: str = ""

    model_config = {
        "env_file": f".env.{PROFILE}",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Config()
