import googlemaps

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
