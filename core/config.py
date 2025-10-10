from pathlib import Path

from pydantic import BaseModel, Field, PostgresDsn
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

class DataBaseConfig(BaseModel):
    url:PostgresDsn = ""
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


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
    db: DataBaseConfig = DataBaseConfig()
    deepseek: DeepseekConfig
    tg: TelegramConfig




settings = Settings()
