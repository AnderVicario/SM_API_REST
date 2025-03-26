# 🔹 models.py - Definición de Tablas
# Define las tablas User y Message.

from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, unique=True, index=True)
    public_key = Column(Text, nullable=False)
    password_hash = Column(String, nullable=False)

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, unique=True)
    sender = Column(String, ForeignKey("users.username"))
    receiver = Column(String, ForeignKey("users.username"))
    encrypted_message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_initial = Column(Boolean, default=False)

    sender_user = relationship("User", foreign_keys=[sender])
    receiver_user = relationship("User", foreign_keys=[receiver])