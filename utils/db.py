import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl": True},
    )

def query(sql: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()

def execute(sql: str, params: tuple = ()) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()

def call_proc(name: str, args: list):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc(name, args)
            conn.commit()
            result = args
            return {
                "reserva_id": result[-2],
                "mensaje": result[-1]
            }
    finally:
        conn.close()