from django.shortcuts import render

def index(request):
    context={

    }
    return render(request, 'moviesystem/app/index.html', context)