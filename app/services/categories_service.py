"""Servicio de categorias, maneja la lógica de negocio relacionada con las categorías."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlmodel import select

from app.models import CategoryCreate, CategoryDB


async def create_category(db: Session, category: CategoryCreate) -> CategoryDB:
    """Crea una nueva categoría en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        category (CategoryCreate): La categoría a crear.

    Returns:
        CategoryDB: La categoría creada.
    """
    # Verifica si la categoria ya existe
    statement = select(CategoryDB).where(CategoryDB.name == category.name)
    db_category = await db.scalars(statement)
    db_category = db_category.first()
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría con este nombre ya existe.",
        )
    # Crea la categoría
    new_category = CategoryDB(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


async def get_category(db: Session, category_id: uuid.UUID) -> CategoryDB:
    """Busca una categoria por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        category_id (uuid.UUID): El ID de la categoría a buscar.

    Returns:
        CategoryDB: la categoría encontrada.
    """
    # Busca la categoría por su ID
    statement = select(CategoryDB).where(CategoryDB.category_id == category_id)
    db_category = await db.scalars(statement)
    db_category = db_category.first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada.",
        )
    return db_category


async def get_categories(db: Session) -> list[CategoryDB]:
    """Obtiene todas las categorías de la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list[CategoryDB]: Lista de categorías.
    """
    statement = select(CategoryDB)
    results = await db.scalars(statement)
    categories = list(results.all())
    return categories


async def delete_category(db: Session, category_id: uuid.UUID) -> None:
    """Elimina una categoría por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        category_id (uuid.UUID): El ID de la categoría a eliminar.

    Raises:
        HTTPException: Si la categoría no existe.
    """
    # Busca la categoría por su ID
    statement = select(CategoryDB).where(CategoryDB.category_id == category_id)
    db_category = await db.scalars(statement)
    db_category = db_category.first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada.",
        )
    await db.delete(db_category)
    await db.commit()
