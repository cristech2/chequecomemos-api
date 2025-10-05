""" "Este modulo define la conexion a la base de datos y la configuración del ORM."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()  # Cargar variables de entorno desde un archivo .env


# definimos la ubicacion de la DB
DATABASE_URL = os.getenv("DATABASE_URL")
# Verificamos que la variable de entorno esté definida
if DATABASE_URL is None:
    raise RuntimeError("La variable de entorno DATABASE_URL no está definida.")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# creamos la sesion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# creamos la clase base para los modelos
class Base(DeclarativeBase):
    pass
