#!/bin/bash

# Activa el entorno virtual
source venv/bin/activate  # Para Linux/macOS
# source venv/Scripts/activate  # Para Windows (Git Bash)

# Ejecuta Uvicorn
uvicorn app.main:app --reload