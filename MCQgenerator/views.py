from django.shortcuts import render
from .forms import DiseaseNameForm

def index(request):
    if request.method=="POST":
        form=DiseaseNameForm(request.POST)
        if form.is_valid():
            diseaseName=form.cleaned_data['name']
            
    
    context={
        "form":form,
    }
    return render(request, 'MCQgenerator/app/index.html')