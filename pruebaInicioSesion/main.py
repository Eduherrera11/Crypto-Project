# Prueba de envio de correo electronico con token de verificacion
import uuid
import bcrypt
import mysql.connector
import smtplib
from email.mime.text import MIMEText

# Conexion a la base de datos
conexion = mysql.connector.connect(
    user="root",
    host="localhost",
    password="Eduherrera11",
    database="proyecto_crypto")

def generar_token():
    return str(uuid.uuid4())

def cifrar_contraseña(contraseña):
    return bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

def guardar_usuario(correo, contraseña_cifrada, token_verificacion):
    cursor = conexion.cursor()
    query = 'insert into usuarios(correo, contraseña, username, token_verificacion, verificado) values(%s, %s, %s, %s, %s)'
    cursor.execute(query, (correo, contraseña_cifrada, correo.split('@')[0], token_verificacion, False))
    conexion.commit()

def enviar_correo_verificacion(correo, token_verificacion):
    mensaje = MIMEText(f"Por favor verifica tu correo usando este codigo: {token_verificacion}")
    mensaje["Subject"] = 'Verificacion de Correo'
    mensaje["From"] = 'eduardo.pruebaserver@gmail.com'
    mensaje["To"] = correo

    servidor = smtplib.SMTP('smpt.gamil.com', 587)
    servidor.starttls()
    servidor.login("eduardo.pruebaserver@gmail.com", "pruebasServer")
    servidor.sendmail("eduardo.pruebaserver@gmail.com", correo, mensaje.as_string())
    servidor.quit()

# Registro de usuario
correo = input("Introduce tu correo electronico: ")
contraseña = input("Introduce tu contraseña: ")
contraseña_cifrada = cifrar_contraseña(contraseña)
token_verificacion = generar_token()

guardar_usuario(correo, contraseña_cifrada, token_verificacion)
enviar_correo_verificacion(correo, token_verificacion)

print("Te hemos enviado un correo electronico con un token de verificacion.")

def verificar_usuario(correo, token):
    cursor = conexion.cursor()
    query = "select token_verificacion from usuarios where correo = %s"
    cursor.execute(query, (correo,))
    resultado = cursor.fetchone()
    if resultado and resultado[0] == token:
        query_update = "update usuarios set verificado where correo = %s"
        cursor.execute(query_update, (True, correo))
        conexion.commit()
        return True
    return False

# Proceso de verificacion
correo = input("Introduce tu correo electronico para verificar: ")
token = input("Inroduce el codigo de verificacion que recibiste: ")

if verificar_usuario(correo, token):
    print("Tu cuenta ha sido verificada con exito.")
else:
    print("Codigo de verificacion incorrecto.")



