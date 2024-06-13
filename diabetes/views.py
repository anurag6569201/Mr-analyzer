from django.shortcuts import render
from .forms import DataUploadForm

from diabetes.ml_model import predicting_model
from diabetes.ml_model import testing_data
from diabetes.ml_model import testing_data_result
from diabetes.ml_model import testing_accuracy_score
from diabetes.ml_model import training_accuracy_score

def index(request):
    if request.method == 'POST':
        form = DataUploadForm(request.POST)
        if form.is_valid():
            testing_score = testing_accuracy_score()
            training_score = training_accuracy_score()
            pregnancy = form.cleaned_data['pregnancies']
            glucose = form.cleaned_data['glucose']
            blood_pressure = form.cleaned_data['blood_pressure']
            skin_thickness = form.cleaned_data['skin_thickness']
            insulin = form.cleaned_data['insulin']
            bmi = form.cleaned_data['bmi']
            dbf = form.cleaned_data['dbf']
            age = form.cleaned_data['age']

            data = pregnancy,glucose,blood_pressure,skin_thickness,insulin,bmi,dbf,age
            
            result_model = predicting_model(data)

            context = {
                'result_model': result_model,
                'testing_score': testing_score,
                'training_score': training_score,
            }
            return render(request, 'diabetes/app/result.html', context)
    else:
        form = DataUploadForm()

    context = {
        'datform': form,
    }
    return render(request, 'diabetes/app/index.html', context)