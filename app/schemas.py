# 🔹 schemas.py - Validación con Pydantic
# Define los modelos de entrada/salida.

from pydantic import BaseModel
from datetime import datetime
from typing import Union

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

class UpdateProfilePicture(BaseModel):
    username: str
    password: str
    profile_picture: str

class MessageCreate(BaseModel):
    sender: str
    receiver: str
    encrypted_message: str

class MessageResponse(BaseModel):
    sender: str
    encrypted_message: str
    timestamp: datetime
    is_initial: bool