from .schema import (
    UsuarioCrear,
    UsuarioRespuesta,
    UsuarioActualizar,
)
from fastapi import APIRouter
from .dependencies import ServiceDep
from ..sesiones.dependencies import UsuarioActual


router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)


@router.post("", response_model=UsuarioRespuesta)
def crear_usuario(
    payload: UsuarioCrear,
    servicio: ServiceDep
) -> UsuarioRespuesta:  
    usuario = servicio.crear_usuario(payload)
    return UsuarioRespuesta.model_validate(usuario)


@router.get("/{user_id}", response_model=UsuarioRespuesta)
def leer_usuario(
    user_id: int,
    servicio: ServiceDep,
    actual: UsuarioActual
) -> UsuarioRespuesta:
    usuario = servicio.leer_usuario(user_id)
    return UsuarioRespuesta.model_validate(usuario)


@router.delete("/{user_id}", response_model=UsuarioRespuesta)
def eliminar_usuario(
    user_id: int,
    servicio: ServiceDep,
    actual: UsuarioActual
) -> UsuarioRespuesta:
    usuario_eliminado = servicio.eliminar_usuario(user_id)
    return UsuarioRespuesta.model_validate(usuario_eliminado)


@router.patch("/{user_id}", response_model=UsuarioRespuesta)
def actualizar_usuario(
    user_id: int,
    payload: UsuarioActualizar,
    servicio: ServiceDep
) -> UsuarioRespuesta:
    usuario_actualizado = servicio.actualizar_usuario(user_id, payload)
    return UsuarioRespuesta.model_validate(usuario_actualizado)