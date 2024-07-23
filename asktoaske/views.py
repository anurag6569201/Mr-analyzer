from django.shortcuts import render

def index(request):
    context={

    }
    return render(request, 'asktoaske/app/index.html',context)