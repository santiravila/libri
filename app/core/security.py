"""Hashing de contraseñas con Argon2id.

Este módulo es el ÚNICO lugar que sabe qué algoritmo usamos. El servicio llama a
`hash_password` / `verify_password` sin conocer argon2. Si mañana cambiamos de
algoritmo o de parámetros, solo se toca este archivo.

Por qué Argon2id:
  - Es deliberadamente LENTO y usa MUCHA memoria, para que un atacante que roba
    la base de datos no pueda probar millones de contraseñas por segundo.
  - Sala (salt) cada contraseña automáticamente: dos usuarios con la misma
    contraseña obtienen hashes distintos. El salt viaja DENTRO del string del hash.
"""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

# Parámetros por defecto de la librería (razonables para 2026). Se pueden subir
# con el tiempo; por eso existe `necesita_rehash`.
_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Devuelve el hash codificado (algoritmo + parámetros + salt + hash en un string)."""
    return _hasher.hash(password)


def verify_password(hash_almacenado: str, password: str) -> bool:
    """True si la contraseña coincide. False si no, o si el hash es inválido.

    `_hasher.verify` devuelve True al coincidir y LANZA excepción si no:
      - VerifyMismatchError: la contraseña no coincide.
      - InvalidHashError:    `hash_almacenado` no es un hash argon2 válido
                             (p. ej. una fila vieja en texto plano como "dragon").
    Las convertimos a un bool para que el servicio no tenga que atrapar nada.
    """
    try:
        return _hasher.verify(hash_almacenado, password)
    except (VerifyMismatchError, InvalidHashError, VerificationError):
        return False


def necesita_rehash(hash_almacenado: str) -> bool:
    """True si el hash se hizo con parámetros más débiles que los actuales.

    Úsalo tras un login exitoso: si devuelve True, vuelve a hashear la contraseña
    (que en ese momento tienes en texto plano) y guarda el nuevo hash. Así migras
    a parámetros más fuertes de forma transparente, sin pedir a nadie que cambie
    su contraseña.
    """
    return _hasher.check_needs_rehash(hash_almacenado)
