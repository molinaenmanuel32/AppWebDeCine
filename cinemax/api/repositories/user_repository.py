# cinemax/api/repositories/user_repository.py
"""Repositorio de Usuarios — usa PyMySQL con DictCursor."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..database import get_connection


class UserRepository:

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email, password, role FROM users WHERE email = %s",
                    (email,),
                )
                return cursor.fetchone()

    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email, role FROM users WHERE id = %s", (user_id,)
                )
                return cursor.fetchone()

    def create(self, name: str, email: str, hashed_password: str) -> int:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'user')",
                    (name, email, hashed_password),
                )
                return cursor.lastrowid
