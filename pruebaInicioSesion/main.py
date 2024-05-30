# Prueba de envio de correo electronico con token de verificacion
import uuid
import bcrypt
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import requests
from datetime import datetime


# Conexion a la base de datos
conexion = mysql.connector.connect(
    user="root",
    host="localhost",
    password="Eduherrera11",
    database="proyecto_crypto")


# Inicio de Sesion
def generar_token():
    return str(uuid.uuid4())

def cifrar_contraseña(contraseña):
    return bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

def usuario_existe(correo):
    cursor = conexion.cursor()
    query = "SELECT id FROM usuarios WHERE correo = %s"
    cursor.execute(query, (correo,))
    resultado = cursor.fetchone()
    return resultado is not None

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

    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login("eduardo.pruebasserver@gmail.com", "usax vjqs aclj agrw")
    servidor.sendmail("eduardo.pruebasserver@gmail.com", correo, mensaje.as_string())
    servidor.quit()

def iniciar_sesion(correo, contraseña):
    cursor = conexion.cursor()
    query = "select id, contraseña from usuarios where correo = %s and verificado = %s"
    cursor.execute(query, (correo, True))
    resultado = cursor.fetchone()
    if resultado and bcrypt.checkpw(contraseña.encode('utf-8'), resultado[1].encode('utf-8')):
        return resultado[0]
    return None

# Analisis de datos Crypto
def obtener_precio_criptomoneda(nombre):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={nombre}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        return datos[nombre]["usd"]
    else:
        print(f"Error al obtener precio de la criptomoneda: ", response.json())
        return None

# Funcion para registrar una compra    
def registrar_compra(usuario_id, criptomoneda, cantidad):
    precio_compra = obtener_precio_criptomoneda(criptomoneda)
    if precio_compra is not None:
        cursor = conexion.cursor()
        query = 'insert into inversiones(usuario_id, criptomoneda, cantidad, precio_actual, precio_compra, fecha) values(%s, %s, %s, %s, %s, %s)'
        fecha_compra = datetime.now()
        cursor.execute(query, (usuario_id, criptomoneda, cantidad, precio_compra, precio_compra, fecha_compra))
        conexion.commit()
        print("Compra registrada con exito.")
    else:
        print("No se pudo obtener el precio de la criptomoneda.")

def registrar_compra_manual(usuario_id, criptomoneda, cantidad, precio_compra):
    precio_actual = obtener_precio_criptomoneda(criptomoneda)
    if precio_compra is not None:
        cursor = conexion.cursor()
        query = 'insert into inversiones(usuario_id, criptomoneda, cantidad, precio_actual, precio_compra, fecha) values(%s, %s, %s, %s, %s, %s)'
        fecha_compra = datetime.now()
        cursor.execute(query, (usuario_id, criptomoneda, cantidad, precio_actual, precio_compra, fecha_compra))
        conexion.commit()
        print("Compra registrada con exito.")
    else:
        print("No se pudo obtener el precio de la criptomoneda.")


def actualizar_valor():
    cursor = conexion.cursor()
    query = "select id, criptomoneda, cantidad, from inversiones"
    cursor.execute(query)
    inversiones = cursor.fetchall()

    for inversion in inversiones:
        id, criptomoneda, cantidad = inversion
        precio_actual = obtener_precio_criptomoneda(criptomoneda)
        if precio_actual is not None:
            query_update = "update inversiones set precio_actual = %s where id = %s"
            cursor.execute(query_update, (precio_actual, id))
            conexion.commit()

def mostrar_billetera(id):
    cursor = conexion.cursor()
    query = "select * from inversiones where usuario_id = %s"
    cursor.execute(query, (id,))
    return cursor.fetchone()

def menu_cripto(correo):
    while True:

        menu = str(input("1. Obtener precio de una criptomoneda\n2. Comprar Cripto\n3. Ver billetera\n4. Salir\n->  "))

        if menu.title() in ["1", "Obtener", "Obtener precio de una criptomoneda"]:
            criptomoneda = str(input("Selecciona el nombre de la criptomoneda que deseas observar: "))
            valor = obtener_precio_criptomoneda(criptomoneda)
            if valor:
                print(f"El precio de {criptomoneda.title()} es {valor} usdt")

        elif menu.title() in ["2", "Comprar", "Comprar Crypto"]:
            while True:
                opcion = str(input("1. Comprar al precio actual\n2. Comprar a un precio determinado\n3. Ir atras\n->  "))

                if opcion.title() in ["1", "Comprar Al Precio Actual", "Actual"]:
                    criptomoneda = str(input("Selecciona la cripto que deseas comprar: "))
                    cantidad = str(input(f"Selecciona la cantidad a comprar de {criptomoneda}: "))
                    cursor = conexion.cursor()
                    query = "select id from usuarios where correo like %s"
                    cursor.execute(query, (correo,))
                    resultado = cursor.fetchone()
                    id = resultado[0]
                    registrar_compra(id, criptomoneda, cantidad)

                elif opcion.title() in ["2", "Comprar Al Precio Determinado", "Determinado"]:
                    criptomoneda = str(input("Selecciona la cripto que deseas comprar: "))
                    cantidad = str(input(f"Selecciona la cantidad a comprar de {criptomoneda}: "))
                    precio = str(input(f"Selecciona el precio de compra de la cripto: "))
                    cursor = conexion.cursor()
                    query = "select id from usuarios where correo like %s"
                    cursor.execute(query, (correo,))
                    resultado = cursor.fetchone()
                    id = resultado[0]
                    registrar_compra_manual(id, criptomoneda, cantidad, precio)
                
                elif menu.title() in ["3", "S", "Salir"]:
                    print("Regresando...")
                    break

                else:
                    print("Selecione una opcion valida!")

        elif menu.title() in ["3", "Ver", "Ver Billetera"]:
            cursor = conexion.cursor()
            query = "select id from usuarios where correo like %s"
            cursor.execute(query, (correo,))
            resultado = cursor.fetchone()
            id = resultado[0]
            billetera = mostrar_billetera(id)
            if billetera:
                print("Obteniendo resultados...")
                print(billetera)
            else:
                print("Ha ocurrido un error")

        
        elif menu.title() in ["4", "S", "Salir"]:
            print("Saliendo del programa")
            break

        else:
            print("Selecione una opcion valida!")


def menu_inicio_sesion():
    while True:

        usuario = input(str("1. Iniciar Sesion\n2. Registrarse\n3. Salir\n->"))

        if usuario.title() in ["1", "Inicio", "Iniciar", "Iniciar Sesion"]:
            # Proceso de inicio de sesion
            correo = input("Introduce tu correo electronico: ")
            contraseña = input("Introduce tu contraseña: ")

            usuario_id = iniciar_sesion(correo, contraseña)
            if usuario_id:
                print("Inicio de sesion exitoso.")
                menu_cripto(correo)
            else:
                print("Correo o contraseña incorrectos o cuenta no verificada.")
        
        elif usuario.title() in ["2", "Registrar", "Registrase"]:
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
                    query_update = "update usuarios set verificado = %s where correo = %s"
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

            
        elif usuario.title() in ["3", "S", "Salir"]:
            print("Terminando inicio de sesion.")
            break

        else:
            print("Selecione una opcion valida!")

menu_inicio_sesion()