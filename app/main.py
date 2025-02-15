# 🔹 main.py - Punto de entrada de FastAPI
# Define la app y carga las rutas.

from fastapi import FastAPI
from database import engine, Base
from routes import users, messages

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Mensajería Segura")

# Registrar las rutas
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(messages.router, prefix="/messages", tags=["Mensajes"])

@app.get("/")
def root():
    return {"message": "API de mensajería segura en funcionamiento"}
