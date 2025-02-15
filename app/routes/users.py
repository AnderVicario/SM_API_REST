# 🔹 users.py - Funciones de usuarios
# Define las rutas para el manejo de usuarios.

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.database import get_db

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    new_user = User(username=user.username, public_key=user.public_key)
    db.add(new_user)
    db.commit()
    return {"message": "Usuario registrado exitosamente"}

@router.get("/users/{username}")
def get_public_key(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"public_key": user.public_key}
