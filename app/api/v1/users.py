""" "Endpoints para la gestión de usuarios."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.dependencies import get_db
from app.models import UserCreate, UserResponse
from app.services import create_user

# Configuración del router
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    """Registra un nuevo usuario.

    Args:
        user (UserCreate): Datos del usuario a registrar.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    """

    return await create_user(db, user)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):  # noqa: B008
    """Obtiene los detalles de un usuario por su ID.

    Args:
        user_id (int): ID del usuario a obtener.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    """
    # placeholder de implementacion
    return {"id": user_id, "username": "testuser", "email": "testuser@example.com"}
