"""
exporters/exportar_por_tabla.py

Lee cada tabla de cine_db y genera un archivo JSON independiente
en data/por_tabla/:
    peliculas.json
    generos.json
    salas.json
    funciones.json
    reservas.json
    usuarios.json          (sin password_hash por seguridad)
    peliculas_generos.json
    imagenes.json          (imágenes obtenidas de TMDB por película)

Uso:
    python -m exporters.exportar_por_tabla
"""

import json
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

from utils.db import query
from utils.tmdb import enriquecer_pelicula, get_imagenes_pelicula

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "por_tabla")


# ---------- helpers ---------------------------------------------------------

def _serializable(obj):
    """Convierte tipos no serializables de MySQL a tipos Python nativos."""
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return str(obj)
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Tipo no serializable: {type(obj)}")


def _guardar(nombre: str, data: list | dict) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ruta = os.path.join(OUTPUT_DIR, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=_serializable)
    print(f"  ✓ {nombre}  ({len(data) if isinstance(data, list) else 1} registro(s))")


# ---------- exportadores por tabla ------------------------------------------

def exportar_peliculas():
    rows = query("SELECT * FROM peliculas ORDER BY fecha_estreno DESC")
    _guardar("peliculas.json", rows)
    return rows


def exportar_generos():
    rows = query("SELECT * FROM generos ORDER BY nombre")
    _guardar("generos.json", rows)


def exportar_salas():
    rows = query("SELECT * FROM salas ORDER BY nombre")
    _guardar("salas.json", rows)


def exportar_funciones():
    rows = query("""
        SELECT f.*,
               p.titulo        AS pelicula_titulo,
               s.nombre        AS sala_nombre,
               s.tipo          AS sala_tipo
        FROM funciones f
        JOIN peliculas p ON f.pelicula_id = p.id
        JOIN salas     s ON f.sala_id     = s.id
        ORDER BY f.fecha_hora
    """)
    _guardar("funciones.json", rows)


def exportar_reservas():
    rows = query("""
        SELECT r.*,
               u.nombre        AS usuario_nombre,
               u.email         AS usuario_email,
               p.titulo        AS pelicula_titulo,
               f.fecha_hora    AS funcion_fecha_hora
        FROM reservas r
        JOIN usuarios  u ON r.usuario_id  = u.id
        JOIN funciones f ON r.funcion_id  = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        ORDER BY r.creado_en DESC
    """)
    _guardar("reservas.json", rows)


def exportar_usuarios():
    # NUNCA exportar password_hash
    rows = query("""
        SELECT id, nombre, email, fecha_nacimiento, creado_en
        FROM usuarios
        ORDER BY creado_en DESC
    """)
    _guardar("usuarios.json", rows)


def exportar_peliculas_generos():
    rows = query("""
        SELECT pg.pelicula_id,
               p.titulo     AS pelicula,
               pg.genero_id,
               g.nombre     AS genero
        FROM peliculas_generos pg
        JOIN peliculas p ON pg.pelicula_id = p.id
        JOIN generos   g ON pg.genero_id   = g.id
        ORDER BY p.titulo, g.nombre
    """)
    _guardar("peliculas_generos.json", rows)


def exportar_imagenes(peliculas: list[dict]):
    """
    Para cada película consulta TMDB y guarda sus imágenes.
    Genera imagenes.json con la estructura:
    [
      {
        "pelicula_id": 1,
        "titulo": "...",
        "poster_url": "...",
        "backdrop_url": "...",
        "calificacion_tmdb": 7.8,
        "galeria": { "posters": [...], "backdrops": [...] }
      },
      ...
    ]
    """
    print("  → Consultando TMDB para imágenes (puede tardar unos segundos)...")
    resultado = []
    for p in peliculas:
        datos = enriquecer_pelicula(p["titulo"])
        galeria = {}
        if datos["tmdb_id"]:
            galeria = get_imagenes_pelicula(datos["tmdb_id"])
        resultado.append({
            "pelicula_id": p["id"],
            "titulo": p["titulo"],
            **datos,
            "galeria": galeria,
        })
    _guardar("imagenes.json", resultado)


# ---------- main ------------------------------------------------------------

def exportar_todo():
    print("\n📦 Exportando tablas a JSON individuales...\n")
    peliculas = exportar_peliculas()
    exportar_generos()
    exportar_salas()
    exportar_funciones()
    exportar_reservas()
    exportar_usuarios()
    exportar_peliculas_generos()
    exportar_imagenes(peliculas)
    print(f"\n✅ Archivos guardados en: {os.path.abspath(OUTPUT_DIR)}\n")


if __name__ == "__main__":
    exportar_todo()