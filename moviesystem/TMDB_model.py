import pandas as pd
import difflib
import re
# import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movie_df=pd.read_csv('moviesystem/TMDB_model.csv')
# loaded_model_similarity=pickle.load(open('moviesystem/model/dataset5/trained_TMDB.sav','rb'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

selected_features = ['keywords', 'genres', 'title','production_companies','tagline']
for feature in selected_features:
    movie_df[feature] = movie_df[feature].fillna('')
    movie_df[feature] = movie_df[feature].apply(preprocess_text)

movie_df['combined_features'] = movie_df['keywords'] + ' ' + movie_df['genres'] + ' ' + movie_df['title']+ ' ' + movie_df['production_companies'] + ' ' + movie_df['tagline']

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(movie_df['combined_features'])

similarity = cosine_similarity(feature_vectors)

def recommended_movie_ids(text):
    movie_name = text.lower()
    movie_name_processed = preprocess_text(movie_name)
    close_match = difflib.get_close_matches(movie_name_processed, movie_df['title'].str.lower().tolist(),cutoff=0.6)
    if close_match:
        close_match_name = close_match[0]
        for index, title in enumerate(movie_df['title']):
            if title.lower() == close_match_name:
                movie_index = index
                break
    else:
        exit()
    similarity_score = list(enumerate(similarity[movie_index]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:13]
   
    recommended_ids = []
    for i, movie in enumerate(sorted_similar_movies, 1):
        index = movie[0]
        recommended_ids.append(movie_df.loc[index, 'movie_id'])
    return recommended_ids

# -----------------------------------------------
# getting movies outputs as thier dictionary form
# -----------------------------------------------
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
            adjusted_id=movie_id-1
            movie_data = movie_df.loc[adjusted_id]
            movies_datas.append(movie_data)
        except KeyError:
            print(f"No movie found with adjusted_id {adjusted_id}")

    movies_datas = [movie.to_dict() for movie in movies_datas]
    # print(movies_datas[1]['title'])
    return movies_datas

# movies_details([853, 1269, 772, 3016, 1550, 118, 2554, 1883, 976, 2447])