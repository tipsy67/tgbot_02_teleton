from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from core.config import settings


class UserSchema(BaseModel):
    phone: str
    is_active: bool


class UserCreateUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    language_code: Optional[str] = settings.default_language_code
    model_config = ConfigDict(extra="ignore")


class UserResponse(UserCreateUpdate):
    id: int = Field(alias="_id", serialization_alias="id")
    created_at: datetime
    last_activity: datetime
    is_active: bool
    is_admin: bool = False
    is_speaker: bool = False
    is_banned: bool = False
