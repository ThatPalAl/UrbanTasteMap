import logging
from app.celery import celery
from app.utils.google_places import get_google_places, filter_places_by_reviews
from app.utils.map_creation import create_map, create_average_rating_heatmap, create_ratings_distribution_chart, get_top_n_places

@celery.task(bind=True)
def process_places(self, api_key, city_center, radius_km, grid_size, place_type, city):
    logging.info(f'Starting process_places for {city} with place type {place_type}')
    try:
    
        logging.info('Fetching places from Google Places API')
        places = get_google_places(api_key, city_center, radius_km, grid_size, place_type)
        logging.info(f'Fetched {len(places)} places')
        

        logging.info('Filtering places by reviews')
        places_filtered = filter_places_by_reviews(places)
        logging.info(f'Filtered places, {len(places_filtered)} remaining')

        places_filtered = [p for p in places_filtered if p['user_ratings_total'] >= 50]
        places_filtered = sorted(places_filtered, key=lambda x: x['rating'], reverse=True)[:300]

        logging.info('Creating map')
        map_path = create_map(places_filtered, city)
        logging.info(f'Map created at {map_path}')
        
        logging.info('Creating heatmap')
        heatmap_path = create_average_rating_heatmap(places_filtered, city)
        logging.info(f'Heatmap created at {heatmap_path}')
        
        logging.info('Creating ratings distribution chart')
        ratings_distribution_path = create_ratings_distribution_chart(places_filtered, city)
        logging.info(f'Ratings distribution chart created at {ratings_distribution_path}')

    
        top_places = get_top_n_places(places_filtered, 15)

        result = {
            'city': city,
            'map_path': map_path.replace('app/', ''), 
            'heatmap_path': heatmap_path.replace('app/', ''),  
            'ratings_distribution_path': ratings_distribution_path.replace('app/', ''),  
            'top_places': top_places
        }
        
        logging.info(f'Task completed successfully for {city}')
        return result

    except Exception as e:
        logging.error(f'Error in process_places: {e}')
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
        raise e
