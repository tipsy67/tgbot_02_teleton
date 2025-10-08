from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class TelegramConfig(BaseModel):
    api_id:str
    api_hash:str

    @property
    def session(self) -> str:
        return str(Path(BASE_DIR) / "core" / "session" / self.api_id)


class DeepseekConfig(BaseModel):
    api_url:str
    api_key:str


class BrokerConfig(BaseModel):
    redis_url:str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env",
            # BASE_DIR / ".env.dan",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    broker: BrokerConfig
    deepseek: DeepseekConfig
    tg: TelegramConfig




settings = Settings()
