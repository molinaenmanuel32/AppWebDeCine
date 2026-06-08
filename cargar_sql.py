#!/usr/bin/env python3
"""
cargar_sql.py
Crea las tablas necesarias en la base de datos MySQL y carga datos de ejemplo.

Uso:
    python cargar_sql.py

Requiere las variables en .env:
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

load_dotenv()

DDL = """
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS movies (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    genre           VARCHAR(100),
    duration        INT,
    classification  VARCHAR(20),
    director        VARCHAR(255),
    release_date    DATE,
    poster_url      VARCHAR(500),
    trailer_url     VARCHAR(500),
    price           DECIMAL(10,2) DEFAULT 0.00,
    active          TINYINT(1) NOT NULL DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS reservations (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    movie_id    INT NOT NULL,
    seat        VARCHAR(10) NOT NULL,
    showtime    VARCHAR(20) NOT NULL,
    code        VARCHAR(20) NOT NULL UNIQUE,
    status      ENUM('confirmed', 'used', 'expired', 'cancelled') DEFAULT 'confirmed',
    total       DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def get_connection():
    ssl_ca = os.getenv("DB_SSL_CA")
    ssl_disabled = os.getenv("DB_SSL_DISABLED", "false").lower() == "true"
    kwargs = dict(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "cinemax"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    if ssl_ca and not ssl_disabled:
        kwargs["ssl"] = {"ca": ssl_ca}
    elif not ssl_disabled and kwargs["host"] not in ("localhost", "127.0.0.1"):
        kwargs["ssl"] = {"ssl": True}
    return pymysql.connect(**kwargs)


def run():
    print("Conectando a la base de datos...")
    try:
        conn = get_connection()
    except Exception as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)

    print("Creando tablas...")
    with conn.cursor() as cursor:
        for statement in DDL.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
    conn.commit()
    print("✓ Tablas creadas: users, movies, reservations")

    # Crear usuario admin por defecto si no existe
    import bcrypt
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE email = 'admin@cinemax.com'")
        if not cursor.fetchone():
            hashed = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'admin')",
                ("Administrador", "admin@cinemax.com", hashed)
            )
            conn.commit()
            print("✓ Usuario admin creado: admin@cinemax.com / admin123")
        else:
            print("  Admin ya existe, omitiendo")

    conn.close()
    print("\nBase de datos lista.")


if __name__ == "__main__":
    run()
