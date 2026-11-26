from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from .models import Rol


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioCrear(UsuarioBase):
    password: str  # viaja en texto plano (lo protege HTTPS); se guarda hasheado con argon2


class UsuarioRespuesta(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    rol: Rol
    activo: bool
    creado_en: datetime
    # NB: ni password ni password_hash se exponen nunca


class UsuarioActualizar(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
