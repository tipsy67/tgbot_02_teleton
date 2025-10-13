from datetime import datetime

from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from data_app.models.base import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from data_app.models.user import UserModel


class SessionModel(Base):
    __tablename__ = "sessions"
    phone_number: Mapped[str | None] = mapped_column(String(12))
    session_string: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    suffix: Mapped[str] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="sessions")
