from .repository import SesionRepositorio
from .models import SesionUsuario
from ..usuarios.models import Usuario

from sqlalchemy.orm import Session
from secrets import token_hex
import hashlib
from  datetime import datetime


class SesionServicio:
    def __init__(
    self,
    repo: SesionRepositorio,
    session: Session
    ) -> None:
        self.repo = repo
        self.session = session

    def crear_sesion(self, usuario: Usuario):
        """
        admite un Usuario con datos de login. 
        - genera token crudo y calcula su hash con SHA-256.
        - Crea el objeto de SesionUsuario, usa el repo para persistir
        - devuelve el token crudo
        """
        token_crudo = token_hex(32)
        token_hash = hashlib.sha256(token_crudo.encode(encoding="utf-8")).hexdigest()
        sesion_usuario = SesionUsuario(
            token_hash=token_hash,
            id_usuario=usuario.id
        )
        self.repo.guardar_sesion(sesion_usuario)
        self.session.commit()
        return token_crudo

    def validar_token(self, token_crudo: str) -> int:
        token_hash = hashlib.sha256(token_crudo.encode(encoding="utf-8")).hexdigest()
        sesion = self.repo.leer_sesion(token_hash=token_hash)
        if sesion is None or sesion.revocada_en is not None:
            raise ValueError

        return sesion.id_usuario

    def revocar(self, token_crudo: str) -> SesionUsuario:
        token_hash = hashlib.sha256(token_crudo.encode(encoding="utf-8")).hexdigest()
        sesion = self.repo.leer_sesion(token_hash=token_hash)
        if sesion is None:
            raise ValueError

        sesion.revocada_en = datetime.now()
        
        self.session.commit()
        return sesion