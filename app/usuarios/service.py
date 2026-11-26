from .schema import UsuarioCrear, UsuarioActualizar, UsuarioLogin
from .models import Usuario
from .repository import UsuarioRepositorio
from ..core.security import hash_password, verify_password
from sqlalchemy.orm import Session


class UsuarioServicio:
    def __init__(
            self, 
            repo: UsuarioRepositorio, 
            session: Session
        ) -> None:
        self.repo = repo #proteger
        self.session = session

    def crear_usuario(self, payload: UsuarioCrear) -> Usuario:
        nuevo_usuario = Usuario(
            nombre = payload.nombre,
            email = payload.email,
            password_hash = hash_password(payload.password),
        )

        usuario_db = self.repo.guardar_usuario(nuevo_usuario)
        self.session.commit()
        return usuario_db

    def autenticar(self, payload: UsuarioLogin) -> Usuario | None:
        usuario = self.repo.cargar_por_email(payload.email)
        if usuario is None or not usuario.activo:
            return None
        if not verify_password(usuario.password_hash, payload.password):
            return None
        return usuario


    def leer_usuario(self, user_id: int):
        usuario_db = self.repo.cargar_usuario(user_id=user_id)
        return usuario_db


    def eliminar_usuario(self, user_id: int):
        usuario = self.leer_usuario(user_id=user_id)
        usuario_db = self.repo.borrar_usuario(usuario)
        self.session.commit()
        return usuario_db


    def actualizar_usuario(self, user_id: int, payload: UsuarioActualizar):
        update_fields = payload.model_dump(exclude_unset=True)
        usuario = self.leer_usuario(user_id=user_id)

        for key, value in update_fields.items():
            setattr(usuario, key, value)

        self.session.commit()
        return usuario
