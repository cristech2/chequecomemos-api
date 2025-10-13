"""Endponit para la gestion de categorias"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.dependencies import get_db
from app.models import CategorieSingleResponse, CategoriesListResponse, CategoryCreate
from app.services import create_category, get_categories, get_category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post(
    "/", response_model=CategorieSingleResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Crea una nueva categoría.

    Args:
        category (CategoryCreate): Datos de la categoría a crear.
        db (Session): Sesión de la base de datos. Defaults to Depends(get_db).

    Returns:
        CategoryDB: La categoría creada.
    """
    category = await create_category(db, category)
    return CategorieSingleResponse(category_id=category.category_id, name=category.name)


@router.get("/{category_id}", response_model=CategorieSingleResponse)
async def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Obtiene una categoría por su ID.

    Args:
        category_id (int): ID de la categoría a obtener.
        db (Session): Sesión de la base de datos. Defaults to Depends(get_db).

    Returns:
        CategoryDB: La categoría encontrada.
    """

    category = await get_category(db, category_id)
    return CategorieSingleResponse(category_id=category.category_id, name=category.name)


@router.get("/", response_model=CategoriesListResponse)
async def get_all_categories(db: Session = Depends(get_db)):  # noqa: B008
    """Obtiene todas las categorías.

    Args:
        db (Session): Sesión de la base de datos. Defaults to Depends(get_db).

    Returns:
        CategoriesListResponse: Lista de categorías encontradas.
    """
    categories = await get_categories(db)
    return CategoriesListResponse(
        categories=[
            CategorieSingleResponse(category_id=cat.category_id, name=cat.name)
            for cat in categories
        ]
    )
