from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import SesionUsuario
from datetime import datetime

class SesionRepositorio:
    def __init__(
    self,
    session: Session
    ) -> None:
        self.session = session

    def guardar_sesion(self, sesion_usuario: SesionUsuario) -> SesionUsuario:
        self.session.add(sesion_usuario)
        self.session.flush()
        self.session.refresh(sesion_usuario)

        return sesion_usuario

    def leer_sesion(self, token_hash: str) -> SesionUsuario | None:
        sesion = self.session.scalar(
            select(SesionUsuario).where(SesionUsuario.token_hash == token_hash)
        )

        return sesion

