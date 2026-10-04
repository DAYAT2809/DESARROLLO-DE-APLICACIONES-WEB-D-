import os
import mysql.connector
import psycopg2
from psycopg2.extras import RealDictCursor


def obtener_conexion():

    database_url = os.getenv("DATABASE_URL")

    # En Render se utilizará PostgreSQL
    if database_url:
        return psycopg2.connect(
            database_url,
            cursor_factory=RealDictCursor
        )

    # En local se utilizará MySQL
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NuevaClave123!",
        database="girls"
    )


def obtener_cursor(conexion):

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return conexion.cursor()

    return conexion.cursor(dictionary=True)