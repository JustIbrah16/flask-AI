#!/bin/bash
set -e

echo "Iniciando contenedor..."

PORT=${PORT:-5000}

echo "Levantando servidor con Gunicorn en el puerto $PORT"

exec gunicorn main:app \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --worker-class gthread \
    --threads 4 \
    --timeout 120
