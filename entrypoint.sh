#!/bin/bash
set -e

echo "Iniciando contenedor..."

# Asegurar que el puerto de Railway esté disponible
PORT=${PORT:-5000}

echo "Levantando servidor con Gunicorn en el puerto $PORT"

exec gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --worker-class gevent \
    --timeout 120
