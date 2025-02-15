# 🔹 models.py - Definición de Tablas
# Define las tablas User y Message.

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, unique=True, index=True)
    public_key = Column(Text, nullable=False)

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, unique=True)
    sender = Column(String, ForeignKey("users.username"))
    receiver = Column(String, ForeignKey("users.username"))
    encrypted_message = Column(Text, nullable=False)

    sender_user = relationship("User", foreign_keys=[sender])
    receiver_user = relationship("User", foreign_keys=[receiver])