import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from db import DBConnection

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def enviar_correo(correo, asunto, mensaje):
    mensaje = MIMEText(mensaje)
    mensaje["Subject"] = asunto
    mensaje["From"] = 'eduardo.pruebasserver@gmail.com'
    mensaje["To"] = correo

    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login("eduardo.pruebasserver@gmail.com", os.getenv("EMAIL_PASSWORD"))
    servidor.sendmail("eduardo.pruebasserver@gmail.com", correo, mensaje.as_string())
    servidor.quit()

def enviar_correo_verificacion(correo, token_verificacion):
    mensaje = f"Por favor verifica tu correo usando este codigo: {token_verificacion}"
    enviar_correo(correo, "Verificacion de Correo", mensaje)

def enviar_correo_restauracion(correo, token_restauracion):
    # Actualizar el token en la base de datos
    query_update_token = "UPDATE usuarios SET token_restauracion = %s WHERE correo = %s"
    
    with DBConnection() as cursor:
        cursor.execute(query_update_token, (token_restauracion, correo))

    mensaje = f"Has pedido reestablecer tu contraseña en el programa de criptomonedas de la terminal, por favor ingresa este codigo: {token_restauracion}"  
    enviar_correo(correo, "Correo de restauracion de contraseña", mensaje)