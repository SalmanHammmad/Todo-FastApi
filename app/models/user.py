from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from .base import Base
from typing import List

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    todos: Mapped[List["Todo"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
