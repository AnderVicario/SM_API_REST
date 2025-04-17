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

    timestamp=timestamp = datetime.now().replace(microsecond=0)

    if existing_message is None:
        new_msg = Message(
            id=str(uuid.uuid4()),
            sender=msg.sender,
            receiver=msg.receiver,
            encrypted_message="Hola! Quiero hablar contigo.",
            timestamp=timestamp,
            is_initial=True
        )
        db.add(new_msg)
        db.commit()

    new_msg = Message(
        id=str(uuid.uuid4()),
        sender=msg.sender,
        receiver=msg.receiver,
        encrypted_message=msg.encrypted_message,
        timestamp=timestamp,
        is_initial=False
    )
    db.add(new_msg)
    db.commit()

    # Notificar tanto al receptor como al emisor
    await manager.send_personal_message(
        {"type": "new_message", "sender": msg.sender, "is_yourself": False},
        msg.receiver
    )

    await manager.send_personal_message(
        {"type": "new_message", "sender": msg.sender, "is_yourself": True},
        msg.sender
    )

    return {
        "message": "Mensaje enviado",
        "timestamp": timestamp,
        "is_initial": new_msg.is_initial
    }

@router.get("/receive_messages/{receiver}", response_model=list[MessageResponse])
def get_messages(receiver: str, db: Session = Depends(get_db)):
    # Obtener todos los mensajes relacionados con el usuario (tanto enviados como recibidos)
    messages = db.query(Message).filter(
        or_(
            Message.receiver == receiver,
            Message.sender == receiver
        )
    ).order_by(Message.timestamp).all()
    
    return [
        MessageResponse(
            sender=msg.sender,
            receiver=msg.receiver,
            encrypted_message=msg.encrypted_message,
            timestamp=msg.timestamp,
            is_initial=msg.is_initial
        )
        for msg in messages
    ]
