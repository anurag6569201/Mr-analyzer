from django.shortcuts import render

def index(request):
    return render(request, 'MCQgenerator/app/index.html')