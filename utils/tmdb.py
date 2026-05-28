"""
utils/tmdb.py
Cliente ligero para The Movie Database (TMDB) API.
Obtiene pósters, backdrops y datos de películas por título.
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY", "")
BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
IMG_BASE = os.getenv("TMDB_IMAGE_BASE", "https://image.tmdb.org/t/p/w500")
IMG_BACKDROP = "https://image.tmdb.org/t/p/w1280"
PLACEHOLDER = "https://placehold.co/500x750?text=Sin+imagen"


def _get(endpoint: str, params: dict) -> dict:
    params["api_key"] = API_KEY
    params["language"] = "es-MX"
    with httpx.Client(timeout=8) as client:
        r = client.get(f"{BASE_URL}{endpoint}", params=params)
        r.raise_for_status()
        return r.json()


def buscar_pelicula(titulo: str) -> dict | None:
    """Busca una película por título y devuelve el primer resultado."""
    try:
        data = _get("/search/movie", {"query": titulo})
        results = data.get("results", [])
        return results[0] if results else None
    except Exception:
        return None


def get_poster_url(titulo: str) -> str:
    """Devuelve la URL del póster de una película. Placeholder si no encuentra."""
    pelicula = buscar_pelicula(titulo)
    if pelicula and pelicula.get("poster_path"):
        return f"{IMG_BASE}{pelicula['poster_path']}"
    return PLACEHOLDER


def get_backdrop_url(titulo: str) -> str:
    """Devuelve el backdrop (imagen de fondo) de una película."""
    pelicula = buscar_pelicula(titulo)
    if pelicula and pelicula.get("backdrop_path"):
        return f"{IMG_BACKDROP}{pelicula['backdrop_path']}"
    return PLACEHOLDER


def enriquecer_pelicula(titulo: str) -> dict:
    """
    Devuelve un dict con imágenes y datos extra de TMDB para
    una película dado su título.
    """
    pelicula = buscar_pelicula(titulo)
    if not pelicula:
        return {
            "tmdb_id": None,
            "poster_url": PLACEHOLDER,
            "backdrop_url": PLACEHOLDER,
            "calificacion_tmdb": None,
            "popularidad": None,
        }
    return {
        "tmdb_id": pelicula.get("id"),
        "poster_url": (
            f"{IMG_BASE}{pelicula['poster_path']}"
            if pelicula.get("poster_path")
            else PLACEHOLDER
        ),
        "backdrop_url": (
            f"{IMG_BACKDROP}{pelicula['backdrop_path']}"
            if pelicula.get("backdrop_path")
            else PLACEHOLDER
        ),
        "calificacion_tmdb": pelicula.get("vote_average"),
        "popularidad": pelicula.get("popularity"),
    }


def get_imagenes_pelicula(tmdb_id: int) -> dict:
    """
    Devuelve todas las imágenes disponibles de una película por su ID de TMDB.
    Retorna dicts con listas de poster_urls y backdrop_urls.
    """
    try:
        data = _get(f"/movie/{tmdb_id}/images", {})
        posters = [
            f"{IMG_BASE}{img['file_path']}"
            for img in data.get("posters", [])[:5]
        ]
        backdrops = [
            f"{IMG_BACKDROP}{img['file_path']}"
            for img in data.get("backdrops", [])[:5]
        ]
        return {"posters": posters, "backdrops": backdrops}
    except Exception:
        return {"posters": [PLACEHOLDER], "backdrops": [PLACEHOLDER]}