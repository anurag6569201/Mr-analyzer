import numpy as np
import pandas as pd

movie_df=pd.read_csv('moviesystem/TMDB_model.csv')

poster=movie_df['poster_path']
title=movie_df['title']
overview=movie_df['overview']
date=movie_df['release_date']
runtime=movie_df['runtime']

def movies_details(list):
    movie_ids = list
    movies_datas = []

    for movie_id in movie_ids:
        try:
            movie_data = movie_df.loc[movie_id]
            movies_datas.append(movie_data)
        except KeyError:
            print(f"No movie found with movie_id {movie_id}")

    movies_datas = [movie.to_dict() for movie in movies_datas]
    print(movies_datas[1]['title'])
    # return movies_datas

# movies_details([853, 1269, 772, 3016, 1550, 118, 2554, 1883, 976, 2447])