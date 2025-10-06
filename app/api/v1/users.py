""" "Endpoints para la gestión de usuarios."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import UserCreate, UserResponse
from app.services import create_user

# Configuración del router
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    """Registra un nuevo usuario.

    Args:
        user (UserCreate): Datos del usuario a registrar.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    """

    return create_user(db, user)
