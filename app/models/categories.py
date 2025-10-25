"""Modelo para la tabla categories y contrato para el cliente y la respuesta del servidor."""

import uuid
from typing import TYPE_CHECKING  # <-- Importar List

from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)

# Para evitar importación circular en la comprobación de tipos
if TYPE_CHECKING:
    from .ingredients import Ingredients


class CategoryCreate(SQLModel):
    """Modelo para la creación de una nueva categoría de comida."""

    # Nombre de la categoría. Debe ser único y no nulo.
    name: str


class CategorieSingleResponse(CategoryCreate):
    """Modelo para la respuesta de una categoría de comida."""

    # Identificador único de la categoría.
    category_id: uuid.UUID


class Categories(CategoryCreate, table=True):
    """
    Representa una categoría de comida en la base de datos.
    Cada categoría tiene un identificador único y un nombre descriptivo.
    """

    # Identificador único de la categoría.
    category_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # Nombre de la categoría. Debe ser único y no nulo.
    name: str = Field(default=None, nullable=False, unique=True)

    ingredients: list["Ingredients"] = Relationship(back_populates="category")


class CategoriesListResponse(SQLModel):
    """Modelo para la respuesta que contiene una lista de categorías."""

    # Respuesta para la lista de categorías.
    categories: list[CategorieSingleResponse]
