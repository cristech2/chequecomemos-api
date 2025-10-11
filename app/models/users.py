"""Modelo de Usuarios: Este módulo define la estructura del modelo para usuarios en la aplicación."""

# Importar la base de datos desde la configuración
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.db import Base


class User(Base):
    """
    Representa un usuario de la aplicación.
    Cada usuario tiene identificador, correo, nombre completo, nombre familiar y fechas de creación/actualización.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Identificador único del usuario.
    email = Column(String, unique=True, index=True)
    # Correo electrónico del usuario. Debe ser único.
    full_name = Column(String)
    # Nombre completo del usuario.
    family_name = Column(String)
    # Nombre de la familia asociada al usuario.
    hashed_password = Column(String)
    # Contraseña cifrada del usuario.
    created_at = Column(DateTime, server_default=func.now())
    # Fecha de creación del registro.
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # Fecha de última actualización del registro.
