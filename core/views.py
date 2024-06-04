from django.shortcuts import render

def index(request):
    context={

    }
    return render(request,'core/app/index.html',context)