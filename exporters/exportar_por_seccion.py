"""
exporters/exportar_por_seccion.py

Lee la BD y genera JSONs organizados por sección de la página web,
en data/por_seccion/:

    inicio_ofertas.json        → Cartelera + películas destacadas (para Home)
    inicio_imagenes.json       → Imágenes hero/banner para el Home
    inicio_contacto.json       → Datos de contacto del cine
    descripcion_general.json   → Info detallada de cada película (con imágenes)
    descripcion_detalles.json  → Detalles técnicos (sala, horarios, precios)
    descripcion_itinerario.json→ Funciones del día organizadas como "itinerario"
    reservas_actividades.json  → Funciones disponibles para reservar
    reservas_pagos.json        → Resumen de precios y métodos de pago

Uso:
    python -m exporters.exportar_por_seccion
"""

import json
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

from utils.db import query
from utils.tmdb import enriquecer_pelicula, get_imagenes_pelicula

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "por_seccion")

CONTACTO_CINE = {
    "nombre": "CineMax Plaza",
    "direccion": "Av. Winston Churchill esq. 27 de Febrero, Santo Domingo",
    "telefono": "+1 (809) 555-0199",
    "email": "info@cinemaxplaza.com",
    "redes": {
        "instagram": "@cinemaxplaza",
        "facebook": "CineMaxPlaza",
        "twitter": "@CineMaxRD",
    },
    "horario_taquilla": "Lun–Dom: 12:00 – 23:00",
}


# ---------- helpers ---------------------------------------------------------

def _serializable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return str(obj)
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Tipo no serializable: {type(obj)}")


def _guardar(nombre: str, data) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ruta = os.path.join(OUTPUT_DIR, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=_serializable)
    count = len(data) if isinstance(data, list) else (len(data.get("items", [])) if isinstance(data, dict) else 1)
    print(f"  ✓ {nombre}  ({count} elemento(s))")


# ---------- sección INICIO --------------------------------------------------

def exportar_inicio_ofertas():
    """
    Películas en cartelera enriquecidas con TMDB.
    Sirve para la sección 'Ofertas / Cartelera' del Home.
    """
    rows = query("""
        SELECT
            p.id, p.titulo, p.sinopsis, p.duracion_min,
            p.fecha_estreno, p.clasificacion,
            MIN(f.precio)      AS precio_desde,
            COUNT(f.id)        AS total_funciones,
            SUM(f.asientos_disp) AS asientos_disponibles,
            GROUP_CONCAT(DISTINCT g.nombre ORDER BY g.nombre SEPARATOR ', ') AS generos
        FROM peliculas p
        JOIN funciones f ON f.pelicula_id = p.id
        LEFT JOIN peliculas_generos pg ON pg.pelicula_id = p.id
        LEFT JOIN generos g ON g.id = pg.genero_id
        WHERE f.asientos_disp > 0
        GROUP BY p.id, p.titulo, p.sinopsis, p.duracion_min, p.fecha_estreno, p.clasificacion
        ORDER BY p.fecha_estreno DESC
    """)

    print("  → Enriqueciendo con TMDB...")
    for r in rows:
        tmdb = enriquecer_pelicula(r["titulo"])
        r.update(tmdb)

    _guardar("inicio_ofertas.json", rows)


def exportar_inicio_imagenes():
    """
    Imágenes hero/banner: backdrops de las películas más recientes.
    """
    peliculas = query("SELECT id, titulo FROM peliculas ORDER BY fecha_estreno DESC LIMIT 6")
    imagenes = []
    print("  → Obteniendo backdrops TMDB para el hero...")
    for p in peliculas:
        tmdb = enriquecer_pelicula(p["titulo"])
        imagenes.append({
            "pelicula_id": p["id"],
            "titulo": p["titulo"],
            "backdrop_url": tmdb["backdrop_url"],
            "poster_url": tmdb["poster_url"],
        })
    _guardar("inicio_imagenes.json", imagenes)


def exportar_inicio_contacto():
    """Datos de contacto del cine (estático + generado)."""
    _guardar("inicio_contacto.json", CONTACTO_CINE)


# ---------- sección DESCRIPCIÓN --------------------------------------------

def exportar_descripcion_general():
    """
    Descripción completa de cada película con galería de imágenes.
    """
    peliculas = query("""
        SELECT p.*,
               GROUP_CONCAT(DISTINCT g.nombre ORDER BY g.nombre SEPARATOR ', ') AS generos
        FROM peliculas p
        LEFT JOIN peliculas_generos pg ON pg.pelicula_id = p.id
        LEFT JOIN generos g ON g.id = pg.genero_id
        GROUP BY p.id
        ORDER BY p.fecha_estreno DESC
    """)

    print("  → Obteniendo galería TMDB...")
    resultado = []
    for p in peliculas:
        tmdb = enriquecer_pelicula(p["titulo"])
        galeria = {}
        if tmdb["tmdb_id"]:
            galeria = get_imagenes_pelicula(tmdb["tmdb_id"])
        resultado.append({
            **p,
            **tmdb,
            "galeria": galeria,
        })
    _guardar("descripcion_general.json", resultado)


def exportar_descripcion_detalles():
    """
    Detalles técnicos de cada película: salas donde se proyecta,
    tipos de tecnología y rango de precios.
    """
    rows = query("""
        SELECT
            p.id            AS pelicula_id,
            p.titulo,
            p.duracion_min,
            p.clasificacion,
            s.nombre        AS sala,
            s.tipo          AS tecnologia,
            s.capacidad,
            f.precio,
            f.fecha_hora,
            f.asientos_disp
        FROM peliculas p
        JOIN funciones f ON f.pelicula_id = p.id
        JOIN salas     s ON f.sala_id     = s.id
        ORDER BY p.id, f.fecha_hora
    """)

    # Agrupar por película
    peliculas: dict = {}
    for r in rows:
        pid = r["pelicula_id"]
        if pid not in peliculas:
            peliculas[pid] = {
                "pelicula_id": pid,
                "titulo": r["titulo"],
                "duracion_min": r["duracion_min"],
                "clasificacion": r["clasificacion"],
                "tecnologias_disponibles": set(),
                "precio_min": r["precio"],
                "precio_max": r["precio"],
                "funciones": [],
            }
        p = peliculas[pid]
        p["tecnologias_disponibles"].add(r["tecnologia"])
        p["precio_min"] = min(p["precio_min"], r["precio"])
        p["precio_max"] = max(p["precio_max"], r["precio"])
        p["funciones"].append({
            "sala": r["sala"],
            "tecnologia": r["tecnologia"],
            "capacidad": r["capacidad"],
            "fecha_hora": r["fecha_hora"],
            "precio": r["precio"],
            "asientos_disp": r["asientos_disp"],
        })

    # Convertir sets a listas para serializar
    resultado = []
    for p in peliculas.values():
        p["tecnologias_disponibles"] = sorted(p["tecnologias_disponibles"])
        resultado.append(p)

    _guardar("descripcion_detalles.json", resultado)


def exportar_descripcion_itinerario():
    """
    Funciones organizadas por fecha (como 'itinerario diario').
    Agrupa todas las funciones por día.
    """
    rows = query("""
        SELECT
            DATE(f.fecha_hora)  AS fecha,
            f.id                AS funcion_id,
            p.titulo,
            p.clasificacion,
            s.nombre            AS sala,
            s.tipo              AS tecnologia,
            TIME(f.fecha_hora)  AS hora,
            f.precio,
            f.asientos_disp
        FROM funciones f
        JOIN peliculas p ON f.pelicula_id = p.id
        JOIN salas     s ON f.sala_id     = s.id
        ORDER BY fecha, f.fecha_hora
    """)

    itinerario: dict = {}
    for r in rows:
        fecha_str = r["fecha"].isoformat() if isinstance(r["fecha"], date) else str(r["fecha"])
        if fecha_str not in itinerario:
            itinerario[fecha_str] = {"fecha": fecha_str, "funciones": []}
        itinerario[fecha_str]["funciones"].append({
            "funcion_id": r["funcion_id"],
            "titulo": r["titulo"],
            "clasificacion": r["clasificacion"],
            "sala": r["sala"],
            "tecnologia": r["tecnologia"],
            "hora": str(r["hora"]),
            "precio": r["precio"],
            "asientos_disp": r["asientos_disp"],
        })

    _guardar("descripcion_itinerario.json", list(itinerario.values()))


# ---------- sección RESERVAS -----------------------------------------------

def exportar_reservas_actividades():
    """
    Funciones disponibles para reservar (con datos completos para el form).
    """
    rows = query("""
        SELECT
            f.id            AS funcion_id,
            p.id            AS pelicula_id,
            p.titulo,
            p.duracion_min,
            p.clasificacion,
            s.id            AS sala_id,
            s.nombre        AS sala,
            s.tipo          AS tecnologia,
            f.fecha_hora,
            f.precio,
            f.asientos_disp
        FROM funciones f
        JOIN peliculas p ON f.pelicula_id = p.id
        JOIN salas     s ON f.sala_id     = s.id
        WHERE f.asientos_disp > 0
        ORDER BY f.fecha_hora
    """)
    _guardar("reservas_actividades.json", rows)


def exportar_reservas_pagos():
    """
    Resumen de precios por tipo de sala y descripción de métodos de pago.
    """
    precios = query("""
        SELECT
            s.tipo                  AS tecnologia,
            MIN(f.precio)           AS precio_min,
            MAX(f.precio)           AS precio_max,
            ROUND(AVG(f.precio),2)  AS precio_promedio,
            COUNT(f.id)             AS total_funciones
        FROM funciones f
        JOIN salas s ON f.sala_id = s.id
        GROUP BY s.tipo
        ORDER BY precio_min
    """)

    metodos_pago = [
        {"id": "tarjeta", "nombre": "Tarjeta de crédito / débito", "descripcion": "Visa, Mastercard, American Express"},
        {"id": "transferencia", "nombre": "Transferencia bancaria", "descripcion": "BanReservas, Banco Popular, BHD León"},
        {"id": "efectivo", "nombre": "Efectivo en taquilla", "descripcion": "Solo al recoger las entradas en taquilla"},
        {"id": "paypal", "nombre": "PayPal", "descripcion": "Pago seguro en línea"},
    ]

    resultado = {
        "precios_por_tecnologia": precios,
        "metodos_pago": metodos_pago,
        "politica_cancelacion": (
            "Las reservas pueden cancelarse hasta 2 horas antes de la función "
            "para reembolso completo. Pasado ese tiempo no hay devolución."
        ),
        "descuentos": [
            {"tipo": "Niños (menores de 12)", "porcentaje": 30},
            {"tipo": "Adultos mayores (+65)", "porcentaje": 40},
            {"tipo": "Estudiantes (con carnet)", "porcentaje": 20},
            {"tipo": "Martes de cine", "porcentaje": 50},
        ],
    }
    _guardar("reservas_pagos.json", resultado)


# ---------- main ------------------------------------------------------------

def exportar_todo():
    print("\n📦 Exportando JSONs por sección...\n")

    print("  [ INICIO ]")
    exportar_inicio_ofertas()
    exportar_inicio_imagenes()
    exportar_inicio_contacto()

    print("\n  [ DESCRIPCIÓN ]")
    exportar_descripcion_general()
    exportar_descripcion_detalles()
    exportar_descripcion_itinerario()

    print("\n  [ RESERVAS ]")
    exportar_reservas_actividades()
    exportar_reservas_pagos()

    print(f"\n✅ Archivos guardados en: {os.path.abspath(OUTPUT_DIR)}\n")


if __name__ == "__main__":
    exportar_todo()