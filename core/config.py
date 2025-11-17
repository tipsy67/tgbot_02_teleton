import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
WORKER_LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d][%(processName)s] %(module)16s:%(lineno)-3d %(levelname)-7s - %(message)s"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class TelegramConfig(BaseModel):
    api_id: str = ""
    api_hash: str = ""
    default_language_code: str = "en"

    @property
    def session(self) -> str:
        return str(Path(BASE_DIR) / "core" / "session" / self.api_id)


class DeepseekConfig(BaseModel):
    api_url: str
    api_key: str


class BrokerConfig(LoggingConfig):
    redis_url: str = ""
    log_format: str = WORKER_LOG_DEFAULT_FORMAT
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    queue_name: str = "taskiq:queue"


class DataBaseConfig(BaseModel):
    url: PostgresDsn = ""
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

class HealthCheck(BaseModel):
    heartbeat_timeout: int = 300
    period: int = 120


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    channels: str = "/channels"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

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
    api: ApiPrefix = ApiPrefix()
    broker: BrokerConfig = BrokerConfig()
    db: DataBaseConfig = DataBaseConfig()
    deepseek: DeepseekConfig
    healthcheck: HealthCheck = HealthCheck()
    logging: LoggingConfig = LoggingConfig()
    tg: TelegramConfig = TelegramConfig()
    suffixes:list[str] = ["worker"]


settings = Settings()
