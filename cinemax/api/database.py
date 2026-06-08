# cinemax/api/database.py
"""
Configuración de la conexión a MySQL usando PyMySQL.
Patrón: Repository — separación de acceso a datos.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()


def _get_connection() -> pymysql.Connection:
    """Crea y devuelve una nueva conexión a MySQL usando PyMySQL."""
    ssl_config = None
    ssl_ca = os.getenv("DB_SSL_CA")
    ssl_disabled = os.getenv("DB_SSL_DISABLED", "false").lower() == "true"

    if ssl_ca and not ssl_disabled:
        ssl_config = {"ca": ssl_ca}
    elif not ssl_disabled and os.getenv("DB_HOST", "localhost") not in ("localhost", "127.0.0.1"):
        # Conexiones remotas (Aiven, PlanetScale, etc.) usan SSL por defecto
        ssl_config = {"ssl": True}

    kwargs = dict(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "cinemax"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
    if ssl_config:
        kwargs["ssl"] = ssl_config

    return pymysql.connect(**kwargs)


@contextmanager
def get_connection() -> Generator[pymysql.Connection, None, None]:
    """Context manager que devuelve una conexión y gestiona commit/rollback."""
    conn = _get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
