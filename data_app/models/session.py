from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from data_app.models.base import Base



class SessionModel(Base):
    __tablename__ = 'sessions'

    api_id:Mapped[int] = mapped_column(Integer)
    session_string:Mapped[str] = mapped_column(String, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # suffix:Mapped[str] = mapped_column(String, nullable=True)