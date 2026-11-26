from fastapi import APIRouter
from ..usuarios.models import Usuario
from ..usuarios.schema import UsuarioLogin
from ..usuarios.dependencies import ServiceDep as UsuarioServiceDep
from .schema import LoginRespuesta
from .dependencies import ServiceDep as SesionServiceDep

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
