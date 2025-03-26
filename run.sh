#!/bin/bash

# Activa el entorno virtual
source venv/bin/activate  # Para Linux/macOS
# source venv/Scripts/activate  # Para Windows (Git Bash)

# Ejecuta Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
