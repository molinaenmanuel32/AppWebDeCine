"""
utils/tmdb.py
Cliente TMDB usando Bearer Token (API Read Access Token v4).
Configura en .env:  TMDB_BEARER_TOKEN=eyJhbGci...
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv(override=False)

BASE_URL     = "https://api.themoviedb.org/3"
IMG_BASE     = "https://image.tmdb.org/t/p/w500"
IMG_BACKDROP = "https://image.tmdb.org/t/p/w1280"
PLACEHOLDER  = "https://placehold.co/500x750?text=Sin+imagen"
LANG         = "es-MX"

GENEROS_MAP = {
    28: "Acción", 12: "Aventura", 16: "Animación", 35: "Comedia",
    80: "Crimen", 99: "Documental", 18: "Drama", 10751: "Familiar",
    14: "Fantasía", 36: "Historia", 27: "Terror", 10402: "Música",
    9648: "Misterio", 10749: "Romance", 878: "Ciencia ficción",
    10770: "Película de TV", 53: "Thriller", 10752: "Bélica", 37: "Western",
}


def _bearer() -> str:
    """Lee el Bearer token en cada llamada (no al importar el módulo)."""
    load_dotenv(override=False)
    # Acepta tanto TMDB_BEARER_TOKEN como TMDB_API_KEY (por compatibilidad)
    token = (
        os.getenv("TMDB_BEARER_TOKEN", "").strip()
        or os.getenv("TMDB_API_KEY", "").strip()
    )
    return token


def _get(endpoint: str, params: dict = None) -> dict:
    """Petición GET autenticada con Bearer token."""
    token = _bearer()
    if not token or token == "TU_API_KEY_AQUI":
        raise ValueError(
            "Token TMDB no configurado. "
            "Agrega en .env: TMDB_BEARER_TOKEN=eyJhbGci..."
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }
    req_params = {"language": LANG}
    if params:
        req_params.update(params)

    with httpx.Client(timeout=15) as client:
        response = client.get(f"{BASE_URL}{endpoint}", headers=headers, params=req_params)
        response.raise_for_status()
        return response.json()


def _clasificacion(adult: bool, rating: float) -> str:
    if adult:       return "R"
    if rating >= 8: return "G"
    if rating >= 6: return "PG-13"
    return "PG"


def _build_movie(p: dict, categoria: str = "", precio: float = 250.0) -> dict:
    poster   = f"{IMG_BASE}{p['poster_path']}"     if p.get("poster_path")   else PLACEHOLDER
    backdrop = f"{IMG_BACKDROP}{p['backdrop_path']}" if p.get("backdrop_path") else PLACEHOLDER

    if not categoria and p.get("genre_ids"):
        categoria = GENEROS_MAP.get(p["genre_ids"][0], "Varios")
    if not categoria:
        categoria = "Varios"

    return {
        "id":                f"tmdb_{p['id']}",
        "nombre":            p.get("title", p.get("name", "")),
        "descripcion":       p.get("overview", ""),
        "categoria":         categoria,
        "duracion":          str(p.get("runtime") or "120"),
        "precio":            precio,
        "imagen":            poster,
        "backdrop":          backdrop,
        "horarios":          ["14:00", "16:30", "19:00", "21:30"],
        "vip":               float(p.get("vote_average", 0)) >= 8.0,
        "clasificacion":     _clasificacion(p.get("adult", False), float(p.get("vote_average", 0))),
        "fecha_estreno":     p.get("release_date", ""),
        "director":          "",
        "calificacion_tmdb": round(float(p.get("vote_average", 0)), 1),
        "popularidad":       float(p.get("popularity", 0)),
        "tmdb_id":           p.get("id"),
        "vote_count":        p.get("vote_count", 0),
    }


# ── Endpoints ─────────────────────────────────────────────────────────────────

def peliculas_cartelera(paginas: int = 2) -> list:
    resultado = []
    for page in range(1, paginas + 1):
        data = _get("/movie/now_playing", {"page": page, "region": "MX"})
        for p in data.get("results", []):
            resultado.append(_build_movie(p, precio=250.0))
    return resultado


def peliculas_populares(paginas: int = 2) -> list:
    resultado = []
    for page in range(1, paginas + 1):
        data = _get("/movie/popular", {"page": page})
        for p in data.get("results", []):
            resultado.append(_build_movie(p, precio=200.0))
    return resultado


def peliculas_mejor_calificadas(paginas: int = 1) -> list:
    resultado = []
    for page in range(1, paginas + 1):
        data = _get("/movie/top_rated", {"page": page})
        for p in data.get("results", []):
            resultado.append(_build_movie(p, precio=180.0))
    return resultado


def proximos_estrenos(paginas: int = 1) -> list:
    resultado = []
    for page in range(1, paginas + 1):
        data = _get("/movie/upcoming", {"page": page, "region": "MX"})
        for p in data.get("results", []):
            m = _build_movie(p, categoria="Próximo estreno", precio=270.0)
            resultado.append(m)
    return resultado


def buscar_pelicula_tmdb(titulo: str, paginas: int = 1) -> list:
    resultado = []
    for page in range(1, paginas + 1):
        data = _get("/search/movie", {"query": titulo, "page": page})
        for p in data.get("results", []):
            resultado.append(_build_movie(p))
    return resultado


def detalle_pelicula(tmdb_id: int) -> dict:
    try:
        p = _get(f"/movie/{tmdb_id}", {"append_to_response": "credits"})
        movie = _build_movie(p, precio=250.0)
        movie["duracion"] = str(p.get("runtime") or "120")

        credits  = p.get("credits", {})
        crew     = credits.get("crew", [])
        cast     = credits.get("cast", [])
        movie["director"] = next((c["name"] for c in crew if c.get("job") == "Director"), "")
        movie["reparto"]  = [a["name"] for a in cast[:5]]
        movie["trailer"]  = get_trailer_url(tmdb_id)
        generos = [g["name"] for g in p.get("genres", [])]
        movie["generos"]  = generos
        if generos:
            movie["categoria"] = generos[0]
        return movie
    except Exception as e:
        print("TMDB detalle error:", e)
        return {}


def get_trailer_url(tmdb_id: int) -> str:
    try:
        data = _get(f"/movie/{tmdb_id}/videos")
        for v in data.get("results", []):
            if v.get("site") == "YouTube" and v.get("type") in ("Trailer", "Teaser"):
                return f"https://www.youtube.com/embed/{v['key']}"
    except Exception:
        pass
    return ""


def get_imagenes_pelicula(tmdb_id: int) -> dict:
    try:
        data = _get(f"/movie/{tmdb_id}/images")
        return {
            "posters":   [f"{IMG_BASE}{i['file_path']}"     for i in data.get("posters", [])[:5]],
            "backdrops": [f"{IMG_BACKDROP}{i['file_path']}" for i in data.get("backdrops", [])[:5]],
        }
    except Exception:
        return {"posters": [PLACEHOLDER], "backdrops": [PLACEHOLDER]}


# ── Compatibilidad ────────────────────────────────────────────────────────────
def buscar_pelicula(titulo: str):
    try:
        res = buscar_pelicula_tmdb(titulo, paginas=1)
        return res[0] if res else None
    except Exception:
        return None

def get_poster_url(titulo: str) -> str:
    p = buscar_pelicula(titulo)
    return p["imagen"] if p else PLACEHOLDER

def get_backdrop_url(titulo: str) -> str:
    p = buscar_pelicula(titulo)
    return p["backdrop"] if p else PLACEHOLDER

def enriquecer_pelicula(titulo: str) -> dict:
    p = buscar_pelicula(titulo)
    if not p:
        return {"tmdb_id": None, "poster_url": PLACEHOLDER,
                "backdrop_url": PLACEHOLDER, "calificacion_tmdb": None, "popularidad": None}
    return {
        "tmdb_id":           p.get("tmdb_id"),
        "poster_url":        p.get("imagen", PLACEHOLDER),
        "backdrop_url":      p.get("backdrop", PLACEHOLDER),
        "calificacion_tmdb": p.get("calificacion_tmdb"),
        "popularidad":       p.get("popularidad"),
    }
