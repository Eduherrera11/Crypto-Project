import os
import mysql.connector
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Conexion a la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Contexto de conexión a la base de datos
class DBConnection:
    def __enter__(self):
        self.conexion = obtener_conexion()
        self.cursor = self.conexion.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conexion.commit()
        self.cursor.close()
        self.conexion.close()

class DBConnection2:
    def __enter__(self):
        self.conexion = obtener_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conexion.commit()
        self.cursor.close()
        self.conexion.close()