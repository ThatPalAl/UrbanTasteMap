import googlemaps
from time import sleep
import itertools

def get_bounding_boxes(city_center, radius_km, grid_size):
    lat, lng = city_center
    d_lat = radius_km / 111  
    d_lng = radius_km / (111 * abs(lat))  

    latitudes = [lat + i * d_lat for i in range(-grid_size, grid_size + 1)]
    longitudes = [lng + i * d_lng for i in range(-grid_size, grid_size + 1)]

    boxes = []
    for (lat1, lng1), (lat2, lng2) in itertools.product(
        zip(latitudes, longitudes), zip(latitudes[1:], longitudes[1:])
    ):
        boxes.append([(lat1, lng1), (lat2, lng2)])

    return boxes

def get_google_places(api_key, city_center, radius_km, grid_size, place_type):
    gmaps = googlemaps.Client(key=api_key)
    boxes = get_bounding_boxes(city_center, radius_km, grid_size)
    all_places = []

    for box in boxes:
        (lat1, lng1), (lat2, lng2) = box
        location = ((lat1 + lat2) / 2, (lng1 + lng2) / 2)
        query = f"{place_type} in {city_center}"
        places = []

        response = gmaps.places_nearby(location=location, radius=radius_km*1000, keyword=place_type)
        places.extend(response.get('results', []))

        while 'next_page_token' in response:
            sleep(2)  
            response = gmaps.places_nearby(location=location, radius=radius_km*1000, keyword=place_type, page_token=response['next_page_token'])
            places.extend(response.get('results', []))

        all_places.extend(places)

    return all_places

def filter_places_by_reviews(places, min_reviews=50):
    return [place for place in places if place.get('user_ratings_total', 0) >= min_reviews]
