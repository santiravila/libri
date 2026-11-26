from ..infra.database import DBSession
from ..usuarios.models import Usuario
from ..usuarios.dependencies import ServiceDep as ServicioUsuarioDep 
from .repository import SesionRepositorio
from .service import SesionServicio
from fastapi import Depends, Header, HTTPException, status
from typing import Annotated


def get_service_dependency(session: DBSession):
    repo = SesionRepositorio(session)
    return SesionServicio(repo, session)

ServiceDep = Annotated[SesionServicio, Depends(get_service_dependency)]


def usuario_actual(
    servicio_sesion: ServiceDep,
    servicio_usuario: ServicioUsuarioDep,
    authorization: Annotated[str | None, Header()] = None # cambiar por HTTPBearer mas adelante
) -> Usuario:
    """
    lee el header the la peticion http en busca del auth bearer (token)
    usa el servicio de sesion para validar el token
    devuelve Usuario si el usuario existe y el token coincide. Lanza 401 Unauthorized de lo contrario
    """
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    scheme, _, token = authorization.partition(" ")

    if scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        usuario_id = servicio_sesion.validar_token(token)
        usuario = servicio_usuario.leer_usuario(usuario_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    
    return usuario

UsuarioActual = Annotated[Usuario, Depends(usuario_actual)]



