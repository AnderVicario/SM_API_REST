# 🔹 app/websocket_manager.py

from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        if username not in self.active_connections:
            self.active_connections[username] = []
        self.active_connections[username].append(websocket)

    def disconnect(self, username: str, websocket: WebSocket):
        if username in self.active_connections:
            self.active_connections[username].remove(websocket)
            if not self.active_connections[username]:
                del self.active_connections[username]

    async def send_personal_message(self, message: str, username: str):
        if username in self.active_connections:
            for websocket in self.active_connections[username]:
                await websocket.send_json(message)

manager = ConnectionManager()