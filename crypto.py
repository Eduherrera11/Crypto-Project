import requests
from datetime import datetime
import prettytable as tb
from urllib.parse import quote
import os 
from db import DBConnection, DBConnection2
from email_utils import enviar_correo
import time

# Conexion a la api de CoinGecko
# Lista de criptomonedas 
def obtener_precios_criptomonedas(nombres):
    nombres_codificados = [quote(nombre) for nombre in nombres]
    ids = ",".join(nombres_codificados)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener precios de las criptomonedas: {response.status_code} - {response.text}")
        return None

def obtener_precio_criptomoneda(nombre):
    nombre_codificado = quote(nombre)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={nombre_codificado}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        if nombre_codificado in datos:
            return datos[nombre_codificado]["usd"]
        else:
            print(f"No se encontraron datos para la criptomoneda: {nombre}")
            return None
    else:
        print(f"Error al obtener precio de la criptomoneda: {response.status_code} - {response.text}")
        return None
    
# Funcion para registrar una compra de una cripto al precio actual   
def registrar_compra(usuario_id, criptomoneda, cantidad):
    precio_compra = obtener_precio_criptomoneda(criptomoneda)
    if precio_compra is not None:
        with DBConnection() as cursor:
            query = 'insert into inversiones(usuario_id, criptomoneda, cantidad, precio_actual, precio_compra, fecha) values(%s, %s, %s, %s, %s, %s)'
            fecha_compra = datetime.now()
            cursor.execute(query, (usuario_id, criptomoneda, cantidad, precio_compra, precio_compra, fecha_compra))
            print("Compra registrada con exito.")
    else:
        print("No se pudo obtener el precio de la criptomoneda.")

def registrar_compra_manual(usuario_id, criptomoneda, cantidad, precio_compra):
    precio_actual = obtener_precio_criptomoneda(criptomoneda)
    if precio_compra is not None:
        with DBConnection() as cursor:
            query = 'insert into inversiones(usuario_id, criptomoneda, cantidad, precio_actual, precio_compra, fecha) values(%s, %s, %s, %s, %s, %s)'
            fecha_compra = datetime.now()
            cursor.execute(query, (usuario_id, criptomoneda, cantidad, precio_actual, precio_compra, fecha_compra))
            print("Compra registrada con exito.")
    else:
        print("No se pudo obtener el precio de la criptomoneda.")

def actualizar_valor():
    with DBConnection() as cursor:   
        query = "SELECT id, criptomoneda, cantidad FROM inversiones"
        cursor.execute(query)
        inversiones = cursor.fetchall()

        criptomonedas = set(inversion[1] for inversion in inversiones)
        precios = obtener_precios_criptomonedas(list(criptomonedas))
        
        # Diccionario para almacenar precios ya obtenidos
        precios_cache = {}

        if precios:
            for inversion in inversiones:
                id, criptomoneda, cantidad = inversion

                # Verificar si ya se ha obtenido el precio de esta criptomoneda
                if criptomoneda in precios_cache:
                    precio_actual = precios_cache[criptomoneda]
                else:
                    precio_actual = precios.get(quote(criptomoneda), {}).get("usd")
                    if precio_actual is not None:
                        precios_cache[criptomoneda] = precio_actual

                if precio_actual is not None:
                    query_update = "UPDATE inversiones SET precio_actual = %s WHERE id = %s"
                    cursor.execute(query_update, (precio_actual, id))

def mostrar_historial(id):
    with DBConnection() as cursor:  
        query = "select id, criptomoneda, cantidad, precio_actual, precio_compra, fecha from inversiones where usuario_id = %s"
        cursor.execute(query, (id,))
        inversiones = cursor.fetchall()

        if inversiones:
            tabla = tb.PrettyTable()
            tabla.field_names = ["Id", "Criptomoneda", "Cantidad", "Precio Actual","Precio compra","Fecha"]
            for inversion in inversiones:
                tabla.add_row(inversion)
            print(tabla)
        else:
            print("No se encontraron inversiones para este usuario.")

def ver_billetera(id):
    with DBConnection() as cursor: 
        query = """select criptomoneda, sum(cantidad) as cantidad, (sum(precio_actual)/(count(precio_actual))) as precio_actual, 
        ((sum(cantidad))*(sum(precio_actual)/(count(precio_actual)))) as liquidez,
        ((SUM(cantidad) * precio_actual) - SUM(cantidad * precio_compra)) / SUM(cantidad * precio_compra) * 100 AS ganancia_perdida_porcentaje
        from inversiones where usuario_id = %s group by criptomoneda, precio_actual"""
        cursor.execute(query, (id,))
        inversiones = cursor.fetchall()

        if inversiones:
            tabla = tb.PrettyTable()
            tabla.field_names = ["Criptomoneda", "Cantidad", "Precio Actual","Liquidez","Redimiento (%)"]
            for inversion in inversiones:
                tabla.add_row(inversion)
            print(tabla)
        else:
            print("No se encontraron inversiones para este usuario.")
    

def ver_liquidez(id):
    with DBConnection() as cursor: 
        query = """select sum(cantidad*precio_actual) as liquidez from inversiones where usuario_id = %s;"""
        cursor.execute(query, (id,))
        inversiones = cursor.fetchall()

        if inversiones:
            tabla = tb.PrettyTable()
            tabla.field_names = ["Liquidez"]
            for inversion in inversiones:
                tabla.add_row(inversion)
            print(tabla)
        else:
            print("No se encontraron inversiones para este usuario.")

def obtener_cripto_billetera(id, criptomoneda):
    with DBConnection() as cursor:
        query = """SELECT 
                        criptomoneda,
                        SUM(cantidad) AS cantidad_total,
                        AVG(precio_actual) AS precio_actual,
                        SUM(cantidad) * AVG(precio_actual) AS liquidez,
                        ((SUM(cantidad) * AVG(precio_actual)) - SUM(cantidad * precio_compra)) / SUM(cantidad * precio_compra) * 100 AS ganancia_perdida_porcentaje
                    FROM 
                        inversiones
                    WHERE 
                        usuario_id = %s AND criptomoneda = %s
                    GROUP BY 
                        criptomoneda;"""
        cursor.execute(query, (id, criptomoneda))
        inversiones = cursor.fetchall()

        if inversiones:
            tabla = tb.PrettyTable()
            tabla.field_names = ["Criptomoneda", "Cantidad", "Precio Actual","Liquidez","Redimiento (%)"]
            for inversion in inversiones:
                tabla.add_row(inversion)
                print(tabla)
            else:
                print("No se encontraron inversiones para este usuario.")

def calcular_precio_deseado(id, criptomoneda, precio):
    with DBConnection() as cursor:
        query = """call calcular_precio_deseado(%s, %s, %s)"""
        cursor.execute(query, (precio, id, criptomoneda))
        inversiones = cursor.fetchall()

        if inversiones:
            tabla = tb.PrettyTable()
            tabla.field_names = ["Criptomoneda", "Cantidad", "Precio Deseado","Liquidez","Redimiento (%)"]
            for inversion in inversiones:
                tabla.add_row(inversion)
            print(tabla)
        else:
            print("No se encontraron inversiones para este usuario.")

def obtener_rendimiento(id):
    with DBConnection() as cursor:
        query = '''select (sum(precio_actual*cantidad) - sum(precio_compra*cantidad)) as Rendimiento_de_inversion, 
                (sum(precio_actual*cantidad) - sum(precio_compra*cantidad))/(sum(precio_compra*cantidad))*100 as "%" from inversiones where usuario_id = %s;'''
        cursor.execute(query, (id,))
        inversiones = cursor.fetchall()

        if inversiones:
            tabla = tb.PrettyTable()
            tabla.field_names = ["Rendimiento de Inversion", "%"]
            for inversion in inversiones:
                tabla.add_row(inversion)
            print(tabla)
        else:
            print("No se encontraron inversiones para este usuario.")

def comprobar_precios(id, correo, target_list):
    with DBConnection2() as cursor: 
        query = """select criptomoneda, sum(cantidad) as cantidad, (sum(precio_actual)/(count(precio_actual))) as precio_actual, 
        ((sum(cantidad))*(sum(precio_actual)/(count(precio_actual)))) as liquidez,
        ((SUM(cantidad) * precio_actual) - SUM(cantidad * precio_compra)) / SUM(cantidad * precio_compra) * 100 AS ganancia_perdida_porcentaje
        from inversiones where usuario_id = %s group by criptomoneda, precio_actual"""
        cursor.execute(query, (id,))
        inversiones = cursor.fetchall()

        # Asegúrate de que la longitud de inversiones y target_list sea la misma
        if len(inversiones) != len(target_list):
            raise ValueError("La longitud de inversiones y target_list debe ser la misma")

        for inversion, target in zip(inversiones, target_list):
            if float(inversion["precio_actual"]) > target:
                asunto = f"Alerta de precio crypto: {inversion["criptomoneda"]}"
                mensaje = f"El precio de {inversion["criptomoneda"]} ha alcanzado los {inversion["precio_actual"]} usdt, que es mayor o igual a tu precio objetivo de {target} usdt."
                enviar_correo(correo, asunto, mensaje)
                print(f"La cripto {inversion["criptomoneda"]} ha alcanzado su target")
            else:
                pass

def comprobar_precios_continuamente(id, correo, target_list, interval=15):
    while True:
        comprobar_precios(id, correo, target_list)
        time.sleep(interval)


def crear_stop_profit(id):
    with DBConnection2() as cursor: 
        query = """select criptomoneda, sum(cantidad) as cantidad, (sum(precio_actual)/(count(precio_actual))) as precio_actual, 
        ((sum(cantidad))*(sum(precio_actual)/(count(precio_actual)))) as liquidez,
        ((SUM(cantidad) * precio_actual) - SUM(cantidad * precio_compra)) / SUM(cantidad * precio_compra) * 100 AS ganancia_perdida_porcentaje
        from inversiones where usuario_id = %s group by criptomoneda, precio_actual"""
        cursor.execute(query, (id,))
        inversiones = cursor.fetchall()

        target_list = []

        for inversion in inversiones:
            target = float(input(f"Selecciona el stop profit de la criptomoneda {inversion["criptomoneda"]}: "))
            target_list.append(target)

    print(target_list)
    return target_list

            