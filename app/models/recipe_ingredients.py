"""
Modelo y contratos para la relación muchos a muchos entre recetas e ingredientes.

Este módulo utiliza SQLModel para definir la tabla intermedia en la base de datos, permitiendo gestionar la relación entre recetas e ingredientes. Además, centraliza los modelos Pydantic utilizados como contratos de entrada y salida en la API, facilitando la validación y serialización de datos entre el cliente y el servidor."""

import uuid
from typing import TYPE_CHECKING  # <-- Importar List

from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)

from .ingredients import IngredientResponse

# Para evitar importación circular en la comprobación de tiposx`x`
if TYPE_CHECKING:
    from .ingredients import Ingredients
    from .recipes import Recipes


class RecipeIngredientsBase(SQLModel):
    """Modelo base para la relación entre recetas e ingredientes."""

    quantity: float
    optional: bool


class RecipeIngredients(RecipeIngredientsBase, table=True):
    """Modelo de tabla para la relación entre recetas e ingredientes."""

    __tablename__: str = "recipe_ingredients"  # type: ignore
    recipe_ingredient_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True
    )
    recipe_id: uuid.UUID = Field(foreign_key="recipes.recipe_id")
    ingredient_id: uuid.UUID = Field(foreign_key="ingredients.ingredient_id")

    ingredient: "Ingredients" = Relationship(back_populates="recipe_ingredients")
    recipe: "Recipes" = Relationship(back_populates="recipe_ingredients")


class RecipeIngredientsCreate(RecipeIngredientsBase):
    """Modelo para crear una nueva relación entre receta e ingrediente."""

    recipe_id: uuid.UUID
    ingredient_id: uuid.UUID


class RecipeIngredientsUpdate(SQLModel):
    """Modelo para actualizar una relación entre receta e ingrediente."""

    recipe_ingredient_id: uuid.UUID
    quantity: float | None = None
    optional: bool | None = None


class RecipeIngredientsResponse(RecipeIngredientsBase):
    """Contrato de respuesta para la relación entre recetas e ingredientes. permite incluir detalles del ingrediente."""

    ingredient: IngredientResponse
