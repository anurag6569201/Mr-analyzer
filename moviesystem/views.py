from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import DataUploadForm

from .models import top10alltime
from .TMDB_model import recommended_movie_ids
from .TMDB_model import movies_details

from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
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
        remaining_movies = movies_information[1:] 
    else:
        searched_movie = None
        remaining_movies = []

    context = {
        'searched_movie': searched_movie,
        'movies_information': remaining_movies
    }
    return render(request, 'moviesystem/app/result.html', context)