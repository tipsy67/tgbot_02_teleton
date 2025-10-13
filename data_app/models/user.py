import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.config import settings
from data_app.models import Base, SessionModel
from data_app.models.channel import ChannelModel


class UserModel(Base):
    __tablename__ = "users"
    tg_id: Mapped[int| None] = mapped_column(
        BigInteger, index=True
    )
    username: Mapped[str | None] = mapped_column(String(50))
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    phone_number: Mapped[str | None] = mapped_column(String(12))
    language_code: Mapped[str | None] = mapped_column(
        String(2), default=settings.tg.default_language_code
    )
    user_uuid: Mapped[uuid.UUID | None] = mapped_column(default=uuid.uuid4)
    created_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_activity: Mapped[datetime | None] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    channels: Mapped[list[ChannelModel]] = relationship(
        "ChannelModel", back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[list[SessionModel]] = relationship(
        "SessionModel", back_populates="user", cascade="all, delete-orphan"
    )
