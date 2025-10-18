"""Modelo de Usuarios: Este módulo define la estructura del modelo para usuarios en la aplicación."""

import uuid

# Importar la base de datos desde la configuración
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    SQLModel,
)


class UserBase(SQLModel):
    """Modelo base para usuarios, utilizado para compartir atributos comunes."""

    # Correo electrónico del usuario. Debe ser único.
    email: EmailStr
    # Nombre completo del usuario.
    full_name: str
    # Nombre de la familia asociada al usuario.
    family_name: str


class Users(UserBase, table=True):
    """
    Representa un usuario de la aplicación.
    Cada usuario tiene identificador, correo, nombre completo, nombre familiar y fechas de creación/actualización.
    """

    # Identificador único del usuario.
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # Correo electrónico del usuario. Debe ser único.
    email: EmailStr = Field(default=None, unique=True, index=True)
    # Nombre completo del usuario.
    full_name: str = Field(default=None)
    # Nombre de la familia asociada al usuario.
    family_name: str = Field(default=None)
    # Contraseña cifrada del usuario.
    hashed_password: str = Field(default=None)
    # Fecha de creación del registro.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # type: ignore  # noqa: UP017
    # Fecha de actualización del registro.
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # type: ignore  # noqa: UP017


class UserCreate(UserBase):
    """Modelo para la creación de un nuevo usuario, incluye la contraseña."""

    # Contraseña del usuario en texto plano (será cifrada antes de almacenar).
    password: str


class UserUpdate(SQLModel):
    """Modelo para la actualización de un usuario, todos los campos son opcionales."""

    # Correo electrónico del usuario. Debe ser único.
    email: EmailStr | None = None
    # Nombre completo del usuario.
    full_name: str | None = None
    # Nombre de la familia asociada al usuario.
    family_name: str | None = None


class UserResponse(UserBase):
    """Modelo para la respuesta de usuario, excluye la contraseña."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
