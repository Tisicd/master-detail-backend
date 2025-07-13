FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Herramientas de testing
RUN pip install pytest pytest-html pytest-cov requests

COPY . .

# Variables de entorno para pruebas (usadas por dotenv en tus scripts)
ENV PYTHONUNBUFFERED=1

CMD ["pytest", "tests/", "--html=report.html", "--self-contained-html"]
