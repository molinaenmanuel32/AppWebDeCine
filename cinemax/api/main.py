# cinemax/api/main.py
"""
Punto de entrada de la API FastAPI.
Se monta como sub-aplicación dentro de la app Reflex.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import movies, auth

app = FastAPI(
    title="CineMax API",
    version="2.0.0",
    description="API REST para la gestión del cine online CineMax",
)

# CORS — ajusta origins en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movies.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "cinemax-api"}
