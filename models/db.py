import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables desde .env solo en desarrollo
load_dotenv(dotenv_path=os.getenv("ENV_FILE", ".env"))

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL no está definida. Verifica tu entorno.")

    return psycopg2.connect(database_url)
