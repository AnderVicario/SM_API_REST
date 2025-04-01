# 🔹 main.py - Punto de entrada de FastAPI
# Define la app y carga las rutas.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.database import engine, Base
from app.routes import users, messages
from app.websocket_manager import manager  # Importa el manager aquí

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Mensajería Segura")

# Registrar las rutas
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(messages.router, prefix="/messages", tags=["Mensajes"])

@app.get("/")
def root():
    return {"message": "API de mensajería segura en funcionamiento"}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(username, websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantener la conexión abierta
    except WebSocketDisconnect:
        manager.disconnect(username)