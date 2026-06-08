#!/usr/bin/env python3
"""
scripts/actualizar_bd_con_tmdb.py

Actualiza las peliculas de tu BD MySQL con datos reales de TMDB:
poster, backdrop, sinopsis, duracion, director, precio y calificacion.

Uso:
    cd AppCineManon_TMDB
    python scripts/actualizar_bd_con_tmdb.py
"""

import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(override=False)

import pymysql, pymysql.cursors, httpx

BEARER       = (os.getenv("TMDB_BEARER_TOKEN") or os.getenv("TMDB_API_KEY") or "").strip()
TMDB_BASE    = "https://api.themoviedb.org/3"
IMG_BASE     = "https://image.tmdb.org/t/p/w500"
IMG_BACKDROP = "https://image.tmdb.org/t/p/w1280"
PRECIO_BASE  = 350.0
LANG         = "es-MX"
HEADERS      = {"Authorization": f"Bearer {BEARER}", "accept": "application/json"}


def tmdb_buscar(titulo: str):
    try:
        r = httpx.get(f"{TMDB_BASE}/search/movie",
                      headers=HEADERS,
                      params={"query": titulo, "language": LANG},
                      timeout=10)
        r.raise_for_status()
        results = r.json().get("results", [])
        return results[0] if results else None
    except Exception as e:
        print(f"  TMDB search error '{titulo}': {e}")
        return None


def tmdb_detalle(tmdb_id: int):
    try:
        r = httpx.get(f"{TMDB_BASE}/movie/{tmdb_id}",
                      headers=HEADERS,
                      params={"language": LANG, "append_to_response": "credits"},
                      timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  TMDB detalle error {tmdb_id}: {e}")
        return {}


def get_director(detalle: dict) -> str:
    crew = detalle.get("credits", {}).get("crew", [])
    return next((c["name"] for c in crew if c.get("job") == "Director"), "")


def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl": True},
        connect_timeout=10,
    )


def main():
    if not BEARER or BEARER == "TU_API_KEY_AQUI":
        print("ERROR: TMDB_BEARER_TOKEN no configurado en .env")
        sys.exit(1)

    print(f"\n=== Actualizando BD con TMDB ===")
    print(f"Token: {BEARER[:30]}...\n")

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM peliculas ORDER BY id")
            peliculas = cur.fetchall()
            cur.execute("DESCRIBE peliculas")
            columnas = {row["Field"] for row in cur.fetchall()}

        print(f"Peliculas en BD: {len(peliculas)}")
        print(f"Columnas disponibles: {sorted(columnas)}\n")

        ok = 0
        for p in peliculas:
            pid    = p.get("id")
            titulo = p.get("titulo", "")
            precio = float(p.get("precio") or 0)
            print(f"[{pid}] {titulo}")

            tmdb = tmdb_buscar(titulo)
            if not tmdb:
                # Sin TMDB al menos arreglar el precio
                if precio == 0 and "precio" in columnas:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE peliculas SET precio=%s WHERE id=%s", (PRECIO_BASE, pid))
                    conn.commit()
                    print(f"  Precio actualizado a {PRECIO_BASE}")
                else:
                    print(f"  No encontrado en TMDB")
                continue

            tmdb_id = tmdb.get("id")
            det     = tmdb_detalle(tmdb_id) if tmdb_id else {}

            updates = {}

            if "poster_url" in columnas and tmdb.get("poster_path"):
                updates["poster_url"] = f"{IMG_BASE}{tmdb['poster_path']}"
            if "backdrop_url" in columnas and tmdb.get("backdrop_path"):
                updates["backdrop_url"] = f"{IMG_BACKDROP}{tmdb['backdrop_path']}"
            if "sinopsis" in columnas:
                sinopsis = det.get("overview") or tmdb.get("overview") or ""
                if sinopsis:
                    updates["sinopsis"] = sinopsis
            if "duracion_min" in columnas and det.get("runtime"):
                updates["duracion_min"] = det["runtime"]
            if "director" in columnas:
                d = get_director(det)
                if d: updates["director"] = d
            if "precio" in columnas:
                updates["precio"] = precio if precio > 0 else PRECIO_BASE
            if "calificacion_tmdb" in columnas:
                updates["calificacion_tmdb"] = round(float(tmdb.get("vote_average", 0)), 1)
            if "tmdb_id" in columnas and tmdb_id:
                updates["tmdb_id"] = tmdb_id

            if updates:
                set_sql = ", ".join(f"`{k}` = %s" for k in updates)
                with conn.cursor() as cur:
                    cur.execute(f"UPDATE peliculas SET {set_sql} WHERE id = %s",
                                list(updates.values()) + [pid])
                conn.commit()
                poster_ok = "poster_url" in updates
                print(f"  OK | poster={'SI' if poster_ok else 'NO'} | "
                      f"precio={updates.get('precio','--')} | "
                      f"rating={updates.get('calificacion_tmdb','--')} | "
                      f"director={updates.get('director','N/D')}")
                ok += 1
            else:
                print(f"  Sin columnas para actualizar")

            time.sleep(0.25)

    finally:
        conn.close()

    print(f"\nListo. {ok}/{len(peliculas)} peliculas actualizadas.")
    print("Reinicia Reflex: reflex run\n")


if __name__ == "__main__":
    main()
