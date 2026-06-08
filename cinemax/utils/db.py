# cinemax/utils/db.py
"""
Utilidades de acceso directo a MySQL usando PyMySQL.
Usado por app_state.py para login/registro desde el frontend Reflex.
"""

import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    ssl_config = None
    ssl_ca = os.getenv("DB_SSL_CA")
    ssl_disabled = os.getenv("DB_SSL_DISABLED", "false").lower() == "true"

    if ssl_ca and not ssl_disabled:
        ssl_config = {"ca": ssl_ca}
    elif not ssl_disabled and os.getenv("DB_HOST", "localhost") not in ("localhost", "127.0.0.1"):
        ssl_config = {"ssl": True}

    kwargs = dict(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "cinemax"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    if ssl_config:
        kwargs["ssl"] = ssl_config

    return pymysql.connect(**kwargs)


def query(sql: str, params: tuple = ()) -> list:
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
