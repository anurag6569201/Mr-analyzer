from django.shortcuts import render
from .forms import DataUploadForm
from rockmine.ml_model import predicting_model

def rockmine(request):
    if request.method == "POST":
        form = DataUploadForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            data_list = [float(i) for i in data.split(',')]
            result_model = predicting_model(data_list)
            context = {
                'result_model': result_model,
            }
            return render(request, 'rockmine/app/result.html', context)
    else:
        form = DataUploadForm()
    
    context = {
        'datform': form,
    }
    return render(request, 'rockmine/app/index.html', context)