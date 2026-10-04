import os
import mysql.connector
import psycopg2


def obtener_conexion():

    database_url = os.getenv("DATABASE_URL")

    # En Render se utilizará PostgreSQL
    if database_url:
        return psycopg2.connect(database_url)

    # En local se utilizará MySQL
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NuevaClave123!",
        database="girls"
    )