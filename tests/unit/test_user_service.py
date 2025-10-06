from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.users import User
from app.schemas.user_schema import UserCreate
from app.services import user_service


@pytest.fixture
def fake_db():
    """Fixture para simular la base de datos.

    Returns:
        MagicMock: Un objeto MagicMock que simula la base de datos.
    """
    return MagicMock()


@pytest.fixture
def user_create_data():
    """Fixture para proporcionar datos de creación de usuario.

    Returns:
        UserCreate: Un objeto UserCreate con datos de creación de usuario.
    """
    from app.schemas.user_schema import UserCreate

    return UserCreate(
        email="test@example.com",
        password="password",  # nosec
        full_name="cristian rosales",
        family_name="rosales",
    )


def test_create_user_success(
    fake_db: MagicMock, user_create_data: UserCreate, monkeypatch
):
    """Prueba la creación de un usuario exitoso.

    Args:
        fake_db (MagicMock): Simulación de la base de datos.
        user_create_data (UserCreate): Datos de creación del usuario.
        monkeypatch (MonkeyPatch): Herramienta para modificar el comportamiento de las funciones.
    """
    fake_db.query().filter().first.return_value = None
    monkeypatch.setattr(user_service, "get_hash_password", lambda pwd: "hashed")
    # No es necesario mockear add/commit/refresh para este test
    # Aseguramos que user_create_data es UserCreate
    from app.schemas.user_schema import UserCreate

    if isinstance(user_create_data, dict):
        user_create_data = UserCreate(**user_create_data)
    result = user_service.create_user(fake_db, user_create_data)
    # Comprobamos que el email es el esperado
    assert hasattr(result, "email")  # nosec
    assert str(result.email) == user_create_data.email  # nosec


def test_create_user_already_exists(fake_db: MagicMock, user_create_data: UserCreate):
    """Prueba la creación de un usuario que ya existe.

    Args:
        fake_db (MagicMock): Simulación de la base de datos.
        user_create_data (UserCreate): Datos de creación del usuario.
    """
    fake_db.query().filter().first.return_value = User(
        email=user_create_data.email,
        full_name=user_create_data.full_name,
        family_name=user_create_data.family_name,
        hashed_password="hashed",  # nosec
    )
    with pytest.raises(HTTPException) as exc:
        user_service.create_user(fake_db, user_create_data)
    assert exc.value.status_code == 400  # nosec
    assert "ya existe" in exc.value.detail  # nosec
