#!/bin/sh
# Espera hasta que la base de datos esté lista

echo "Esperando a que la base de datos esté disponible..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "Base de datos disponible. Ejecutando pruebas..."
pytest tests/ --html=report.html --self-contained-html
