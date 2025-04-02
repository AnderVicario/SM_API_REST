# 🔹 messages.py - Funciones de mensajes
# Define las rutas para el manejo de mensajes.

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Message
from app.schemas import MessageCreate, MessageResponse
from app.database import get_db
from app.websocket_manager import manager
import uuid
from datetime import datetime, timezone

router = APIRouter()

@router.post("/send_message")
async def send_message(msg: MessageCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un mensaje en la conversación
    existing_message = db.query(Message).filter(
        or_(
            ((Message.sender == msg.sender) & (Message.receiver == msg.receiver)),
            ((Message.sender == msg.receiver) & (Message.receiver == msg.sender))
        )
    ).first()

    new_msg = Message(
        id=str(uuid.uuid4()),
        sender=msg.sender,
        receiver=msg.receiver,
        encrypted_message=msg.encrypted_message,
        timestamp=datetime.now(timezone.utc),
        is_initial=True if existing_message is None else False
    )
    db.add(new_msg)
    db.commit()

    # Notificar al receptor mediante WebSockets
    await manager.send_personal_message(f"{msg.sender}", msg.receiver)

    return {
        "message": "Mensaje enviado",
        "timestamp": new_msg.timestamp,
        "is_initial": new_msg.is_initial
    }

@router.get("/receive_messages/{receiver}", response_model=list[MessageResponse])
def get_messages(receiver: str, db: Session = Depends(get_db)):
    # Obtener todos los mensajes para el receptor
    messages = db.query(Message).filter(Message.receiver == receiver).all()
    
    # Separamos los mensajes iniciales de los no iniciales
    non_initial_messages = [msg for msg in messages if not msg.is_initial]
    
    # Borrar de la base de datos los mensajes que no sean iniciales
    for msg in non_initial_messages:
        db.delete(msg)
    db.commit()
    
    # Devolver únicamente los mensajes iniciales (los que se mantienen)
    return [
        MessageResponse(
            sender=msg.sender,
            encrypted_message=msg.encrypted_message,
            timestamp=msg.timestamp,
            is_initial=msg.is_initial
        )
        for msg in messages
    ]
