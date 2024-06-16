from django.shortcuts import render
from .models import top10alltime

def index(request):
    top10movie=top10alltime.objects.all()
    context={
        'top10movie':top10movie,
    }
    return render(request, 'moviesystem/app/index.html', context)