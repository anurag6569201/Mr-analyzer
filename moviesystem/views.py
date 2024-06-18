from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import DataUploadForm

from .models import top10alltime
from .TMDB_model import recommended_movie_ids
from .TMDB_model import movies_details

from PIL import Image
import numpy as np
import requests
from io import BytesIO

def get_image_color(image_url):
    url = image_url
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.convert('RGB')
    image_array = np.array(image)
    pixels = image_array.reshape(-1, 3)

    # Get the most frequent color
    unique, counts = np.unique(pixels, axis=0, return_counts=True)
    most_frequent_color = unique[np.argmax(counts)]

    # Convert the most frequent color to hexadecimal
    most_frequent_color_hex = '#%02x%02x%02x' % tuple(most_frequent_color)
    return most_frequent_color_hex

def index(request):
    top10movie = top10alltime.objects.all()

    if request.method == "POST":
        form = DataUploadForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            return redirect(reverse('moviesystem:moviesystem_result') + f'?text={text}')

    context = {
        'top10movie': top10movie,
    }
    return render(request, 'moviesystem/app/index.html', context)


def result(request):
    movie_ids = []
    movies_information = []
    text = request.GET.get('text', '')
    movie_ids = recommended_movie_ids(text)
    movies_information = movies_details(movie_ids)

    if movies_information:
        searched_movie = movies_information[0]
        poster_url = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + searched_movie['poster_path']
        max_color_on_image = get_image_color(poster_url)
        remaining_movies = movies_information[1:]  # Remove the first element
    else:
        searched_movie = None
        max_color_on_image = None
        remaining_movies = []

    context = {
        'max_color_on_image': max_color_on_image,
        'searched_movie': searched_movie,
        'movies_information': remaining_movies
    }
    return render(request, 'moviesystem/app/result.html', context)