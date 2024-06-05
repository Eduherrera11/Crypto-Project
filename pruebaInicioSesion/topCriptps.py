import requests
import json

def obtener_top_criptomonedas(limite=500):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    criptomonedas = []

    # Hacer solicitudes en páginas de 250 resultados cada una
    paginas = (limite // 250) + (1 if limite % 250 != 0 else 0)
    for pagina in range(1, paginas + 1):
        parametros = {
            'vs_currency': 'usd',  # Moneda base (puedes cambiarla a otra, como 'eur', 'btc', etc.)
            'order': 'market_cap_desc',  # Ordenar por capitalización de mercado descendente
            'per_page': 250,  # Número de resultados por página
            'page': pagina,  # Página actual
            'sparkline': 'false'  # Sin datos de sparkline
        }
        response = requests.get(url, params=parametros)
        if response.status_code == 200:
            datos = response.json()
            criptomonedas.extend(datos)
        else:
            print(f"Error al obtener las criptomonedas en la página {pagina}: ", response.json())
            return None
    
    return criptomonedas[:limite]

# Ejemplo de uso:
top_criptomonedas = obtener_top_criptomonedas(500)
if top_criptomonedas:
    # Guardar en un archivo JSON
    with open('top_criptomonedas.json', 'w') as file:
        json.dump(top_criptomonedas, file, indent=4)
    print("Las primeras 500 criptomonedas se han guardado en 'top_criptomonedas.json'.")
else:
    print("No se pudieron obtener las criptomonedas.")
