# cinemax/api/services/movie_service.py
"""
Servicio de Películas — lógica de negocio.
El router solo llama al servicio; el servicio solo llama al repositorio.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status

from ..repositories.movie_repository import MovieRepository
from ..schemas.movie import MovieCreate, MovieUpdate, MovieStatusUpdate, MovieResponse


class MovieService:

    def __init__(self) -> None:
        self._repo = MovieRepository()

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _or_404(self, movie: Optional[Dict]) -> Dict:
        if not movie:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Película no encontrada")
        return movie

    # ── Public API ────────────────────────────────────────────────────────────
    def list_movies(self, active_only: bool = False) -> List[Dict]:
        return self._repo.find_all(active_only=active_only)

    def get_movie(self, movie_id: int) -> Dict:
        return self._or_404(self._repo.find_by_id(movie_id))

    def create_movie(self, payload: MovieCreate) -> Dict:
        data = payload.model_dump()
        # Decimal → float para MySQL
        data["price"] = float(data["price"])
        data["active"] = int(data["active"])
        new_id = self._repo.create(data)
        return self._repo.find_by_id(new_id)

    def update_movie(self, movie_id: int, payload: MovieUpdate) -> Dict:
        self._or_404(self._repo.find_by_id(movie_id))
        data = {k: v for k, v in payload.model_dump().items() if v is not None}
        if "price" in data:
            data["price"] = float(data["price"])
        self._repo.update(movie_id, data)
        return self._repo.find_by_id(movie_id)

    def delete_movie(self, movie_id: int) -> Dict[str, str]:
        self._or_404(self._repo.find_by_id(movie_id))
        self._repo.delete(movie_id)
        return {"message": "Película eliminada correctamente"}

    def set_status(self, movie_id: int, payload: MovieStatusUpdate) -> Dict:
        self._or_404(self._repo.find_by_id(movie_id))
        self._repo.set_status(movie_id, payload.active)
        return self._repo.find_by_id(movie_id)

    def get_dashboard_stats(self) -> Dict[str, Any]:
        return {
            "total_movies": self._repo.count_total(),
            "active_movies": self._repo.count_active(),
            "recent_movies": self._repo.find_recent(5),
        }
