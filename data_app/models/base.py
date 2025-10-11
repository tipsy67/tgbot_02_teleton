from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.schema import MetaData

from core.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        """Универсальный repr для всех моделей"""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            return f"<{class_name}(id={self.id})>"
        else:
            return f"<{class_name}(unsaved)>"
