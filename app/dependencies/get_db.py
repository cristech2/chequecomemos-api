"""dependencia para obtener la sesion de la DB en FastAPI"""

from app.core import SessionLocal


def get_db():
    """dependencias de FastAPI para obtener la sesion de la DB. Crea y cierra la sesion automaticamente"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
