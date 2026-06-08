# cinemax/api/routers/movies.py
"""
Router de Películas.
Endpoints públicos: GET /movies, GET /movies/{id}
Endpoints admin: POST, PUT, DELETE, PATCH /status
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status

from ..schemas.movie import MovieCreate, MovieUpdate, MovieStatusUpdate, MovieResponse
from ..services.movie_service import MovieService
from ..services.auth_service import get_current_user, require_admin
from ..schemas.auth import UserResponse

router = APIRouter(prefix="/movies", tags=["movies"])


def _service() -> MovieService:
    return MovieService()


# ── Públicos ──────────────────────────────────────────────────────────────────
@router.get("/", response_model=List[MovieResponse])
def list_movies(
    active_only: bool = True,
    service: MovieService = Depends(_service),
):
    """Lista películas. Por defecto solo las activas (para cartelera pública)."""
    return service.list_movies(active_only=active_only)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, service: MovieService = Depends(_service)):
    return service.get_movie(movie_id)


# ── Solo Admin ────────────────────────────────────────────────────────────────
@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    payload: MovieCreate,
    _admin: UserResponse = Depends(require_admin),
    service: MovieService = Depends(_service),
):
    return service.create_movie(payload)


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    _admin: UserResponse = Depends(require_admin),
    service: MovieService = Depends(_service),
):
    return service.update_movie(movie_id, payload)


@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    _admin: UserResponse = Depends(require_admin),
    service: MovieService = Depends(_service),
):
    return service.delete_movie(movie_id)


@router.patch("/{movie_id}/status", response_model=MovieResponse)
def update_status(
    movie_id: int,
    payload: MovieStatusUpdate,
    _admin: UserResponse = Depends(require_admin),
    service: MovieService = Depends(_service),
):
    return service.set_status(movie_id, payload)


# ── Dashboard admin ───────────────────────────────────────────────────────────
@router.get("/admin/dashboard")
def dashboard(
    _admin: UserResponse = Depends(require_admin),
    service: MovieService = Depends(_service),
):
    return service.get_dashboard_stats()
