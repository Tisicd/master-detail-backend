# Master-Detail Backend (Flask + PostgreSQL)

Sistema para la gestión de clientes y direcciones, con validaciones de cédula/RUC, pruebas automatizadas y arquitectura modular.

## 🔧 Tecnologías
- Python 3.10
- Flask
- PostgreSQL
- Docker + Docker Compose
- Pytest + cobertura HTML

## 🚀 Scripts
- `docker-compose up --build`: levantar entorno completo
- `pytest`: ejecutar pruebas
- `report.html`: resultado de pruebas unitarias

## 📦 Estructura
- /models # Lógica de negocio y validaciones
- /controllers # Endpoints Flask
- /tests # Pruebas automatizadas
- /init.sql # Script de inicialización
## ✅ Features
- CRUD completo de clientes y direcciones
- Validaciones de negocio
- Buscador por nombre / documento
- Pruebas automatizadas y reportes
