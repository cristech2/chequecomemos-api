"""Modelo para la tabla ingredients y contrato para el cliente y la respuesta del servidor."""

import uuid
from typing import TYPE_CHECKING

from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)

from .categories import Categories, CategorieSingleResponse

if TYPE_CHECKING:
    from app.models.recipe_ingredients import RecipeIngredients


class IngredientsBase(SQLModel):
    """Modelo base para los ingredientes de comida."""

    # Nombre del ingrediente. Debe ser único y no nulo.
    name: str
    category_id: uuid.UUID
    default_unit: str


class Ingredients(IngredientsBase, table=True):
    """Modelo de la tabla ingredients en la base de datos."""

    ingredient_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    category_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, foreign_key="categories.category_id"
    )
    category: "Categories" = Relationship(back_populates="ingredients")
    recipe_ingredients: list["RecipeIngredients"] = Relationship(
        back_populates="ingredient"
    )


class IngredientCreate(IngredientsBase):
    """Contrato para crear un nuevo ingrediente."""

    pass


class IngredientUpdate(SQLModel):
    """
    Modelo para actualizar un ingrediente existente.
    Permite modificar solo el nombre y la unidad por defecto.
    """

    name: str
    default_unit: str


class IngredientResponse(IngredientsBase):
    """
    Modelo de respuesta para mostrar los datos completos de un ingrediente.
    Incluye el id y la relación con la categoría.
    """

    ingredient_id: uuid.UUID
    category: "CategorieSingleResponse"
