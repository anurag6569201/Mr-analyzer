from django.shortcuts import render
from .forms import DataUploadForm
from rockmine.ml_model import predicting_model
from rockmine.ml_model import testing_data
from rockmine.ml_model import testing_data_result
from rockmine.ml_model import testing_accuracy_score
from rockmine.ml_model import training_accuracy_score

def rockmine(request):
    testing_datapoints = testing_data()
    testing_results=testing_data_result()
    if request.method == "POST":
        form = DataUploadForm(request.POST)
        if form.is_valid():
            testing_score=testing_accuracy_score()
            training_score=training_accuracy_score()
            data_str = form.cleaned_data['data']
            data = [float(value.strip()) for value in data_str.split(',')]
            result_model = predicting_model(data)
            context = {
                'result_model': result_model,
                'testing_score':testing_score,
                'training_score':training_score,
            }
            return render(request, 'rockmine/app/result.html', context)
    else:
        form = DataUploadForm()
    
    context = {
        'testing_results':testing_results,
        'testing_datapoints': testing_datapoints,
        'datform': form,
    }
    return render(request, 'rockmine/app/index.html', context)