"""Servicio de usuarios, maneja la lógica de negocio relacionada con los usuarios."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlmodel import select

from app.core.security import get_hash_password
from app.models import UserCreate
from app.models import Users as UserBD


async def create_user(db: Session, user: UserCreate) -> UserBD:
    """Crea un nuevo usuario en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        user (UserCreate): Los datos del nuevo usuario.

    Returns:
        UserResponse: El usuario creado.
    """
    # Verifica si el usuario ya existe
    statement = select(UserBD).where(UserBD.email == user.email)
    result = await db.execute(statement)
    db_user = result.first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario con este correo ya existe.",
        )

    # hasheamos la contraseña
    hashed_password = get_hash_password(user.password)

    # creamos el usuario
    new_user = UserBD(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        family_name=user.family_name,
    )

    # Agrega el usuario a la sesión y confirma la transacción
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Retorna el usuario creado
    return new_user
