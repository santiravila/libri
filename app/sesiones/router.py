from fastapi import APIRouter, Header
from ..usuarios.models import Usuario
from ..usuarios.schema import UsuarioLogin
from ..usuarios.dependencies import ServiceDep as UsuarioServiceDep
from .schema import LoginRespuesta, LogoutRespuesta
from .dependencies import ServiceDep as SesionServiceDep, UsuarioActual
from typing import Annotated


router = APIRouter(
    prefix="/sesiones",
    tags=["sesiones"]
)


@router.post("/login", response_model=LoginRespuesta)
def login(
    payload: UsuarioLogin,
    servicio_usuario: UsuarioServiceDep,
    servicio_sesion: SesionServiceDep
) -> LoginRespuesta:
    usuario = servicio_usuario.autenticar(payload)
    if usuario is None:
        return LoginRespuesta(ok=False)
    token = servicio_sesion.crear_sesion(usuario)

    return LoginRespuesta(ok=True, usuario_id=usuario.id, token=token)


@router.post("/logout", response_model=LogoutRespuesta)
def logout(
    actual: UsuarioActual,
    authorization: Annotated[str, Header()],
    servicio_sesion: SesionServiceDep
) -> LogoutRespuesta:
    """protegido. No puedes hacer logout si no has hecho login"""
    token = authorization.split(" ")[-1]
    usuario = servicio_sesion.revocar(token)

    return LogoutRespuesta(usuario_id=usuario.id, token_revocado=token)