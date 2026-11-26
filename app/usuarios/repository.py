from .models import Usuario
from sqlalchemy import select
from sqlalchemy.orm import Session

class UsuarioRepositorio:
    def __init__(
        self,
        session: Session
            ) -> None:
        self.session = session

    def cargar_por_email(self, email: str) -> Usuario | None:
        return self.session.scalar(
            select(Usuario).where(Usuario.email == email)
        )

    def guardar_usuario(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.flush()
        self.session.refresh(usuario)

        return usuario

    def cargar_usuario(self, user_id: int) -> Usuario:
        usuario = self.session.get(Usuario, user_id)
        if usuario is None:
            raise ValueError(f"No existe usuario con id {user_id}")

        return usuario

    def borrar_usuario(self, usuario: Usuario) -> Usuario:
        self.session.delete(usuario)
        return usuario