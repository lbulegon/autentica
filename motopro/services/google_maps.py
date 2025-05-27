import googlemaps
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def obter_coordenadas(endereco):
    """
    Faz geocoding de um endereço para obter latitude e longitude.
    """
    geocode_result = gmaps.geocode(endereco)
    if not geocode_result:
        raise ValueError("Endereço não encontrado.")
    
    location = geocode_result[0]['geometry']['location']
    return location['lat'], location['lng']

def calcular_rota_google(enderecos):
    """
    Calcula a melhor rota com distância e tempo entre uma sequência de endereços.
    """
    if len(enderecos) < 2:
        raise ValueError("São necessários pelo menos dois endereços para calcular a rota.")

    # Monta a requisição
    origem = enderecos[0]
    destino = enderecos[-1]
    waypoints = enderecos[1:-1] if len(enderecos) > 2 else None

    directions_result = gmaps.directions(
        origin=origem,
        destination=destino,
        waypoints=waypoints,
        mode="driving",
        optimize_waypoints=True
    )

    if not directions_result:
        raise ValueError("Não foi possível calcular a rota.")

    leg = directions_result[0]['legs']
    distancia_total = sum(l['distance']['value'] for l in leg) / 1000  # km
    duracao_total = sum(l['duration']['value'] for l in leg) / 60  # min

    return {
        'distancia_km': round(distancia_total, 2),
        'duracao_min': round(duracao_total, 2),
        'rota_completa': directions_result
    }
