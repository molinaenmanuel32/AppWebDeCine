# cinemax/states/movie_state.py
"""
Estado de Películas.
Consume la API REST — NO usa datos hardcodeados ni movies.json.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import httpx
import reflex as rx

from .auth_state import AuthState

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


class MovieState(AuthState):
    # ── Lista pública ─────────────────────────────────────────────────────────
    movies: List[Dict[str, Any]] = []
    selected_movie: Dict[str, Any] = {}
    is_loading_movies: bool = False
    movies_error: str = ""

    # ── Admin — lista completa ────────────────────────────────────────────────
    admin_movies: List[Dict[str, Any]] = []
    dashboard_stats: Dict[str, Any] = {"total_movies": 0, "active_movies": 0, "recent_movies": []}

    # ── Form de película ──────────────────────────────────────────────────────
    form_title: str = ""
    form_description: str = ""
    form_genre: str = ""
    form_duration: str = ""
    form_classification: str = ""
    form_director: str = ""
    form_release_date: str = ""
    form_poster_url: str = ""
    form_trailer_url: str = ""
    form_price: str = ""
    form_active: bool = True
    editing_movie_id: int = 0
    show_form: bool = False
    form_error: str = ""
    form_success: str = ""

    # ── Computed ──────────────────────────────────────────────────────────────
    @rx.var
    def is_editing(self) -> bool:
        return self.editing_movie_id > 0

    @rx.var
    def inactive_movies(self) -> int:
        return (
            self.dashboard_stats.get("total_movies", 0)
            - self.dashboard_stats.get("active_movies", 0)
        )
    # ── Public: cargar cartelera ──────────────────────────────────────────────
    async def load_movies(self):
        self.is_loading_movies = True
        self.movies_error = ""
        yield
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{API_BASE}/movies/?active_only=true", timeout=10)
            if resp.status_code == 200:
                self.movies = resp.json()
            else:
                self.movies_error = "No se pudo cargar la cartelera"
        except Exception as e:
            self.movies_error = f"Error: {str(e)}"
        finally:
            self.is_loading_movies = False

    async def load_movie_detail(self, movie_id: int):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{API_BASE}/movies/{movie_id}", timeout=10)
            if resp.status_code == 200:
                self.selected_movie = resp.json()
        except Exception:
            self.selected_movie = {}

    # ── Admin: cargar todas las películas ─────────────────────────────────────
    async def admin_load_movies(self):
        if not self.is_admin:
            return rx.redirect("/")
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{API_BASE}/movies/?active_only=false",
                    headers=self._auth_headers(),
                    timeout=10,
                )
            if resp.status_code == 200:
                self.admin_movies = resp.json()
        except Exception:
            pass

    async def admin_load_dashboard(self):
        if not self.is_admin:
            return rx.redirect("/")
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{API_BASE}/movies/admin/dashboard",
                    headers=self._auth_headers(),
                    timeout=10,
                )
            if resp.status_code == 200:
                self.dashboard_stats = resp.json()
        except Exception:
            pass

    # ── Admin: acciones ───────────────────────────────────────────────────────
    def open_create_form(self):
        self._reset_form()
        self.editing_movie_id = 0
        self.show_form = True

    def open_edit_form(self, movie: Dict[str, Any]):
        self.editing_movie_id = movie.get("id", 0)
        self.form_title = movie.get("title", "")
        self.form_description = movie.get("description", "") or ""
        self.form_genre = movie.get("genre", "") or ""
        self.form_duration = str(movie.get("duration", "")) if movie.get("duration") else ""
        self.form_classification = movie.get("classification", "") or ""
        self.form_director = movie.get("director", "") or ""
        self.form_release_date = str(movie.get("release_date", "")) if movie.get("release_date") else ""
        self.form_poster_url = movie.get("poster_url", "") or ""
        self.form_trailer_url = movie.get("trailer_url", "") or ""
        self.form_price = str(movie.get("price", "0"))
        self.form_active = bool(movie.get("active", True))
        self.show_form = True

    def close_form(self):
        self._reset_form()
        self.show_form = False

    def _reset_form(self):
        self.form_title = ""
        self.form_description = ""
        self.form_genre = ""
        self.form_duration = ""
        self.form_classification = ""
        self.form_director = ""
        self.form_release_date = ""
        self.form_poster_url = ""
        self.form_trailer_url = ""
        self.form_price = ""
        self.form_active = True
        self.editing_movie_id = 0
        self.form_error = ""
        self.form_success = ""

    def _build_payload(self) -> Optional[Dict]:
        if not self.form_title.strip():
            self.form_error = "El título es obligatorio"
            return None
        try:
            price = float(self.form_price) if self.form_price else 0.0
        except ValueError:
            self.form_error = "El precio debe ser un número válido"
            return None
        duration = int(self.form_duration) if self.form_duration.isdigit() else None
        return {
            "title": self.form_title,
            "description": self.form_description or None,
            "genre": self.form_genre or None,
            "duration": duration,
            "classification": self.form_classification or None,
            "director": self.form_director or None,
            "release_date": self.form_release_date or None,
            "poster_url": self.form_poster_url or None,
            "trailer_url": self.form_trailer_url or None,
            "price": price,
            "active": self.form_active,
        }

    async def save_movie(self):
        self.form_error = ""
        payload = self._build_payload()
        if payload is None:
            return
        try:
            async with httpx.AsyncClient() as client:
                if self.is_editing:
                    resp = await client.put(
                        f"{API_BASE}/movies/{self.editing_movie_id}",
                        json=payload,
                        headers=self._auth_headers(),
                        timeout=10,
                    )
                else:
                    resp = await client.post(
                        f"{API_BASE}/movies/",
                        json=payload,
                        headers=self._auth_headers(),
                        timeout=10,
                    )
            if resp.status_code in (200, 201):
                self.form_success = "Película guardada correctamente"
                self.show_form = False
                self._reset_form()
                yield MovieState.admin_load_movies
            else:
                self.form_error = resp.json().get("detail", "Error al guardar")
        except Exception as e:
            self.form_error = f"Error de conexión: {str(e)}"

    async def delete_movie(self, movie_id: int):
        try:
            async with httpx.AsyncClient() as client:
                await client.delete(
                    f"{API_BASE}/movies/{movie_id}",
                    headers=self._auth_headers(),
                    timeout=10,
                )
            yield MovieState.admin_load_movies
        except Exception:
            pass

    async def toggle_status(self, movie_id: int, current_active: bool):
        try:
            async with httpx.AsyncClient() as client:
                await client.patch(
                    f"{API_BASE}/movies/{movie_id}/status",
                    json={"active": not current_active},
                    headers=self._auth_headers(),
                    timeout=10,
                )
            yield MovieState.admin_load_movies
        except Exception:
            pass

    # ── Setters de formulario (requeridos por admin/movies.py) ────────────────
    def set_form_title(self, val: str): self.form_title = val
    def set_form_description(self, val: str): self.form_description = val
    def set_form_genre(self, val: str): self.form_genre = val
    def set_form_duration(self, val: str): self.form_duration = val
    def set_form_classification(self, val: str): self.form_classification = val
    def set_form_director(self, val: str): self.form_director = val
    def set_form_release_date(self, val: str): self.form_release_date = val
    def set_form_poster_url(self, val: str): self.form_poster_url = val
    def set_form_trailer_url(self, val: str): self.form_trailer_url = val
    def set_form_price(self, val: str): self.form_price = val
    def set_form_active(self, val: bool): self.form_active = val
