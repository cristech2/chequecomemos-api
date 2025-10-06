"""Modulo de seguridad utilizando passlib para hashear contraseñas"""

from passlib.context import CryptContext

# Configuración del contexto de hashing de contraseñas
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    """
    Hashea una contraseña utilizando bcrypt.

    args:
    password (str) -- La contraseña en texto plano a hashear.

    Return: La contraseña hasheada.
    """

    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con una contraseña hasheada.

    args:
    plain_password (str) -- La contraseña en texto plano a verificar.
    hashed_password (str) -- La contraseña hasheada contra la que se verifica.

    Return: True si las contraseñas coinciden, False en caso contrario.
    """
    return password_context.verify(plain_password, hashed_password)
