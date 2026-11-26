from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRespuesta(BaseModel):
    ok: bool
    usuario_id: int | None = None
    token: str | None = None