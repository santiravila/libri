from ..infra.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, ForeignKey, Null, null
from datetime import datetime

class SesionUsuario(Base):
    __tablename__ = "sesiones"

    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[str] = mapped_column(VARCHAR(256), unique=True)
    revocada_en: Mapped[datetime | None]
    creado_en: Mapped[datetime] = mapped_column(default=datetime.now)
    
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))