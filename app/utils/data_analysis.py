import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import DBSCAN
import numpy as np

def analyze_and_plot(places, city):
    df = pd.DataFrame(places)
    df = df[['name', 'geometry', 'rating', 'user_ratings_total']]
    df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
    df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])


    coords = df[['lat', 'lng']].to_numpy()
    db = DBSCAN(eps=0.01, min_samples=5).fit(coords)
    labels = db.labels_

    df['cluster'] = labels

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='lng', y='lat', hue='cluster', palette='viridis', s=100)
    plt.title(f'{city} Clustering of {len(df)} Places')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    

    plt.savefig(f'app/static/{city}_analysis.png')
    plt.close()

    cluster_summary = df.groupby('cluster').agg({
        'name': 'count',
        'rating': 'mean',
        'user_ratings_total': 'sum'
    }).rename(columns={'name': 'count', 'rating': 'avg_rating', 'user_ratings_total': 'total_reviews'})

    cluster_summary = cluster_summary.to_dict(orient='index')

    return cluster_summary

import pandas as pd

def get_top_n_places(places, n=10):
    df = pd.DataFrame(places)
    df = df[['name', 'geometry', 'rating', 'user_ratings_total']]
    df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
    df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])
    top_n = df.nlargest(n, 'rating')
    return top_n.to_dict(orient='records')
