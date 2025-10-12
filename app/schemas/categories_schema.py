"""contrato pydantic para categorias.
Define los esquemas para el envio de una categoria por parte del cliente  y la respuesta por parte del servidor
"""

from pydantic import BaseModel, ConfigDict


# Esquema para crear una categoría (solo requiere el nombre)
class CategoryCreate(BaseModel):
    name: str
    # Nombre de la categoría. Debe ser único y no nulo.


# Esquema para la respuesta de una categoría (incluye el ID)
class CategoryOut(CategoryCreate):
    category_id: int
    # Identificador único de la categoría.

    model_config = ConfigDict(from_attributes=True)


# Esquema para la respuesta: lista de categorías
class CategoriesResponse(BaseModel):
    categories: list[CategoryOut]
