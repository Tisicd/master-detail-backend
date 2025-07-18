import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.getenv("ENV_FILE", ".env"))

def get_db_connection():
    print("DB_HOST:", os.getenv("DB_HOST"))  # ⬅️ Esto debe imprimir 181.199.54.170
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
