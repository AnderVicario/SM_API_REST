# 🔹 schemas.py - Validación con Pydantic
# Define los modelos de entrada/salida.

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    public_key: str

class MessageCreate(BaseModel):
    sender: str
    receiver: str
    encrypted_message: str