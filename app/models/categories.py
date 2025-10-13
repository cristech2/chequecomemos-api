"""Modelo para la tabla categories y contrato para el cliente y la respuesta del servidor."""

from sqlmodel import Field, SQLModel  # pyright: ignore[reportUnknownVariableType]


class CategoryCreate(SQLModel):
    """Modelo para la creación de una nueva categoría de comida."""

    # Nombre de la categoría. Debe ser único y no nulo.
    name: str


class CategorieSingleResponse(CategoryCreate):
    """Modelo para la respuesta de una categoría de comida."""

    # Identificador único de la categoría.
    category_id: int


class Categories(CategoryCreate, table=True):
    """
    Representa una categoría de comida en la base de datos.
    Cada categoría tiene un identificador único y un nombre descriptivo.
    """

    # Identificador único de la categoría.
    category_id: int = Field(default=None, primary_key=True)
    # Nombre de la categoría. Debe ser único y no nulo.
    name: str = Field(default=None, nullable=False, unique=True)


class CategoriesListResponse(SQLModel):
    """Modelo para la respuesta que contiene una lista de categorías."""

    # Respuesta para la lista de categorías.
    categories: list[CategorieSingleResponse]
