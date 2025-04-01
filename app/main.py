# 🔹 main.py - Punto de entrada de FastAPI
# Define la app y carga las rutas.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.database import engine, Base
from app.routes import users, messages

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Mensajería Segura")

# Registrar las rutas
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(messages.router, prefix="/messages", tags=["Mensajes"])

@app.get("/")
def root():
    return {"message": "API de mensajería segura en funcionamiento"}


# 🔹 WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def send_personal_message(self, message: str, username: str):
        websocket = self.active_connections.get(username)
        if websocket:
            await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(username, websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantener la conexión abierta
    except WebSocketDisconnect:
        manager.disconnect(username)