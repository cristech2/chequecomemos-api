"""Modelo y contratos para las recetas.
Este módulo utiliza SQLModel para definir el modelo de receta en la base de datos. Además, centraliza los modelos Pydantic utilizados como contratos de entrada y salida en la API, facilitando la validación y serialización de datos entre el cliente y el servidor."""

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING  # <-- Importar List

from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)

# evitar importación circular en la comprobación de tipos
if TYPE_CHECKING:
    from .recipe_ingredients import ListRecipeIngredientsRead, RecipeIngredients
    from .users import Users


class RecipeVisibility(str, Enum):
    """Enum para la visibilidad de las recetas."""

    PUBLIC = "public"
    PRIVATE = "private"


class RecipesBase(SQLModel):
    """Modelo base para las recetas."""

    name: str
    description: str
    instructions: str | None = None
    prep_time: int | None = None  # en minutos
    servings: int | None = None  # n de porciones, por defecto 1
    visibility: RecipeVisibility  # 'public' o 'private', por defecto 'public'


class Recipes(RecipesBase, table=True):
    """Modelo de tabla para las recetas."""

    __tablename__: str = "recipes"  # type: ignore
    recipe_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="users.id")
    servings: int | None = Field(default=1)
    visibility: RecipeVisibility = Field(default=RecipeVisibility.PUBLIC)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))  # type: ignore  # noqa: UP017
    update_at: datetime = Field(default_factory=datetime.now(timezone.utc))  # type: ignore  # noqa: UP017

    owner: "Users" = Relationship(back_populates="recipes")
    recipe_ingredients: list["RecipeIngredients"] = Relationship(
        back_populates="recipe"
    )


class RecipesCreate(RecipesBase):
    """Contrato para crear una receta."""

    pass


class RecipesUpdate(SQLModel):
    """Contrato para actualizar una receta."""

    recipe_id: uuid.UUID
    name: str | None = None
    description: str | None = None
    instructions: str | None = None
    prep_time: int | None = None  # en minutos
    servings: int | None = None  # n de porciones
    visibility: RecipeVisibility | None = None  # 'public' o 'private'


class RecipesResponse(RecipesBase):
    """Contrato de respuesta para una receta."""

    recipe_id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    update_at: datetime
    recipe_ingredients: "ListRecipeIngredientsRead"
