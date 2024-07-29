import folium
from folium.plugins import HeatMap
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns

def create_map(places, city):
    if not places:
        raise ValueError("No places to create a map")

    df = pd.DataFrame(places)
    df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
    df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])

    first_place = places[0]
    location = [first_place['geometry']['location']['lat'], first_place['geometry']['location']['lng']]
    m = folium.Map(location=location, zoom_start=13)

    for place in places:
        folium.Marker(
            [place['geometry']['location']['lat'], place['geometry']['location']['lng']],
            popup=f"<b>{place['name']}</b><br>Rating: {place['rating']}<br>Reviews: {place['user_ratings_total']}"
        ).add_to(m)
    
    map_path = f'static/{city}_map.html'
    m.save(map_path)
    return map_path

def create_average_rating_heatmap(places, city):
    if not places:
        raise ValueError("No places to create a heatmap")

    df = pd.DataFrame(places)
    df = df[df['user_ratings_total'] >= 50]
    df = df.nlargest(300, 'rating')
    df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
    df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])
    df['weight'] = df['rating']

    location = [df['lat'].mean(), df['lng'].mean()]
    m = folium.Map(location=location, zoom_start=13)
    
    heat_data = [[row['lat'], row['lng'], row['weight']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(m)
    
    map_path = f'static/{city}_average_rating_heatmap.html'
    m.save(map_path)
    return map_path

def create_ratings_distribution_chart(places, city):
    if not places:
        raise ValueError("No places to create a ratings distribution chart")

    df = pd.DataFrame(places)
    df = df[df['user_ratings_total'] >= 50]
    df = df.nlargest(300, 'rating')

    plt.figure(figsize=(10, 6))
    sns.histplot(df['rating'], bins=10, kde=True)
    plt.title(f'Ratings Distribution of Top 300 Places in {city}')
    plt.xlabel('Rating')
    plt.ylabel('Count')

    plot_path = f'static/{city}_ratings_distribution.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

def get_top_n_places(places, n=15):
    df = pd.DataFrame(places)
    df = df[df['user_ratings_total'] > 300] 
    df = df[['name', 'geometry', 'rating', 'user_ratings_total']]
    df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
    df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])
    top_n = df.nlargest(n, 'rating')
    return top_n.to_dict(orient='records')
