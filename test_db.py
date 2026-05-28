import sys, os
from dotenv import load_dotenv
load_dotenv()

print("DB_PASSWORD:", repr(os.getenv("DB_PASSWORD")))
print("DB_USER:", repr(os.getenv("DB_USER")))

from utils.db import query
try:
    rows = query("SELECT COUNT(*) AS total FROM peliculas")
    print("✅ BD conectada —", rows[0]["total"], "películas")
except Exception as e:
    print("❌ Error de conexión:", e)