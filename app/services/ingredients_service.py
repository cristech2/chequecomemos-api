"""Servicio para ingredientes, maneja la lógica de negocio relacionada con los ingredientes. maneja el crud de ingredientes."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlmodel import select

from app.models import IngredientCreate, Ingredients
from app.models.ingredients import IngredientUpdate


async def create_ingredient(db: Session, ingredient: IngredientCreate) -> Ingredients:
    """Crea un nuevo ingrediente en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        ingredient (IngredientCreate): El ingrediente a crear.

    Returns:
        Ingredients: El ingrediente creado.
    """
    # Verifica si el ingrediente ya existe
    statement = select(Ingredients).where(Ingredients.name == ingredient.name)
    db_ingredient = await db.scalars(statement)
    db_ingredient = db_ingredient.first()
    if db_ingredient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ingrediente con este nombre ya existe.",
        )
    # Crea el ingrediente
    new_ingredient = Ingredients(**ingredient.model_dump())
    db.add(new_ingredient)
    await db.commit()
    await db.refresh(new_ingredient)
    return new_ingredient


async def get_ingredient(db: Session, ingredient_id: uuid.UUID) -> Ingredients:
    """Busca un ingrediente por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        ingredient_id (uuid.UUID): El ID del ingrediente a buscar.

    Returns:
        Ingredients: el ingrediente encontrado.
    """
    # Busca el ingrediente por su ID
    statement = select(Ingredients).where(Ingredients.ingredient_id == ingredient_id)
    db_ingredient = await db.scalars(statement)
    db_ingredient = db_ingredient.first()
    if not db_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado.",
        )
    return db_ingredient


async def update_ingredient(
    db: Session, ingredient_id: uuid.UUID, ingredient: IngredientUpdate
) -> Ingredients:
    """Actualiza un ingrediente existente.

    Args:
        db (Session): La sesión de la base de datos.
        ingredient_id (uuid.UUID): El ID del ingrediente a actualizar.
        ingredient (IngredientCreate): Los nuevos datos del ingrediente.

    Returns:
        Ingredients: El ingrediente actualizado.
    """
    # Busca el ingrediente por su ID
    statement = select(Ingredients).where(Ingredients.ingredient_id == ingredient_id)
    db_ingredient = await db.scalars(statement)
    db_ingredient = db_ingredient.first()
    if not db_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado.",
        )
    # Actualiza los campos del ingrediente
    for key, value in ingredient.model_dump().items():
        setattr(db_ingredient, key, value)
    db.add(db_ingredient)
    await db.commit()
    await db.refresh(db_ingredient)
    return db_ingredient


async def delete_ingredient(db: Session, ingredient_id: uuid.UUID) -> None:
    """Elimina un ingrediente por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        ingredient_id (uuid.UUID): El ID del ingrediente a eliminar.

    Raises:
        HTTPException: Si el ingrediente no existe.
    """
    # Busca el ingrediente por su ID
    statement = select(Ingredients).where(Ingredients.ingredient_id == ingredient_id)
    db_ingredient = await db.scalars(statement)
    db_ingredient = db_ingredient.first()
    if not db_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado.",
        )
    await db.delete(db_ingredient)
    await db.commit()
