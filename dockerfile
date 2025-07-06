FROM python:3.10-slim

WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias adicionales para testing
RUN pip install pytest pytest-cov requests pyyaml

# Copiar todo el código
COPY . .

# Variables de entorno (puedes sobreescribir en EC2)
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
