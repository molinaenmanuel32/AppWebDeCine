# cinemax/cinemax.py
"""
Punto de entrada principal de la app Reflex.
Registra TODAS las páginas incluyendo las de administración.
La API FastAPI se monta en /api/ mediante app.api.
"""

import reflex as rx

# ── Importar páginas principales ─────────────────────────────────────────────
from .pages.index import index_page                     # noqa: F401
from .pages.login import login_page                     # noqa: F401
from .pages.registro import registro_page               # noqa: F401
from .pages.catalogo import catalogo_page               # noqa: F401
from .pages.pelicula import movie_detail_page  # noqa: F401               # noqa: F401
from .pages.reservas import reservas_page               # noqa: F401
from .pages.mis_reservas import mis_reservas_page       # noqa: F401

# ── Importar páginas de administración ───────────────────────────────────────
from .pages.admin.dashboard import admin_dashboard_page  # noqa: F401
from .pages.admin.movies import admin_movies_page        # noqa: F401

# ── Importar API FastAPI ──────────────────────────────────────────────────────
from .api.main import app as fastapi_app


# ── App Reflex ────────────────────────────────────────────────────────────────
app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="red"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&display=swap",
    ],
    style={
        "font_family": "Inter, sans-serif",
        "background_color": "#0a0a0a",
    },
)

# Montar la API FastAPI bajo el prefijo /api
# En Reflex 0.9.x se usa app.api para sub-aplicaciones ASGI
app.api = fastapi_app
