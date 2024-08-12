import uuid
import bcrypt
from Cryptos.scripts.db import DBConnection

# Generando codigo
def generar_token():
    return str(uuid.uuid4())

# Funcion para guardar las contraseñas de los usuarios cifradas 
def cifrar_contraseña(contraseña):
    return bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

def usuario_existe(correo):
    with DBConnection() as cursor:
        query = "SELECT id FROM usuarios WHERE correo = %s"
        cursor.execute(query, (correo,))
        resultado = cursor.fetchone()
        return resultado is not None

def guardar_usuario(correo, contraseña_cifrada, token_verificacion):
    with DBConnection() as cursor:
        query = 'insert into usuarios(correo, contraseña, username, token_verificacion, verificado) values(%s, %s, %s, %s, %s)'
        cursor.execute(query, (correo, contraseña_cifrada, correo.split('@')[0], token_verificacion, False))

def verificar_usuario(correo, token):
    with DBConnection() as cursor:
        query = "select token_verificacion from usuarios where correo = %s"
        cursor.execute(query, (correo,))
        resultado = cursor.fetchone()
        if resultado and resultado[0] == token:
            query_update = "update usuarios set verificado = %s where correo = %s"
            cursor.execute(query_update, (True, correo))
            return True
        return False
    
def verificar_usuario_recuperacion_contraseña(correo, token):
    with DBConnection() as cursor:
        query = "select token_restauracion from usuarios where correo = %s"
        cursor.execute(query, (correo,))
        resultado = cursor.fetchone()
        if resultado and resultado[0] == token:
            query_update = "update usuarios set verificado = %s where correo = %s"
            cursor.execute(query_update, (True, correo))
            return True
        return False
    
def actualizar_contraseña(correo, contraseña):
    with DBConnection() as cursor:
        new_password = cifrar_contraseña(contraseña)
        query = "update usuarios set contraseña = %s where correo = %s"
        cursor.execute(query, (new_password, correo))
        print(f"Contraseña actualizada para el correo: {correo}")

def iniciar_sesion(correo, contraseña):
    try:
        # Iniciar la conexion de la base de datos / Start database connection
        with DBConnection() as cursor:
            query = "select id, contraseña from usuarios where correo = %s and verificado = %s"
            cursor.execute(query, (correo, True))
            resultado = cursor.fetchone()
            if resultado and bcrypt.checkpw(contraseña.encode('utf-8'), resultado[1].encode('utf-8')):
                return resultado[0]
            return None
        
    except Exception as e:
        # Manejar excepciones generales / Handle general exceptions
        print(f"Ocurrio un error durante el inicio de sesion: {e}")
        return None