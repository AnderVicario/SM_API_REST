# 🔹 users.py - Funciones de usuarios
# Define las rutas para el manejo de usuarios.

import base64
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserLogin, UpdatePublicKey, UpdateProfilePicture
from app.database import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    # Hashear la contraseña del usuario
    hashed_password = pwd_context.hash(user.password)

    # Crear el usuario con el hash de la contraseña
    new_user = User(username=user.username, public_key=user.public_key, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "Usuario registrado exitosamente"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # Verificar la contraseña
    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    return {"message": "Login exitoso"}

@router.get("/get_key/{username}")
def get_public_key(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"public_key": user.public_key}

@router.put("/update_key")
def update_public_key(data: UpdatePublicKey, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == data.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que la contraseña sea correcta
    if not pwd_context.verify(data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    # Actualizar la clave pública
    db_user.public_key = data.new_public_key
    db.commit()
    return {"message": "Clave pública actualizada exitosamente"}

@router.put("/update_profile_picture")
def update_profile_picture(data: UpdateProfilePicture, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == data.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar contraseña
    if not pwd_context.verify(data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    # Decodificar y validar Base64
    try:
        if data.profile_picture:
            db_user.profile_picture = base64.b64decode(data.profile_picture)
    except Exception:
        raise HTTPException(status_code=400, detail="Imagen en Base64 no válida")

    db.commit()
    return {"message": "Foto de perfil actualizada exitosamente"}