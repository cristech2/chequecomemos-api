"""Servicio de usuarios, maneja la lógica de negocio relacionada con los usuarios."""

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlmodel import select

from app.core.security import get_hash_password
from app.models import UserCreate, UserUpdate
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
    db_user = await db.scalars(statement)
    db_user = db_user.first()
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


async def get_user_by_email(db: Session, email: EmailStr) -> UserBD:
    """Obtiene un usuario por su correo electrónico.

    Args:
        db (Session): La sesión de la base de datos.
        email (EmailStr): El correo electrónico del usuario.

    Returns:
        UserResponse: El usuario encontrado o None si no existe.
    """
    statement = select(UserBD).where(UserBD.email == email)
    result = await db.scalars(statement)
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )
    return user


async def update_user(db: Session, email: EmailStr, user_update: UserUpdate) -> UserBD:
    """Actualiza los datos de un usuario existente.

    Args:
        db (Session): La sesión de la base de datos.
        email (EmailStr): El correo electrónico del usuario a actualizar.
        user_update (UserUpdate): Los datos a actualizar.

    Returns:
        UserResponse: El usuario actualizado.
    """
    # Busca el usuario por su correo electrónico
    statement = select(UserBD).where(UserBD.email == email)
    result = await db.scalars(statement)
    db_user = result.first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    # Actualiza los campos proporcionados
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.full_name is not None:
        db_user.full_name = user_update.full_name
    if user_update.family_name is not None:
        db_user.family_name = user_update.family_name

    # Confirma la transacción
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el usuario.",
        ) from e

    return db_user
