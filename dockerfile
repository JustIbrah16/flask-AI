# Imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# definir tu archivo principal de flask
ENV FLASK_APP=app.py  

# puerto expuesto
EXPOSE 5000

# comando que usas normalmente
CMD ["flask", "run", "--host=0.0.0.0"]










