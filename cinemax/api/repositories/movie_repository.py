# cinemax/api/repositories/movie_repository.py
"""
Repositorio de Películas — patrón Repository.
Solo acceso a datos MySQL (PyMySQL), sin lógica de negocio.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..database import get_connection


class MovieRepository:
    """CRUD sobre la tabla `movies`."""

    # ── Read ──────────────────────────────────────────────────────────────────
    def find_all(self, active_only: bool = False) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM movies"
        if active_only:
            sql += " WHERE active = 1"
        sql += " ORDER BY created_at DESC"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    def find_by_id(self, movie_id: int) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
                return cursor.fetchone()

    def count_active(self) -> int:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as c FROM movies WHERE active = 1")
                row = cursor.fetchone()
                return row["c"] if row else 0

    def count_total(self) -> int:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as c FROM movies")
                row = cursor.fetchone()
                return row["c"] if row else 0

    def find_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM movies ORDER BY created_at DESC LIMIT %s", (limit,)
                )
                return cursor.fetchall()

    # ── Create ────────────────────────────────────────────────────────────────
    def create(self, data: Dict[str, Any]) -> int:
        sql = """
            INSERT INTO movies
              (title, description, genre, duration, classification,
               director, release_date, poster_url, trailer_url, price, active)
            VALUES
              (%(title)s, %(description)s, %(genre)s, %(duration)s,
               %(classification)s, %(director)s, %(release_date)s,
               %(poster_url)s, %(trailer_url)s, %(price)s, %(active)s)
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                return cursor.lastrowid

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self, movie_id: int, data: Dict[str, Any]) -> bool:
        if not data:
            return False
        fields = ", ".join(f"{k} = %s" for k in data.keys())
        values = list(data.values()) + [movie_id]
        sql = f"UPDATE movies SET {fields} WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                return cursor.rowcount > 0

    # ── Delete ────────────────────────────────────────────────────────────────
    def delete(self, movie_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
                return cursor.rowcount > 0

    # ── Status ────────────────────────────────────────────────────────────────
    def set_status(self, movie_id: int, active: bool) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE movies SET active = %s WHERE id = %s", (int(active), movie_id)
                )
                return cursor.rowcount > 0
