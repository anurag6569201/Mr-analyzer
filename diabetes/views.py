from django.shortcuts import render

def index(request):
    context={

    }
    return render(request,'diabetes/app/index.html',context)