"""dependencia para obtener la sesion de la DB en FastAPI"""

from app.core import async_session


async def get_db():
    """dependencias de FastAPI para obtener la sesion de la DB. Crea y cierra la sesion automaticamente"""
    async with async_session() as db:
        yield db
