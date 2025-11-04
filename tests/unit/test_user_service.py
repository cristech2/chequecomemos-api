from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.users import UserCreate, Users
from app.services import user_service


@pytest.fixture
def fake_db():
    """Fixture para simular la base de datos asíncrona.

    Returns:
        AsyncMock: Un objeto AsyncMock que simula la base de datos asíncrona.
    """
    return AsyncMock()


@pytest.fixture
def user_create_data():
    """Fixture para proporcionar datos de creación de usuario.

    Returns:
        UserCreate: Un objeto UserCreate con datos de creación de usuario.
    """
    from app.models.users import UserCreate

    return UserCreate(
        email="test@example.com",
        password="password",  # nosec
        full_name="cristian rosales",
        family_name="rosales",
    )


@pytest.mark.asyncio
async def test_create_user_success(
    fake_db: AsyncMock, user_create_data: UserCreate, monkeypatch: pytest.MonkeyPatch
):
    """Prueba la creación de un usuario exitoso.

    Args:
        fake_db (MagicMock): Simulación de la base de datos.
        user_create_data (UserCreate): Datos de creación del usuario.
        monkeypatch (MonkeyPatch): Herramienta para modificar el comportamiento de las funciones.
    """
    mock_result = MagicMock()
    mock_result.first.return_value = None
    fake_db.scalars.return_value = mock_result
    monkeypatch.setattr(user_service, "get_hash_password", lambda pwd: "hashed")

    # --- INICIO DE LA SOLUCIÓN ---
    # Sobreescribe 'add' para que sea un mock síncrono y evitar el RuntimeWarning
    fake_db.add = MagicMock()
    # --- FIN DE LA SOLUCIÓN ---

    # Aseguramos que user_create_data es UserCreate
    from app.models.users import UserCreate

    if isinstance(user_create_data, dict):
        user_create_data = UserCreate(**user_create_data)

    result = await user_service.create_user(fake_db, user_create_data)

    # Comprobamos que el email es el esperado
    assert hasattr(result, "email")  # nosec
    assert str(result.email) == user_create_data.email  # nosec


@pytest.mark.asyncio
async def test_create_user_already_exists(
    fake_db: AsyncMock, user_create_data: UserCreate
):
    """Prueba la creación de un usuario que ya existe.

    Args:
        fake_db (MagicMock): Simulación de la base de datos.
        user_create_data (UserCreate): Datos de creación del usuario.
    """
    mock_result = MagicMock()
    mock_result.first.return_value = Users(
        email=user_create_data.email,
        full_name=user_create_data.full_name,
        family_name=user_create_data.family_name,
        hashed_password="hashed",  # nosec
    )
    fake_db.scalars.return_value = mock_result
    with pytest.raises(HTTPException) as exc:
        await user_service.create_user(fake_db, user_create_data)
    assert exc.value.status_code == 400  # nosec
    assert "ya existe" in exc.value.detail  # nosec
