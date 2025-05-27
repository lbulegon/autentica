import googlemaps

import openrouteservice
from openrouteservice import convert


def calcular_rota_google(enderecos, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    origem = enderecos[0]
    destino = enderecos[-1]
    waypoints = enderecos[1:-1]  # intermediários

    rota = gmaps.directions(
        origem,
        destino,
        waypoints=waypoints,
        optimize_waypoints=True,
        mode="driving"
    )
    
    return rota


def calcular_rota_ors(coordenadas, api_key):
    client = openrouteservice.Client(key=api_key)
    
    rota = client.directions(
        coordinates=coordenadas,
        profile='driving-car',
        optimize_waypoints=True
    )
    
    return rota



# Substitua com sua API Key do OpenRouteService
ORS_API_KEY = 'SUA_API_KEY'

client = openrouteservice.Client(key=ORS_API_KEY)

def calcular_rota_e_tempo(pedidos):
    """
    Calcula a rota ótima e o tempo estimado usando OpenRouteService.

    pedidos: queryset ou lista de IfoodWebhookEvent com endereço e coordenadas.
    """

    # Aqui supomos que os pedidos possuem latitude e longitude.
    coordenadas = []
    for pedido in pedidos:
        if pedido.latitude and pedido.longitude:
            coordenadas.append((pedido.longitude, pedido.latitude))
        else:
            raise ValueError(f"Pedido {pedido.id} sem coordenadas.")

    if len(coordenadas) < 2:
        return "Precisa de pelo menos 2 pontos para roteirização."

    # Calcula rota
    rota = client.directions(
        coordinates=coordenadas,
        profile='driving-car',
        format='geojson'
    )

    distancia_total = rota['features'][0]['properties']['summary']['distance'] / 1000  # km
    duracao_total = rota['features'][0]['properties']['summary']['duration'] / 60  # minutos

    return {
        'distancia_km': round(distancia_total, 2),
        'duracao_min': round(duracao_total, 2),
        'rota_geojson': rota
    }
