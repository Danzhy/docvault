from datetime import datetime
from sqlalchemy import String, DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .connection import engine, Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(40))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        nullable=False
    )