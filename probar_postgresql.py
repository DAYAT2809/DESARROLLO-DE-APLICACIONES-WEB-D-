import os
import psycopg2

url = os.getenv("DATABASE_URL")

if not url:
    print("NO EXISTE DATABASE_URL")
else:
    try:
        conexion = psycopg2.connect(url)
        print("CONEXIÓN EXITOSA CON POSTGRESQL")
        conexion.close()
    except Exception as e:
        print("ERROR:", e)