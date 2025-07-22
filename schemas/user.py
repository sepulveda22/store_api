# Define los esqumas Pydantic para validar datos de entrada y salida.
from pydantic import BaseModel, EmailStr

# Esquema base con campos comunes.
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Extiende UserBase incluir la contrasenia al crear un usuario.
class UserCreate(UserBase):
    password: str
    
# Esquema para devolver datos del usuario, incluyendo el ID.
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True # Permite convertir objetos SQLAlchemy a Pydantic.

# Esquema para la respuesta del token.
class Token(BaseModel):
    access_token: str
    token_type: str