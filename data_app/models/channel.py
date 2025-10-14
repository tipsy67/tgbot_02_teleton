from sqlalchemy import Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_app.models import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_app.models.user import UserModel

class ChannelModel(Base):
    __tablename__ = "channels"
    chat_id: Mapped[int] = mapped_column(BigInteger)
    prompt: Mapped[str] = mapped_column(String)
    system_prompt: Mapped[str] = mapped_column(String)
    triggers: Mapped[str] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="channels")
