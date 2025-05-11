
import psycopg2
from psycopg2 import sql, OperationalError
from sqlalchemy import create_engine

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    USERNAME,
    PASSWORD,
    DB_URL,

)

def create_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,      
            port=DB_PORT,                      
            database=DB_NAME,
            user=USERNAME,
            password=PASSWORD,
            sslmode="disable"                  
        )
        print("[OK] -- Connection successful")
        return conn
    except OperationalError as e:
        print(f"[FAILED] -- Connection failed: {e}")
        return None

def close_connection(conn):
    if conn:
        conn.close()
        print("[OK] -- Connection closed")

def get_engine():
    try:
        engine = create_engine(DB_URL)
        return engine
    
    except Exception as e:
        return None
