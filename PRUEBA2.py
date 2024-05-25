import requests

def geocode_city(api_key, city_name):
    url = 'https://graphhopper.com/api/1/geocode'
    params = {
        'key': api_key,
        'q': city_name,
        'limit': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(f"Respuesta de la API de geocodificación para {city_name}: {data}")  # Mensaje de depuración
    if 'hits' in data and data['hits']:
        lat = data['hits'][0]['point']['lat']
        lng = data['hits'][0]['point']['lng']
        return f"{lat},{lng}"
    else:
        print(f"Error: No se encontraron resultados para {city_name}.")
        return None

def get_directions(api_key, from_city, to_city):
    url = 'https://graphhopper.com/api/1/route'
    params = {
        'key': api_key,
        'point': [from_city, to_city],
        'type': 'json',
        'vehicle': 'car',
        'locale': 'es',
        'instructions': 'true',
        'calc_points': 'true'
    }
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error de solicitud: {err}")
        return None

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def main():
    graphhopper_api_key = 'f5817c60-a0f4-4b41-ba64-0e526bbe2c3f'  # Reemplaza esto con tu token de GraphHopper

    while True:
        print("\nIngrese 'q' en cualquier momento para salir.")
        from_city_name = input("Ciudad de Origen: ")
        if from_city_name.lower() == 'q':
            break
        to_city_name = input("Ciudad de Destino: ")
        if to_city_name.lower() == 'q':
            break

        from_city_coords = geocode_city(graphhopper_api_key, from_city_name)
        to_city_coords = geocode_city(graphhopper_api_key, to_city_name)

        if not from_city_coords or not to_city_coords:
            print("Error al obtener las coordenadas. Por favor, intente nuevamente.")
            continue

        data = get_directions(graphhopper_api_key, from_city_coords, to_city_coords)

        if not data or 'paths' not in data:
            print("Error al obtener los datos de GraphHopper. Por favor, intente nuevamente.")
            continue

        path = data['paths'][0]
        distance_km = path['distance'] / 1000  # Convertir metros a kilómetros
        formatted_distance = f"{distance_km:.2f} km"

        time_seconds = path['time'] / 1000  # Convertir milisegundos a segundos
        formatted_time = format_time(time_seconds)

        Asumiendo un consumo de combustible promedio de 8 litros cada 100 km
        fuel_used = (distance_km / 100) * 8
        formatted_fuel = f"{fuel_used:.2f} L"

        instructions = path['instructions']
        narrative = "\n".join([instr['text'] for instr in instructions])

        print(f"\nDistancia: {formatted_distance}")
        print(f"Duración del viaje: {formatted_time}")
        print(f"Combustible requerido: {formatted_fuel}")
        print(f"Narrativa del viaje:\n{narrative}")

if _name_ == "__main__":
    main()