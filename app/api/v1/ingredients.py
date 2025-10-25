"""Endpoint API para gestionar ingredientes."""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.dependencies import get_db
from app.models import IngredientCreate, IngredientResponse, IngredientUpdate
from app.services import (
    create_ingredient,
    delete_ingredient,
    get_ingredient,
    update_ingredient,
)

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.post(
    "/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Crea un nuevo ingrediente.

    Args:
        ingredient (IngredientCreate): Datos del ingrediente a crear.
        db (Session): Sesión de la base de datos. Defaults to Depends(get_db).

    Returns:
        IngredientResponse: El ingrediente creado.
    """
    new_ingredient = await create_ingredient(db, ingredient)
    return IngredientResponse(**new_ingredient.model_dump())


@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def read_ingredient(
    ingredient_id: uuid.UUID,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Obtiene un ingrediente por su ID.

    Args:
        ingredient_id (uuid.UUID): ID del ingrediente a obtener.
        db (Session): Sesión de la base de datos. Defaults to Depends(get_db).

    Returns:
        IngredientResponse: El ingrediente encontrado.
    """
    db_ingredient = await get_ingredient(db, ingredient_id)
    return IngredientResponse(**db_ingredient.model_dump())


@router.put("/{ingredient_id}", response_model=IngredientResponse)
async def update_existing_ingredient(
    ingredient_id: uuid.UUID,
    ingredient: IngredientUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Actualiza un ingrediente existente.

    Args:
        ingredient_id (uuid.UUID): ID del ingrediente a actualizar.
        ingredient (IngredientUpdate): Datos del ingrediente a actualizar.
        db (Session): Sesión de la base de datos. Defaults to Depends(get_db).

    Returns:
        IngredientResponse: El ingrediente actualizado.
    """
    db_ingredient = await update_ingredient(db, ingredient_id, ingredient)
    return IngredientResponse(**db_ingredient.model_dump())


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient_by_id(
    ingredient_id: uuid.UUID,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Elimina un ingrediente por su ID.

    Args:
        ingredient_id (uuid.UUID): ID del ingrediente a eliminar.
        db (Session): Sesión de la base de datos. Defaults to Depends(get_db).
    """
    await delete_ingredient(db, ingredient_id)
