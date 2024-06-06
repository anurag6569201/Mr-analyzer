from django.shortcuts import render

def rockmine(request):
    context={
        
    }
    return render(request,'rockmine/app/index.html',context)