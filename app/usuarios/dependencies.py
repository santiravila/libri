from ..infra.database import DBSession
from .repository import UsuarioRepositorio
from .service import UsuarioServicio
from fastapi import Depends
from typing import Annotated


def get_service_dependency(session: DBSession):
    repo = UsuarioRepositorio(session)
    return UsuarioServicio(repo, session)

ServiceDep = Annotated[UsuarioServicio, Depends(get_service_dependency)]

