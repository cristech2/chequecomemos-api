"""Modelo para la tabla categories"""

from sqlalchemy import Column, Integer, String

from app.core.db import Base


class Category(Base):
    """
    Representa una categoría de comida en la base de datos.
    Cada categoría tiene un identificador único y un nombre descriptivo.
    """

    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    # Identificador único de la categoría.
    name = Column(String, nullable=False, unique=True)
    # Nombre de la categoría. Debe ser único y no nulo.
