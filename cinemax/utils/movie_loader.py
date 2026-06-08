"""
utils/movie_loader.py
Funciones utilitarias para cargar y filtrar películas desde JSON local.
"""

import json
import os
from typing import Optional, List, Dict, Any


# Busca el archivo movies.json relativo al directorio raíz del proyecto
_THIS_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(_THIS_DIR, "..", "data", "movies.json")


def load_movies() -> List[Dict[str, Any]]:
    """Carga todas las películas desde el archivo JSON local."""
    try:
        path = os.path.abspath(DATA_PATH)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def get_featured_movies() -> List[Dict[str, Any]]:
    movies = load_movies()
    featured = [m for m in movies if m.get("vip", False)]
    return featured if featured else movies[:5]


def get_vip_movies() -> List[Dict[str, Any]]:
    return [m for m in load_movies() if m.get("vip", False)]


def search_movies(query: str) -> List[Dict[str, Any]]:
    if not query:
        return load_movies()
    q = query.lower()
    return [
        m for m in load_movies()
        if q in m.get("nombre", "").lower()
        or q in m.get("descripcion", "").lower()
        or q in m.get("categoria", "").lower()
    ]


def filter_by_category(category: str) -> List[Dict[str, Any]]:
    if not category or category == "Todos":
        return load_movies()
    return [m for m in load_movies() if m.get("categoria", "") == category]


def sort_movies(movies: List[Dict[str, Any]], by: str = "nombre", asc: bool = True) -> List[Dict[str, Any]]:
    reverse = not asc
    try:
        if by == "precio":
            return sorted(movies, key=lambda m: float(m.get("precio", 0)), reverse=reverse)
        return sorted(movies, key=lambda m: str(m.get(by, "")), reverse=reverse)
    except (TypeError, ValueError):
        return movies


def get_movie_by_id(movie_id: str) -> Optional[Dict[str, Any]]:
    return next((m for m in load_movies() if str(m.get("id")) == str(movie_id)), None)


def get_categories() -> List[str]:
    movies = load_movies()
    cats = sorted(set(m.get("categoria", "") for m in movies if m.get("categoria")))
    return ["Todos"] + cats
