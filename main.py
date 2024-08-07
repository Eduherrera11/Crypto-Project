# Importaciones necesarias para el funcionamiento del programa
from auth import iniciar_sesion, usuario_existe, guardar_usuario, verificar_usuario, verificar_usuario_recuperacion_contraseña, cifrar_contraseña, generar_token, actualizar_contraseña
from email_utils import enviar_correo, enviar_correo_restauracion, enviar_correo_verificacion
from crypto import obtener_cripto_billetera, crear_stop_profit, comprobar_precios, obtener_precio_criptomoneda, obtener_precios_criptomonedas, obtener_rendimiento, registrar_compra, registrar_compra_manual, actualizar_valor, mostrar_historial, ver_billetera, ver_liquidez, calcular_precio_deseado, comprobar_precios_continuamente
from db import DBConnection
import time
import schedule

### FLUJO DEL PROGRAMA ###



def menu_inicio_sesion():
    while True:
        # Menu principal de inicio de sesion y registro
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
                verificar = str(input("Deseas reestablecer tu contraseña? Si/No\n:"))
                if verificar.title() in ["N", "No"]:
                    print("Vuelve a intentarlo.")
                elif verificar.title() in ["S", "Si"]:
                    email = str(input("Ingresa tu correo: "))
                    with DBConnection() as cursor: 
                        query = "select correo from usuarios"
                        cursor.execute(query)
                        resultado = cursor.fetchall()
                        resultados = list(i[0] for i in resultado)
                        if email in resultados:
                            token_verificacion = generar_token()
                            enviar_correo_restauracion(email, token_verificacion)
                            print("Te hemos enviado un correo electronico con un token de verificacion.")

                            # Proceso de verificacion

                            token = input("Inroduce el codigo de verificacion que recibiste: ")

                            if token_verificacion == token:
                                nueva_contraseña = str(input("Escribe la nueva contraseña: "))
                                actualizar_contraseña(email, nueva_contraseña)
                                print("Contraseña actualizada con exito!")
                            else:
                                print("Codigo de verificacion incorrecto.")
                        else:
                            print("El correo que ingresaste no esta en la base de datos. Registrate")

        elif usuario.title() in ["2", "Registrar", "Registrase"]:
            # Registro de usuario
            correo = input("Introduce tu correo electronico: ")
            contraseña = input("Introduce tu contraseña: ")
            contraseña_cifrada = cifrar_contraseña(contraseña)
            token_verificacion = generar_token()

            guardar_usuario(correo, contraseña_cifrada, token_verificacion)
            enviar_correo_verificacion(correo, token_verificacion)

            print("Te hemos enviado un correo electronico con un token de verificacion.")

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



def menu_cripto(correo):
    while True:
        # Menu principal para gestion de criptomonedas
        menu = str(input("1. Obtener precio de una criptomoneda\n2. Comprar Cripto\n3. Ver billetera\n4. Ver historial de compra\n5. Liquidez total\n6. Ver Criptomoneda en billetera\n7. Rendiemiento total de la inversion\n8. Calcular precio deseado\n9. Poner Targets De Stop Profit\n10. Analisis De Stop Profit\n11. Analisis Continuo De Stop\n12. Salir\n->  "))

        if menu.title() in ["1", "Obtener", "Obtener precio de una criptomoneda"]:
            # Obtener el precio de una criptomoneda especifica
            criptomoneda = str(input("Selecciona el nombre de la criptomoneda que deseas observar: "))
            valor = obtener_precio_criptomoneda(criptomoneda)
            if valor:
                print(f"El precio de {criptomoneda.title()} es {valor} usdt")

        elif menu.title() in ["2", "Comprar", "Comprar Crypto"]:
            while True:
                # Menu para comprar criptomonedas
                opcion = str(input("1. Comprar al precio actual\n2. Comprar a un precio determinado\n3. Ir atras\n->  "))

                if opcion.title() in ["1", "Comprar Al Precio Actual", "Actual"]:
                    criptomoneda = str(input("Selecciona la cripto que deseas comprar: "))
                    cantidad = str(input(f"Selecciona la cantidad a comprar de {criptomoneda}: "))
                    with DBConnection() as cursor: 
                        query = "select id from usuarios where correo like %s"
                        cursor.execute(query, (correo,))
                        resultado = cursor.fetchone()
                        id = resultado[0]
                        registrar_compra(id, criptomoneda, cantidad)

                elif opcion.title() in ["2", "Comprar Al Precio Determinado", "Determinado"]:
                    criptomoneda = str(input("Selecciona la cripto que deseas comprar: "))
                    cantidad = str(input(f"Selecciona la cantidad a comprar de {criptomoneda}: "))
                    precio = str(input(f"Selecciona el precio de compra de la cripto: "))
                    with DBConnection() as cursor: 
                        query = "select id from usuarios where correo like %s"
                        cursor.execute(query, (correo,))
                        resultado = cursor.fetchone()
                        id = resultado[0]
                        registrar_compra_manual(id, criptomoneda, cantidad, precio)
                
                elif opcion.title() in ["3", "S", "Salir"]:
                    print("Regresando...")
                    break

                else:
                    print("Selecione una opcion valida!")

        elif menu.title() in ["3", "Ver", "Ver Billetera"]:
            # Ver el contenido de la billetera del usuario
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                actualizar_valor()
                print("Obteniendo resultados...")
                ver_billetera(id)            

        elif menu.title() in ["4", "Ver", "Ver Historial De Compra"]:
            # Ver el historial de compras del usuario
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                actualizar_valor()
                print("Obteniendo resultados...")
                mostrar_historial(id)

        elif menu.title() in ["5", "Liquidez"]:
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                actualizar_valor()
                print("Obteniendo resultados...") 
                ver_liquidez(id)

        elif menu.title() in ["6", "Ver Criptomoneda En Billetera"]:
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                criptomoneda = str(input("Selecciona la cripto que deseas ver en tu billetera: "))
                actualizar_valor()
                print("Obteniendo resultados...")
                obtener_cripto_billetera(id, criptomoneda)

        elif menu.title() in ["7", "Rendimiento", "Rendimiento Total De La Inversion"]:
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                actualizar_valor()
                print("Obteniendo resultados...") 
                obtener_rendimiento(id)

        elif menu.title() in ["8", "Calcular", "Calcular Precio Deseado"]:
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                criptomoneda = str(input("Selecciona la cripto que deseas ver en tu billetera: "))
                precio = float(input(f"Selecciona el precio al que crees que podra cotizar {criptomoneda}: "))
                print("Obteniendo resultados...") 
                calcular_precio_deseado(id, criptomoneda, precio)


        elif menu.title() in ["9", "Poner", "Poner Targets De Stop Profit"]: 
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                actualizar_valor()
                print("Obteniendo resultados...")
                global target_list 
                target_list = crear_stop_profit(id)

        elif menu.title() in ["10", "Analisis", "Analisis De Stop Profit"]: 
            with DBConnection() as cursor: 
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                actualizar_valor()
                print("Obteniendo resultados...")
                comprobar_precios(id, correo, target_list)

        elif menu.title() in ["11", "Analisis Continuo", "Analisis Continuo De Stop"]:
            with DBConnection() as cursor:
                query = "select id from usuarios where correo like %s"
                cursor.execute(query, (correo,))
                resultado = cursor.fetchone()
                id = resultado[0]
                actualizar_valor()
                print("Obteniendo resultados...")
                interval = int(input("Ingrese el intervalo en segundos para comprobar los precios: "))
                print("La comprobación continua de precios ha comenzado. Presiona Ctrl+C para detener.")

                try:
                    while True:
                        comprobar_precios_continuamente(id, correo, target_list, interval)
                except KeyboardInterrupt:
                    print("Deteniendo la comprobacion continua de precios...")
                    break

        elif menu.title() in ["12", "S", "Salir"]:
            print("Saliendo del programa")
            break

        else:
            print("Selecione una opcion valida!")



if __name__ == "__main__":
    menu_inicio_sesion()