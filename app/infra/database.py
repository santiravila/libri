from datetime import datetime
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from sqlalchemy import DateTime, create_engine, func
from app.core.config import settings


engine = create_engine(
    url=settings.DATABASE_URL
)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Columnas de auditoría. La base de datos genera los valores (UTC, con zona horaria)."""

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_db_session)]