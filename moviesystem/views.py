from django.shortcuts import render
from .forms import DataUploadForm

from .models import top10alltime
from .TMDB_model import recommended_movie_ids
from .result_outputs import movies_details

def index(request):
    top10movie=top10alltime.objects.all()
    movie_ids = []
    if request.method=="POST":
        form = DataUploadForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data['text']
            movie_ids=recommended_movie_ids(text)
            movies_details(movie_ids)
            print(movie_ids)
    context={
        'top10movie':top10movie,
    }
    return render(request, 'moviesystem/app/index.html', context)