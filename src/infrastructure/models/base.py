from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=True, nullable=True, default=None)