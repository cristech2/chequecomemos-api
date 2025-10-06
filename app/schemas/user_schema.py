""" "Contrato pydantic para usuarios.
Define los esquemas para el envio de un usuario por parte del cliente  y la respuesta por parte del sevidor
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

# Esquema base para un usuario


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    family_name: str


# Esquema para la creación de un usuario
class UserCreate(UserBase):
    password: str


# Esquema para la respuesta del usuario (sin la contraseña)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
