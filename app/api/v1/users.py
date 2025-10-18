""" "Endpoints para la gestión de usuarios."""

from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.dependencies import get_db
from app.models import UserCreate, UserResponse, UserUpdate
from app.services import create_user, get_user_by_email, update_user

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


@router.get(
    "/{user_email}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def get_user(user_email: EmailStr, db: Session = Depends(get_db)):  # noqa: B008
    """Obtiene los detalles de un usuario por su email.

    Args:
        user_email (EmailStr): Email del usuario a obtener.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    """
    return await get_user_by_email(db, user_email)


@router.put(
    "/{user_email}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user_by_email(
    user_email: EmailStr,
    user_update: UserUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Modifica los detalles de un usuario existente.

    Args:
        user_email (EmailStr): Email del usuario a modificar.
        user_update (UserUpdate): Datos actualizados del usuario.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    """
    return await update_user(db, user_email, user_update)
