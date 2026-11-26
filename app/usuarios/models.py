import enum
from sqlalchemy import Enum, String, true
from sqlalchemy.orm import Mapped, mapped_column
from ..infra.database import Base, TimestampMixin


class Rol(str, enum.Enum):
    LECTOR = "lector"
    ADMIN = "admin"


class Usuario(TimestampMixin, Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[Rol] = mapped_column(
        Enum(
            Rol,
            name="rol_usuario",
            native_enum=False,
            create_constraint=True,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=Rol.LECTOR,
        server_default=Rol.LECTOR.value,
    )
    activo: Mapped[bool] = mapped_column(default=True, server_default=true())
    