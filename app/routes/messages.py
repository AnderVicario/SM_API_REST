# 🔹 messages.py - Funciones de mensajes
# Define las rutas para el manejo de mensajes.

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Message
from app.schemas import MessageCreate
from app.database import get_db
import uuid

router = APIRouter()

@router.post("/send_message")
def send_message(msg: MessageCreate, db: Session = Depends(get_db)):
    new_msg = Message(
        id=str(uuid.uuid4()),
        sender=msg.sender,
        receiver=msg.receiver,
        encrypted_message=msg.encrypted_message
    )
    db.add(new_msg)
    db.commit()
    return {"message": "Mensaje enviado"}

@router.get("/messages/{receiver}")
def get_messages(receiver: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.receiver == receiver).all()
    return [{"sender": msg.sender, "encrypted_message": msg.encrypted_message} for msg in messages]
