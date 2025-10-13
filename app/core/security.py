"""Modulo de seguridad utilizando passlib para hashear contraseñas"""

import bcrypt


def get_hash_password(password: str) -> str:
    """
    Hashea una contraseña utilizando bcrypt.

    args:
    password (str) -- La contraseña en texto plano a hashear.

    Return: La contraseña hasheada.
    """
    # Codifica la contraseña a bytes y genera un salt
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con una contraseña hasheada.

    args:
    plain_password (str) -- La contraseña en texto plano a verificar.
    hashed_password (str) -- La contraseña hasheada contra la que se verifica.

    Return: True si las contraseñas coinciden, False en caso contrario.
    """
    # Codifica ambos a bytes para la verificación
    plain_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_bytes, hashed_bytes)
