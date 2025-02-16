# 🔹 schemas.py - Validación con Pydantic
# Define los modelos de entrada/salida.

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    public_key: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UpdatePublicKey(BaseModel):
    username: str
    password: str
    new_public_key: str

class MessageCreate(BaseModel):
    sender: str
    receiver: str
    encrypted_message: str